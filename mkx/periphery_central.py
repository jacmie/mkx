from mkx.communication_message import encode_message
from mkx.periphery_abstract import PeripheryAbstract


class CentralPeriphery(PeripheryAbstract):
    def receive(self) -> list[dict]:
        # Central has no transport to receive messages
        return []

    def send(self, msg_type: str, data: dict):
        self.payload = encode_message(msg_type, data)
