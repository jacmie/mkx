import digitalio
from keypad import Event as KeyEvent

from mkx.diode_orientation import DiodeOrientation

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
    def __init__(
        self,
        cols,
        rows,
        diode_orientation,
        pull,
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

        # In CircuitPython, to use a GPIO pin, wrap it in a digitalio.DigitalInOut(pin) object.
        self.drive_pins = [ensure_digital_in_out(p) for p in self.drive_pins]
        self.sense_pins = [ensure_digital_in_out(p) for p in self.sense_pins]

        # Set drive and sense pin roles
        for pin in self.drive_pins:
            pin.switch_to_output()
        for pin in self.sense_pins:
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

        for out_idx, out_pin in enumerate(self.drive_pins):
            out_pin.value = output_active

            for in_idx, in_pin in enumerate(self.sense_pins):
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

                ba_idx += 1

            out_pin.value = not output_active

        return raw_events
