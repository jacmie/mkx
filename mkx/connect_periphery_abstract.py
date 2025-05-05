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

    def receive(self) -> list[dict]:
        raise NotImplementedError(
            "Subclass of the ConnectPeripheryAbstract must implement receive()"
        )

    def send(self, msg_type: str, data: dict):
        raise NotImplementedError(
            "Subclass of the ConnectPeripheryAbstract must implement send()"
        )
