import serial

from mkx.interphace_abstract import InterfahceAbstract


class InterphaceUSB(InterfahceAbstract):
    def __init__(self, device_id="usb", baudrate=115200):
        super().__init__(device_id)
        self.baudrate = baudrate
        self.serial = None
        self.port = None
        self.reconnect()

    def is_connected(self):
        return self.serial is not None and self.serial.is_open

    def reconnect(self):
        self.serial = None
        ports = serial.tools.list_ports.comports()
        for port in ports:
            if "USB" in port.description or "CDC" in port.description:
                try:
                    self.serial = serial.Serial(port.device, self.baudrate, timeout=0.1)
                    self.port = port.device
                    print(f"[{self.device_id}] Connected on {port.device}")
                    return
                except Exception as e:
                    print(f"[{self.device_id}] Failed to open {port.device}: {e}")
        print(f"[{self.device_id}] No USB device found")

    def receive(self, verbose=False):
        if not self.ensure_connection():
            return []

        try:
            data = self.serial.read(64)
            if data:
                return self.parse_buffered_lines(data)
        except Exception as e:
            print(f"[{self.device_id}] Read error: {e}")
            self.serial.close()
            self.serial = None
        return []

    def send(self, msg_type: str, data: dict, verbose=False):
        if not self.ensure_connection():
            return

        try:
            self.serial.write(self.encode_message(msg_type, data))
        except Exception as e:
            print(f"[{self.device_id}] Send error: {e}")
            self.serial.close()
            self.serial = None
