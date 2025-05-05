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

    def get_key_events(self) -> list[tuple[int, int, bool]]:
        events = []
        data = self.uart.read(64)
        if data:
            self.buffer += data
            while b"\n" in self.buffer:
                line, self.buffer = self.buffer.split(b"\n", 1)
                try:
                    msg = json.loads(line.decode().strip())
                    if msg.get("type") == "key":
                        events.append((msg["row"], msg["col"], bool(msg["pressed"])))
                except Exception as e:
                    print("UART parse error:", e)
        return events

    def receive(self) -> list[dict]:
        # Placeholder for receiving messages from central
        return []

    def send(self, msg_type, data):
        payload = self._message(msg_type, data)
        try:
            self.uart.write(payload)
        except Exception as e:
            print("UART send error:", e)
