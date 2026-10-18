import digitalio, time
from keypad import Event as KeyEvent

from mkx.diode_orientation import DiodeOrientation
from mkx import matrix_scanner_rp_pio as rp_pio
from mkx import matrix_scanner_keypad as keypad_scan
from mkx.ansi_colors import Ansi, Ansi256

# COL2ROW:
# [ Column (output) ] → [ + anode ]---|>|---[ - cathode (diode | ) ] → [ Row (input) ]

# ROW2COL:
# [ Row (output) ] → [ + anode ]---|>|---[ - cathode (diode | ) ] → [ Column (input) ]


def ensure_digital_in_out(pin):
    # Check if the object looks like a DigitalInOut (has the right interface)
    if (
        hasattr(pin, "switch_to_input")
        and hasattr(pin, "switch_to_output")
        and hasattr(pin, "value")
    ):
        return pin
    return digitalio.DigitalInOut(pin)


class MatrixScanner:
    """Internal scan-engine used by PeripheryAbstract; not meant for direct user instantiation."""

    def __init__(
        self,
        cols,
        rows,
        diode_orientation,
        pull,
        warmup_cycles,
        use_rp_pio,
        use_keypad_scan,
    ):
        self.len_cols = len(cols)
        self.len_rows = len(rows)
        self.diode_orientation = diode_orientation
        self.pull = pull

        # Pin overlap check
        unique_pins = {repr(c) for c in cols} | {repr(r) for r in rows}
        assert (
            len(unique_pins) == self.len_cols + self.len_rows
        ), "Cannot use a pin as both a column and row"

        # Set diode_orientation
        if self.diode_orientation == DiodeOrientation.COL2ROW:
            self.anodes = cols
            self.cathodes = rows
        elif self.diode_orientation == DiodeOrientation.ROW2COL:
            self.anodes = rows
            self.cathodes = cols
        else:
            raise ValueError(f"Invalid Diode Orientation: {self.diode_orientation}")

        # Set pins
        if self.pull == digitalio.Pull.DOWN:
            self.drive_pins = self.anodes
            self.sense_pins = self.cathodes
        elif self.pull == digitalio.Pull.UP:
            self.drive_pins = self.cathodes
            self.sense_pins = self.anodes
        else:
            raise ValueError(f"Invalid Pull: {self.pull}")

        self._accelerated_scanner = None

        if use_rp_pio and rp_pio.RpPioMatrixScanner.is_eligible(
            self.drive_pins, self.sense_pins
        ):
            self._accelerated_scanner = rp_pio.RpPioMatrixScanner(
                self.drive_pins, self.sense_pins, self.pull
            )
            print(
                f"{Ansi256.MINT}MatrixScanner: using rp2pio for matrix scanning{Ansi.RESET}"
            )
            print()
        elif use_keypad_scan and keypad_scan.KeypadMatrixScanner.is_eligible(
            cols, rows
        ):
            self._accelerated_scanner = keypad_scan.KeypadMatrixScanner(
                cols, rows, self.diode_orientation
            )
            print(
                f"{Ansi256.MINT}MatrixScanner: using keypad for matrix scanning{Ansi.RESET}"
            )
            print()
        else:
            self._init_digitalio_scan()
            print(
                f"{Ansi256.MINT}MatrixScanner: using digitalio for matrix scanning{Ansi.RESET}"
            )
            print()

        initial_val = 1 if pull is digitalio.Pull.UP else 0
        self.state = bytearray([initial_val] * (self.len_cols * self.len_rows))
        time.sleep(1)

        # Run safety warmup cycles before hardware pins stabilize
        for _ in range(warmup_cycles):
            _ = self.get_key_events(use_interrupts=False)  # Throw away events
            time.sleep(0.001)

    def _init_digitalio_scan(self):
        # In CircuitPython, to use a GPIO pin, wrap it in a digitalio.DigitalInOut(pin) object.
        self.drive_pins = [ensure_digital_in_out(p) for p in self.drive_pins]
        self.sense_pins = [ensure_digital_in_out(p) for p in self.sense_pins]

        # Set drive and sense pin roles
        for pin in self.drive_pins:
            pin.switch_to_output()
        for pin in self.sense_pins:
            pin.switch_to_input(pull=self.pull)

    def get_key_events(self, use_interrupts: bool) -> list[tuple[int, int, bool]]:
        if self._accelerated_scanner is not None:
            return self._accelerated_scanner.get_key_events(self)

        if use_interrupts:
            return self._scan_interrupts()

        return self._scan_digitalio()

    def _scan_digitalio(self):
        raw_events = []
        output_active = (
            self.pull is not digitalio.Pull.UP
        )  # True if pull = digitalio.Pull.DOWN
        input_active_val = (
            0 if self.pull is digitalio.Pull.UP else 1
        )  # What value means "pressed"
        ba_idx = 0  # Index into the flat state byte array

        for out_idx, out_pin in enumerate(self.drive_pins):
            out_pin.value = output_active

            for in_idx, in_pin in enumerate(self.sense_pins):
                ba_idx = self._process_pin_state(
                    in_pin, ba_idx, input_active_val, out_idx, in_idx, raw_events
                )

            out_pin.value = not output_active

        return raw_events

    def _scan_interrupts(self):
        raw_events = []
        output_active = self.pull is not digitalio.Pull.UP
        input_active_val = 0 if self.pull is digitalio.Pull.UP else 1
        ba_idx = 0

        # Read the pins once to clear
        for pin in self.sense_pins:
            _ = pin.value

        # Isolate rows safely by resetting them to resting states first
        for out_pin in self.drive_pins:
            out_pin.value = not output_active

        for out_idx, out_pin in enumerate(self.drive_pins):
            # Actively drive ONLY the current row line
            out_pin.value = output_active

            for in_idx, in_pin in enumerate(self.sense_pins):
                ba_idx = self._process_pin_state(
                    in_pin, ba_idx, input_active_val, out_idx, in_idx, raw_events
                )

            # Instantly drop it back to resting state
            out_pin.value = not output_active

        # Drive all rows low simultaneously so a new key edge can trip the MCU
        for out_pin in self.drive_pins:
            out_pin.value = output_active

        return raw_events

    def _process_pin_state(
        self, in_pin, ba_idx, input_active_val, out_idx, in_idx, raw_events
    ) -> int:
        new_val = int(in_pin.value)
        old_val = self.state[ba_idx]

        if old_val != new_val:
            self.state[ba_idx] = new_val
            pressed = new_val == input_active_val

            if self.diode_orientation == DiodeOrientation.COL2ROW:
                col = out_idx
                row = in_idx
            else:
                row = out_idx
                col = in_idx

            if col < self.len_cols and row < self.len_rows:
                raw_events.append((col, row, pressed))
            else:
                print(f"Ignoring out-of-bounds key event: col={col}, row={row}")

        return ba_idx + 1
