from core.matrix_scanner import MatrixScanner  # assumed to exist
from communication.central_hid.central_hid_base import CentralHidBase


class MKXPeriphery:
    def __init__(self, matrix: MatrixScanner, output: CentralHidBase):
        self.matrix = matrix
        self.output = output
        self.prev_state = {}

    def run_once(self):
        state = self.matrix.scan()
        for (row, col), pressed in state.items():
            prev = self.prev_state.get((row, col), False)
            if pressed != prev:
                self.output.send_key(row, col, pressed)
        self.prev_state = state.copy()

    def run_forever(self):
        while True:
            self.run_once()
