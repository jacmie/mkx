from mkx.interphace_abstract import InterfahceAbstract
from mkx.communication_message import MessageParser


class InterphaceCentral(InterfahceAbstract):
    def __init__(self, central_periphery, col_min, row_min, col_max, row_max):
        super().__init__(
            central_periphery.device_id, col_min, row_min, col_max, row_max
        )
        self.central_periphery = central_periphery
        self.msg_parser = MessageParser()

    def is_connected(self):
        return True  # Always available

    def reconnect(self):
        pass  # Not needed

    def receive(self, verbose=False):
        try:
            data = self.central_periphery.payload
            self.central_periphery.payload = None
            if data:
                return self.msg_parser.parse(data, verbose)
        except Exception as e:
            print(f"[{self.device_id}] Central read error: {e}")
            self.uart = None  # Mark as disconnected
        return []

    def send(self, msg_type: str, data: dict, verbose=False):
        pass  # Placeholder for sending messages from central to perypheries
