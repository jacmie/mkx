import sys

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_hid.keyboard import Keyboard
from mkx.hid_abstract import HID_abstract


class HID_BLE(HID_abstract):
    def __init__(self):
        try:
            self.ble = BLERadio()
            self.hid = HIDService()
            self.advertisement = ProvideServicesAdvertisement(self.hid)

            print("Starting BLE advertisement...")
            self.ble.start_advertising(self.advertisement)

            # Wait for connection
            while not self.ble.connected:
                pass

            print("BLE connected")
            self.keyboard = Keyboard(self.hid.devices)

        except (ImportError, RuntimeError) as e:
            print("BLE initialization failed:", e)
            print("This board may not support BLE or the firmware lacks BLE support.")
            sys.exit()

    def send_key(self, keycode, pressed):
        if pressed:
            self.keyboard.press(keycode)
        else:
            self.keyboard.release(keycode)
