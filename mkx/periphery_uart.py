import busio

from mkx.communication_message import encode_message
from mkx.periphery_abstract import PeripheryAbstract


class PeripheryUART(PeripheryAbstract):
    def __init__(
        self,
        device_id,
        col_pins,
        row_pins,
        tx_pin,
        *,
        rx_pin=None,
        baudrate=9600,
        **kwargs
    ):
        super().__init__(device_id, col_pins, row_pins, **kwargs)
        self.uart = busio.UART(tx_pin, rx_pin, baudrate=baudrate, timeout=0.01)
        self.buffer = b""

    def receive(self, verbose=False) -> list[dict]:
        # Placeholder for receiving messages from central
        return []

    def send(self, msg_type: str, data: dict, verbose=False):
        payload = encode_message(self.device_id, msg_type, data, verbose)
        try:
            self.uart.write(payload)
        except Exception as e:
            print("UART send error:", e)
