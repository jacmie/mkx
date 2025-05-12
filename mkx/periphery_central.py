from mkx.communication_message import encode_message
from mkx.periphery_abstract import PeripheryAbstract


class CentralPeriphery(PeripheryAbstract):
    def __init__(self, device_id, col_pins, row_pins, **kwargs):
        super().__init__(device_id, col_pins, row_pins, **kwargs)
        self.payload = None

    def receive(self, verbose=False) -> list[dict]:
        # Central has no transport to receive messages
        return []

    def send(self, msg_type: str, data: dict, verbose=False):
        self.payload = encode_message(self.device_id, msg_type, data, verbose)
