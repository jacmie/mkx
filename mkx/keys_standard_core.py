"""
Core KeysStandard class definition - no key instances.
"""

from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from mkx.keys_abstract import KeysAbstract


class KeysStandard(KeysAbstract):
    """
    A standard key that sends a HID keycode using Adafruit HID library.
    """

    __slots__ = ("key_code", "key_name")

    def __init__(self, key_code: Keycode, key_name: str):
        super().__init__()
        self.key_code = key_code
        self.key_name = key_name

    def on_press(self, _, keyboard: Keyboard, __):
        keyboard.press(self.key_code)

    def on_release(self, _, keyboard: Keyboard, __):
        keyboard.release(self.key_code)
