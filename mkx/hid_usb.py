import usb_hid
from adafruit_hid.keyboard import Keyboard

from mkx.hid_abstract import HID_abstract


class HID_USB(HID_abstract):
    def __init__(self):
        self.keyboard = Keyboard(usb_hid.devices)

    def send_key(self, keycode, pressed):
        if pressed:
            self.keyboard.press(keycode)
        else:
            self.keyboard.release(keycode)
