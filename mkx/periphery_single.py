from mkx.periphery_abstract import PeripheryAbstract


class PeripherySingle(PeripheryAbstract):
    def __init__(self, col_pins, row_pins, **kwargs):
        # device_id has to match the one used in InterfaceSingle
        super().__init__("keyboard_single", col_pins, row_pins, **kwargs)

    def receive(self, verbose=False) -> list[dict]:
        # Single has no transport to receive messages
        return []

    def send(self, msg_type: str, data: dict, verbose=False):
        pass
