import time
from collections import OrderedDict

from mkx.periphery_abstract import PeripheryAbstract


class MKX_Periphery:
    def __init__(self, periphery: PeripheryAbstract, debug=False):
        self.periphery = periphery
        self.debug = debug

    def run_once(self):
        if self.periphery:
            signal = self.periphery.get_key_events()
            for col, row, pressed in signal:
                self.periphery.send(
                    "key_event",
                    OrderedDict(
                        [("col", col), ("row", row), ("pressed", pressed)],
                    ),
                    verbose=True,
                )

        time.sleep(0.001)  # Keep CPU usage low

        if self.debug and self.periphery:
            self.periphery.debug_receive(verbose=True)

    def run_forever(self):
        while True:
            self.run_once()
