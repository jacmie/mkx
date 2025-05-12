import digitalio
from keypad import Event as KeyEvent

from mkx.diode_orientation import DiodeOrientation

# COL2ROW:
# [ Column (output) ] → [ + anode ]---|>|---[ - cathode ] → [ Row (input) ]


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
    def __init__(
        self,
        cols,
        rows,
        diode_orientation=DiodeOrientation.COL2ROW,
        pull=digitalio.Pull.DOWN,
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
        if diode_orientation == DiodeOrientation.COL2ROW:
            anode_pins, cathode_pins = cols, rows
        elif diode_orientation == DiodeOrientation.ROW2COL:
            anode_pins, cathode_pins = rows, cols
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

        initial_val = 1 if pull is digitalio.Pull.UP else 0
        self.state = bytearray([initial_val] * (self.len_cols * self.len_rows))

    def get_key_events(self) -> list[tuple[int, int, bool]]:
        raw_events = []
        output_active = (
            self.pull is not digitalio.Pull.UP
        )  # True if pull = digitalio.Pull.DOWN
        input_active_val = (
            0 if self.pull is digitalio.Pull.UP else 1
        )  # What value means "pressed"
        ba_idx = 0  # Index into the flat state byte array

        for out_idx, out_pin in enumerate(self.outputs):
            out_pin.value = output_active

            for in_idx, in_pin in enumerate(self.inputs):
                new_val = int(in_pin.value)
                old_val = self.state[ba_idx]

                if old_val != new_val:
                    self.state[ba_idx] = new_val
                    pressed = new_val == input_active_val

                    if self.diode_orientation == DiodeOrientation.COL2ROW:
                        col = in_idx
                        row = out_idx
                    else:
                        row = in_idx
                        col = out_idx

                    if col < self.len_cols and row < self.len_rows:
                        raw_events.append((col, row, pressed))
                    else:
                        print(f"Ignoring out-of-bounds key event: col={col}, row={row}")

                ba_idx += 1

            out_pin.value = not output_active

        return raw_events
