import busio
import board

from mkx.connect_periphery_abstract import ConnectPeripheryAbstract
from mkx.communication_message import encode_message, parse_message


class CentralUART(ConnectPeripheryAbstract):
    def __init__(
        self, tx_pin=board.TX, rx_pin=board.RX, baudrate=115200, device_id="uart"
    ):
        super().__init__(device_id)
        self.tx_pin = tx_pin
        self.rx_pin = rx_pin
        self.baudrate = baudrate
        self.uart = None
        self.reconnect()

    def is_connected(self):
        return self.uart is not None

    def reconnect(self):
        try:
            self.uart = busio.UART(
                self.tx_pin, self.rx_pin, baudrate=self.baudrate, timeout=0.01
            )
            print(f"[{self.device_id}] UART reconnected")
        except Exception as e:
            print(f"[{self.device_id}] UART reconnect failed: {e}")
            self.uart = None

    def receive(self, verbose=False):
        if not self.ensure_connection():
            return []

        try:
            data = self.uart.read(64)
            if data:
                return parse_message(data)
        except Exception as e:
            print(f"[{self.device_id}] UART read error: {e}")
            self.uart = None  # Mark as disconnected
        return []

    def send(self, msg_type: str, data: dict, verbose=False):
        if not self.ensure_connection():
            return

        try:
            self.uart.write(encode_message(msg_type, data))
        except Exception as e:
            print(f"[{self.device_id}] UART send error: {e}")
            self.uart = None
