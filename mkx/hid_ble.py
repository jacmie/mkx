import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from mkx.hid_abstract import HID_abstract


class HID_BLE(HID_abstract):
    def __init__(self):
        self.keyboard = Keyboard(usb_hid.devices)

    def send_key(self, keycode, pressed):
        if pressed:
            self.keyboard.press(keycode)
        else:
            self.keyboard.release(keycode)
