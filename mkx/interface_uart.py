import busio

from mkx.interface_abstract import InterfaceAbstract
from mkx.communication_message import encode_message, MessageParser
from mkx.error import halt_on_error


class InterfaceUART(InterfaceAbstract):
    def __init__(
        self,
        device_id,
        tx_pin,
        rx_pin,
        col_min,
        row_min,
        col_max,
        row_max,
        baudrate=9600,  # more then enough for short messages and saves battery in whireless keyboards
    ):
        super().__init__(device_id, col_min, row_min, col_max, row_max)
        self.tx_pin = tx_pin
        self.rx_pin = rx_pin
        self.baudrate = baudrate
        self.uart = None
        self.msg_parser = MessageParser()

        self.reconnect()

    def is_connected(self):
        return self.uart is not None

    def reconnect(self):
        try:
            if self.tx_pin is None and self.rx_pin is None:
                print(f"[{self.device_id}] No TX or RX pins configured - UART disabled")
                self.uart = None
                return

            # busio.UART expects both pins to be valid, so use None carefully
            self.uart = busio.UART(
                self.tx_pin, self.rx_pin, baudrate=self.baudrate, timeout=0.01
            )

            print(f"[{self.device_id}] UART reconnected")
        except Exception as e:
            self.uart = None
            halt_on_error(
                "[{self.device_id}] UART reconnect failed: {e}!",
                status_led=None,
            )

    def receive(self, verbose=False):
        if not self.ensure_connection():
            return []

        messages = []

        if self.uart is not None and self.uart.in_waiting >= 1:
            try:
                data = self.uart.read(self.uart.in_waiting)
                # print("data:", data)
                if data:
                    messages = self.msg_parser.parse(data, verbose=True)

            except Exception as e:
                print("UART receive error:", e)

        return messages

    def send(self, msg_type: str, data: dict, verbose=False):
        if not self.ensure_connection():
            return

        try:
            self.uart.write(encode_message(msg_type, data))
        except Exception as e:
            print(f"[{self.device_id}] UART send error: {e}")
            self.uart = None
