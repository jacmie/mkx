import busio
import board

import rp2pio

print(rp2pio)

try:
    # from adafruit_pio_uart import PIO_UART
    from mkx.pio_uart import PIO_UART

    PIOUART_AVAILABLE = True
except ImportError:
    PIOUART_AVAILABLE = False

from mkx.interphace_abstract import InterfahceAbstract
from mkx.communication_message import encode_message, MessageParser


class InterphaceUART(InterfahceAbstract):
    def __init__(
        self,
        device_id,
        tx_pin,
        rx_pin,
        col_min,
        row_min,
        col_max,
        row_max,
        use_pio=False,
        baudrate=9600,  # more then enough for short messages and saves battery in whireless keyboards
    ):
        super().__init__(device_id, col_min, row_min, col_max, row_max)
        self.tx_pin = tx_pin
        self.rx_pin = rx_pin
        self.use_pio = use_pio
        self.baudrate = baudrate
        self.uart = None
        self.msg_parser = MessageParser()

        self.reconnect()

    def is_connected(self):
        return self.uart is not None

    def reconnect(self):
        try:
            if self.tx_pin is None and self.rx_pin is None:
                print(f"[{self.device_id}] No TX or RX pins configured → UART disabled")
                self.uart = None
                return

            if self.use_pio:
                # if not PIOUART_AVAILABLE:
                #     raise RuntimeError(
                #         "PIOUART not available on this board or not installed!"
                #     )

                self.uart = PIO_UART(
                    tx=self.tx_pin, rx=self.rx_pin, baudrate=self.baudrate
                )
                print(
                    f"[{self.device_id}] PIOUART connected "
                    # f"(TX={'yes' if self.tx_pin else 'no'}, RX={'yes' if self.rx_pin else 'no'})"
                )

            else:
                # busio.UART expects both pins to be valid, so use None carefully
                self.uart = busio.UART(
                    self.tx_pin, self.rx_pin, baudrate=self.baudrate, timeout=0.01
                )

                print(
                    f"[{self.device_id}] busio.UART connected "
                    # f"(TX={'yes' if self.tx_pin else 'no'}, RX={'yes' if self.rx_pin else 'no'})"
                )

            print(f"[{self.device_id}] UART reconnected")
        except Exception as e:
            print(f"[{self.device_id}] UART reconnect failed: {e}")
            self.uart = None

    def receive(self, verbose=False):
        # print("UART")
        if not self.ensure_connection():
            return []
        print("after ensure_connection")

        try:
            in_waiting = getattr(self.uart, "in_waiting", None)
            if in_waiting is not None:
                # UART has in_waiting property → safe to check
                if in_waiting > 0:
                    data = self.uart.read(64)
                    print("data: ", data)
                    if data:
                        print("ret msg")
                        return self.msg_parser.parse(data, verbose)
            else:
                # No in_waiting property → assume non-blocking read (busio UART)
                data = self.uart.read(64)
                print("data: ", data)
                if data:
                    print("ret msg")
                    return self.msg_parser.parse(data, verbose)
        except Exception as e:
            print(f"[{self.device_id}] UART read error: {e}")
            self.uart = None  # Mark as disconnected
        print("ret")
        return []

    def send(self, msg_type: str, data: dict, verbose=False):
        if not self.ensure_connection():
            return

        try:
            self.uart.write(encode_message(msg_type, data))
        except Exception as e:
            print(f"[{self.device_id}] UART send error: {e}")
            self.uart = None

    # def receive(self, verbose=False):
    #     if not self.ensure_connection():
    #         return []

    #     try:
    #         # Check if there's data waiting to avoid blocking
    #         if hasattr(self.uart, "in_waiting"):
    #             n = self.uart.in_waiting
    #             if n == 0:
    #                 return []

    #             # Read only the available data (not a fixed 64)
    #             data = self.uart.read(n)
    #         else:
    #             # Fallback: read whatever is available, up to 64 bytes
    #             data = self.uart.read(64)

    #         if data:
    #             return self.msg_parser.parse(data, verbose)

    #     except Exception as e:
    #         print(f"[{self.device_id}] UART read error: {e}")
    #         self.uart = None

    #     return []
