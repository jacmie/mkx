from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement

from mkx.interphace_abstract import InterfahceAbstract
from mkx.communication_message import encode_message, parse_message


class InterphaceBLE(InterfahceAbstract):
    def __init__(self, device_id="ble"):
        super().__init__(device_id)
        self.ble = BLERadio()
        self.conn = None
        self.uart = None
        self.reconnect()

    def is_connected(self):
        return self.conn and self.conn.connected

    def reconnect(self):
        print(f"[{self.device_id}] Scanning for BLE devices...")
        self.conn = None
        self.uart = None
        try:
            for adv in self.ble.start_scan(ProvideServicesAdvertisement, timeout=5):
                if UARTService in adv.services:
                    self.conn = self.ble.connect(adv)
                    self.uart = self.conn[UARTService]
                    print(f"[{self.device_id}] BLE connected to {adv.address}")
                    break
        except Exception as e:
            print(f"[{self.device_id}] BLE reconnect failed: {e}")
        finally:
            self.ble.stop_scan()

    def receive(self, verbose=False):
        if not self.ensure_connection():
            return []

        try:
            if self.uart.in_waiting:
                return parse_message(self.uart.read())
        except Exception as e:
            print(f"[{self.device_id}] BLE read error: {e}")
            self.conn = None  # Force reconnect
        return []

    def send(self, msg_type: str, data: dict, verbose=False):
        if not self.ensure_connection():
            return

        try:
            self.uart.write(encode_message(msg_type, data))
        except Exception as e:
            print(f"[{self.device_id}] BLE send error: {e}")
            self.conn = None


# import time
# from adafruit_ble import BLERadio
# from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
# from adafruit_ble.services.nordic import UARTService

# ble = BLERadio()
# TARGET_NAME = "SensorNode_001"

# def find_and_connect():
#     print("Scanning for sensor...")
#     for adv in ble.start_scan(ProvideServicesAdvertisement, timeout=5):
#         if adv.complete_name == TARGET_NAME:
#             print(f"Found {TARGET_NAME}, connecting...")
#             ble.stop_scan()
#             return ble.connect(adv)
#     return None

# connection = None

# while True:
#     if not connection or not connection.connected:
#         connection = find_and_connect()
#         time.sleep(1)

#     if connection and connection.connected:
#         uart = connection[UARTService]
#         uart.write(b"GET_TEMP\n")
#         print("Sent GET_TEMP command")
#         time.sleep(1)
#         if uart.in_waiting:
#             response = uart.read().decode().strip()
#             print(f"Received from peripheral: {response}")
#     else:
#         print("Disconnected. Retrying...")
#         time.sleep(2)
