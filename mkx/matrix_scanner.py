import digitalio
from keypad import Event as KeyEvent

from mkx.diode_orientation import DiodeOrientation


def ensure_digital_in_out(pin):
    # Check if the object looks like a DigitalInOut (has the right interface)
    if (
        hasattr(pin, "switch_to_input")
        and hasattr(pin, "switch_to_output")
        and hasattr(pin, "value")
    ):
        return pin
    return digitalio.DigitalInOut(pin)
    # return pin if pin.__class__.__name__ == 'DigitalInOut' else digitalio.DigitalInOut(pin)


class MatrixScanner:
    def __init__(
        self,
        cols,
        rows,
        diode_orientation=DiodeOrientation.COLUMNS,
        pull=digitalio.Pull.DOWN,
        rollover_cols_every_rows=None,
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
        if diode_orientation == DiodeOrientation.COLUMNS:
            anode_pins, cathode_pins = cols, rows
            self.translate_coords = True
        elif diode_orientation == DiodeOrientation.ROWS:
            anode_pins, cathode_pins = rows, cols
            self.translate_coords = False
        else:
            raise ValueError(f"Invalid DiodeOrientation: {diode_orientation}")

        # In CircuitPython, to use a GPIO pin, wrap it in a digitalio.DigitalInOut(pin) object.
        self.anodes = [ensure_digital_in_out(p) for p in anode_pins]
        self.cathodes = [ensure_digital_in_out(p) for p in cathode_pins]

        # Recognize pull direction
        self.outputs, self.inputs = (
            (self.anodes, self.cathodes)
            if pull == digitalio.Pull.DOWN
            else (self.cathodes, self.anodes)
        )

        # Set input and output pins
        for pin in self.outputs:
            pin.switch_to_output()
        for pin in self.inputs:
            pin.switch_to_input(pull=self.pull)

        self.rollover_cols_every_rows = rollover_cols_every_rows or self.len_rows

        initial_state_value = b"\x01" if pull is digitalio.Pull.UP else b"\x00"
        self.state = bytearray(initial_state_value) * self.len_cols * self.len_rows

    def get_key_events(self) -> list[tuple[int, int, bool]]:
        raw_events = []
        output_active = self.pull is not digitalio.Pull.UP
        input_active_val = 0 if self.pull is digitalio.Pull.UP else 1
        ba_idx = 0

        for oidx, opin in enumerate(self.outputs):
            opin.value = output_active

            for iidx, ipin in enumerate(self.inputs):
                new_val = int(ipin.value)
                old_val = self.state[ba_idx]

                if old_val != new_val:
                    self.state[ba_idx] = new_val
                    pressed = new_val == input_active_val

                    # Translate coords based on diode orientation
                    if self.translate_coords:
                        row = iidx % self.rollover_cols_every_rows
                        col = oidx + self.len_cols * (
                            iidx // self.rollover_cols_every_rows
                        )
                    else:
                        row = oidx
                        col = iidx

                    raw_events.append((row, col, pressed))

                ba_idx += 1

            opin.value = not output_active

        return raw_events

    def scan_for_changes(self):
        """
        Scans the entire key matrix for all state changes.
        Returns a list of KeyEvent instances or an empty list if no change.
        """
        ba_idx = 0
        key_events = []
        output_active = self.pull is not digitalio.Pull.UP
        input_active_val = 0 if self.pull is digitalio.Pull.UP else 1

        for oidx, opin in enumerate(self.outputs):
            opin.value = output_active

            for iidx, ipin in enumerate(self.inputs):
                new_val = int(ipin.value)
                old_val = self.state[ba_idx]

                if old_val != new_val:
                    if self.translate_coords:
                        row = iidx % self.rollover_cols_every_rows
                        col = oidx + self.len_cols * (
                            iidx // self.rollover_cols_every_rows
                        )
                    else:
                        row = oidx
                        col = iidx

                    pressed = new_val == input_active_val
                    key_number = self.len_cols * row + col + self.offset
                    key_events.append(KeyEvent(key_number, pressed))
                    self.state[ba_idx] = new_val

                ba_idx += 1

            opin.value = not output_active  # reset output

        return key_events
