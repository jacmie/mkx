# uart_periphery.py

import busio
import board
import json
from periphery_abstract import PeripheryAbstract


class UARTPeriphery(PeripheryAbstract):
    def __init__(
        self, tx_pin=board.TX, rx_pin=board.RX, baudrate=115200, device_id="uart"
    ):
        super().__init__(device_id)
        self.uart = busio.UART(tx_pin, rx_pin, baudrate=baudrate, timeout=0.01)
        self.buffer = b""

    def receive(self) -> list[dict]:
        # Placeholder for receiving messages from central
        return []

    def send(self, msg_type, data):
        payload = self._message(msg_type, data)
        try:
            self.uart.write(payload)
        except Exception as e:
            print("UART send error:", e)
