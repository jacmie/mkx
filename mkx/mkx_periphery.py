from communication.central_hid.central_hid_base import CentralHidBase


class MKX_Periphery:
    def __init__(self, output: CentralHidBase):
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
