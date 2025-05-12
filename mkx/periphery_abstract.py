import digitalio

from mkx.diode_orientation import DiodeOrientation
from mkx.matrix_scanner import MatrixScanner


class PeripheryAbstract:
    def __init__(
        self,
        device_id,
        col_pins,
        row_pins,
        *,
        diode_orientation=DiodeOrientation.COLUMNS,
        pull=digitalio.Pull.UP,
        rollover_cols_every_rows=None
    ):
        self.device_id = device_id or "unknown"

        self.matrix_scanner = MatrixScanner(
            cols=col_pins,
            rows=row_pins,
            diode_orientation=diode_orientation,
            pull=pull,
            rollover_cols_every_rows=rollover_cols_every_rows,
        )

    def get_key_events(self) -> list[tuple[int, int, bool]]:
        """Returns a list of (row, col, pressed) events"""
        return self.matrix_scanner.get_key_events()

    def receive(self, verbose=False) -> list[dict]:
        """Return list of incoming messages as parsed dicts."""
        raise NotImplementedError(
            "Subclass of the PeripheryAbstract must implement receive()"
        )

    def send(self, msg_type: str, data: dict, verbose=False):
        """Send a structured message to the peripheral."""
        raise NotImplementedError(
            "Subclass of the PeripheryAbstract must implement send()"
        )
