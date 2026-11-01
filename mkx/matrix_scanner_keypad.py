from mkx.diode_orientation import DiodeOrientation
from mkx.ansi_colors import Ansi, Ansi256

# the keypad module isn't included in every CircuitPython build/port
try:
    import keypad
    import microcontroller

    _has_keypad = True
except ImportError:
    _has_keypad = False


def _fallback(reason: str) -> bool:
    print(f"{Ansi256.PEACH}MatrixScanner: keypad not used ({reason}){Ansi.RESET}")
    return False


class KeypadMatrixScanner:
    """Drives/reads the matrix via the CircuitPython keypad.KeyMatrix background scanner."""

    enabled = True

    @classmethod
    def set_enabled(cls, enabled: bool):
        cls.enabled = enabled

    @classmethod
    def is_eligible(cls, cols, rows) -> bool:
        if not cls.enabled:
            return _fallback("disabled via use_keypad_scan(False)")

        if not _has_keypad:
            return _fallback("keypad module not available on this board")

        # keypad.KeyMatrix only drives/reads raw microcontroller pins directly, not
        # wrapped digitalio objects or pins behind an I2C expander (e.g. MCP23017)
        all_pins = list(cols) + list(rows)
        if not all(isinstance(p, microcontroller.Pin) for p in all_pins):
            return _fallback("pins are not raw microcontroller pins")

        return True

    def __init__(self, cols, rows, diode_orientation):
        self.col_count = len(cols)

        # DiodeOrientation.COL2ROW means the diode anode is on the column side
        columns_to_anodes = diode_orientation == DiodeOrientation.COL2ROW

        self._km = keypad.KeyMatrix(
            row_pins=rows,
            column_pins=cols,
            columns_to_anodes=columns_to_anodes,
        )

    def get_key_events(self, matrix_scanner) -> list[tuple[int, int, bool]]:
        raw_events = []

        while True:
            event = self._km.events.get()
            if event is None:
                break

            row, col = divmod(event.key_number, self.col_count)
            raw_events.append((col, row, event.pressed))

        return raw_events
