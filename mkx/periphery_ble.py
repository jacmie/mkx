# ble_periphery.py

from adafruit_ble import BLERadio
from adafruit_ble.services.nordic import UARTService
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
import json

from mkx.periphery_abstract import PeripheryAbstract


class PeripheryBLE(PeripheryAbstract):
    def __init__(self, device_id="ble"):
        super().__init__(device_id)
        self.ble = BLERadio()
        self.connections = []
        self.uart_services = []

    def scan_and_connect(self):
        print("Scanning for BLE devices...")
        for adv in self.ble.start_scan(ProvideServicesAdvertisement, timeout=5):
            if UARTService in adv.services:
                try:
                    conn = self.ble.connect(adv)
                    uart = conn[UARTService]
                    self.connections.append(conn)
                    self.uart_services.append(uart)
                    print(f"Connected to: {adv.complete_name}")
                except Exception as e:
                    print("BLE connect error:", e)
        self.ble.stop_scan()

    def receive(self, verbose=False) -> list[dict]:
        # Placeholder for receiving messages from central
        return []

    def send(self, msg_type, data, verbose=False):
        payload = self._message(msg_type, data)
        for uart in self.uart_services:
            try:
                uart.write(payload)
            except Exception as e:
                print("BLE send error:", e)


# import time
# import board
# import microcontroller
# from adafruit_ble import BLERadio
# from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
# from adafruit_ble.services.nordic import UARTService

# ble = BLERadio()
# uart = UARTService()
# advertisement = ProvideServicesAdvertisement(uart)
# advertisement.complete_name = "SensorNode_001"

# print("Peripheral advertising...")

# while True:
#     ble.start_advertising(advertisement)
#     while not ble.connected:
#         time.sleep(0.1)

#     print("Connected!")
#     while ble.connected:
#         if uart.in_waiting:
#             cmd = uart.read().decode().strip()
#             print(f"Command received: {cmd}")

#             if cmd == "GET_TEMP":
#                 temperature = microcontroller.cpu.temperature  # Or sensor read
#                 msg = f"TEMP:{temperature:.2f}\n"
#                 uart.write(msg.encode())
#                 print(f"Sent: {msg}")
#         time.sleep(0.5)
