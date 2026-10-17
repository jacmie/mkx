import array
import digitalio

from mkx.diode_orientation import DiodeOrientation
from mkx.ansi_colors import Ansi, Ansi256

# rp2pio/adafruit_pioasm/microcontroller only exist on RP2040/RP2350 boards
try:
    import rp2pio
    import adafruit_pioasm
    import microcontroller

    _has_rp2pio = True
except ImportError:
    _has_rp2pio = False

PIO_FREQUENCY = 1_000_000  # 1 MHz -> 1us per PIO cycle
PIO_SETTLE_CYCLES = (
    5  # cycles to let the driven column line settle before sampling rows
)

_enabled = True  # user-facing toggle, see MKX_Abstract.use_rp_pio()


def set_enabled(enabled: bool):
    global _enabled
    _enabled = enabled


def _fallback(reason: str) -> bool:
    print(f"{Ansi256.PEACH}MatrixScanner: rp2pio not used ({reason}){Ansi.RESET}")
    return False


def is_eligible(drive_pins, sense_pins) -> bool:
    if not _enabled:
        return _fallback("disabled via use_rp_pio(False)")

    if not _has_rp2pio:
        return _fallback("rp2pio/adafruit_pioasm not available on this board")

    # rp2pio only drives/reads raw microcontroller pins directly, not
    # wrapped digitalio objects or pins behind an I2C expander (e.g. MCP23017)
    all_pins = drive_pins + sense_pins
    if not all(isinstance(p, microcontroller.Pin) for p in all_pins):
        return _fallback("pins are not raw microcontroller pins")

    # "out pins"/"in pins" can only address up to 32 pins in one instruction
    if len(drive_pins) > 32 or len(sense_pins) > 32:
        return _fallback("more than 32 column/row pins")

    # "out pins, N"/"in pins, N" each need a single contiguous GPIO range
    if not (
        rp2pio.pins_are_sequential(drive_pins)
        and rp2pio.pins_are_sequential(sense_pins)
    ):
        return _fallback("column/row pins are not a contiguous GPIO range")

    return True


def _build_program(col_count, row_count):
    lines = [
        ".program matrix_scan",
        ".wrap_target",
        "    pull block",
        f"    out pins, {col_count}",
        f"    nop [{PIO_SETTLE_CYCLES}]",
        f"    in pins, {row_count}",
        "    push block",
        ".wrap",
    ]
    return "\n".join(lines)


class RpPioMatrixScanner:
    """Drives columns and samples rows via the RP2040/RP2350 PIO block."""

    def __init__(self, drive_pins, sense_pins, pull):
        self.drive_pins = drive_pins
        self.sense_pins = sense_pins

        col_count = len(drive_pins)
        row_count = len(sense_pins)
        col_mask = (1 << col_count) - 1
        output_active = pull is digitalio.Pull.DOWN

        program = adafruit_pioasm.assemble(_build_program(col_count, row_count))
        idle_word = 0 if output_active else col_mask

        pull_kwargs = {}
        if pull is digitalio.Pull.UP:
            pull_kwargs["pull_in_pin_up"] = (1 << row_count) - 1
        else:
            pull_kwargs["pull_in_pin_down"] = (1 << row_count) - 1

        self._sm = rp2pio.StateMachine(
            program,
            frequency=PIO_FREQUENCY,
            first_out_pin=drive_pins[0],
            out_pin_count=col_count,
            initial_out_pin_direction=col_mask,
            initial_out_pin_state=idle_word,
            first_in_pin=sense_pins[0],
            in_pin_count=row_count,
            in_shift_right=True,
            out_shift_right=True,
            **pull_kwargs,
        )

        self._col_patterns = array.array(
            "I",
            (
                (1 << i) if output_active else (~(1 << i) & col_mask)
                for i in range(col_count)
            ),
        )
        self._row_samples = array.array("I", [0] * col_count)

    def get_key_events(self, matrix_scanner) -> list[tuple[int, int, bool]]:
        raw_events = []
        input_active_val = 0 if matrix_scanner.pull is digitalio.Pull.UP else 1
        ba_idx = 0

        self._sm.write_readinto(self._col_patterns, self._row_samples)

        for out_idx in range(len(self.drive_pins)):
            row_bits = self._row_samples[out_idx]

            for in_idx in range(len(self.sense_pins)):
                new_val = (row_bits >> in_idx) & 1
                old_val = matrix_scanner.state[ba_idx]

                if old_val != new_val:
                    matrix_scanner.state[ba_idx] = new_val
                    pressed = new_val == input_active_val

                    if matrix_scanner.diode_orientation == DiodeOrientation.COL2ROW:
                        col = out_idx
                        row = in_idx
                    else:
                        row = out_idx
                        col = in_idx

                    if col < matrix_scanner.len_cols and row < matrix_scanner.len_rows:
                        raw_events.append((col, row, pressed))
                    else:
                        print(f"Ignoring out-of-bounds key event: col={col}, row={row}")

                ba_idx += 1

        return raw_events
