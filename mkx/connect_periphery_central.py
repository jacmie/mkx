from mkx.connect_periphery_abstract import ConnectPeripheryAbstract
from mkx.communication_message import MessageParser


class ConnectPeripheryCentral(ConnectPeripheryAbstract):
    def __init__(self, central_periphery):
        super().__init__("central")
        self.central_periphery = central_periphery
        self.msg_parser = MessageParser()

    def is_connected(self):
        return True  # Always available

    def reconnect(self):
        pass  # Not needed

    def receive(self):
        # if not self.is_connected():
        #     self.reconnect()
        #     return []

        try:
            # data = self.uart.read(64)
            data = self.central_periphery.payload
            if data:
                return self.msg_parser.parse(data)
            # return self.msg_parser.parse(
            #     b'{"type":"key_event","row":1,"col":2,"pressed":true}\n'
            # )
        except Exception as e:
            print(f"[{self.device_id}] Central read error: {e}")
            self.uart = None  # Mark as disconnected
        return []
        # return self.central_periphery.receive()

    def send(self, msg_type: str, data: dict):
        pass  # Placeholder for sending messages from central to perypheries
