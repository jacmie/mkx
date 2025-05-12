class ConnectPeripheryAbstract:
    def __init__(self, device_id):
        self.device_id = device_id
        self.buffer = b""

    def is_connected(self) -> bool:
        raise NotImplementedError(
            "Subclass of the ConnectPeripheryAbstract must implement is_connected()"
        )

    def reconnect(self):
        raise NotImplementedError(
            "Subclass of the ConnectPeripheryAbstract must implement reconnect()"
        )

    def receive(self, verbose=False) -> list[dict]:
        raise NotImplementedError(
            "Subclass of the ConnectPeripheryAbstract must implement receive()"
        )

    def send(self, msg_type: str, data: dict, verbose=False):
        raise NotImplementedError(
            "Subclass of the ConnectPeripheryAbstract must implement send()"
        )

    def ensure_connection(self) -> bool:
        if not self.is_connected():
            # print("Not connected, attempting to reconnect...")
            self.reconnect()
            if not self.is_connected():
                print("Reconnection failed.")
                return False
        return True
