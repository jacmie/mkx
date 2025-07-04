from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from mkx.keys_abstract import KeysAbstract


class KeysMedia(KeysAbstract):
    """
    A Media key that sends a HID keycode using Adafruit HID library.
    """

    def __init__(self, key_code: Keycode, key_name: str):
        super().__init__()
        self.key_code = key_code
        self.key_name = key_name

    def on_press(self, _, keyboard: Keyboard, __):
        keyboard.press(self.key_code)

    def on_release(self, _, keyboard: Keyboard, __):
        keyboard.release(self.key_code)


# Media key definitions

MUTE = KeysMedia(0xE2, "MUTE")
"""``MUTE``"""
AUDIO_MUTE = KeysMedia(0xE2, "AUDIO_MUTE")
"""``AUDIO_MUTE``"""

VOLU = KeysMedia(0xE9, "VOLU")
"""``VOLU``"""
AUDIO_VOL_UP = KeysMedia(0xE9, "AUDIO_VOL_UP")
"""``AUDIO_VOL_UP``"""

VOLD = KeysMedia(0xEA, "VOLD")
"""``VOLD``"""
AUDIO_VOL_DOWN = KeysMedia(0xEA, "AUDIO_VOL_DOWN")
"""``AUDIO_VOL_DOWN``"""

BRIU = KeysMedia(0x6F, "BRIU")
"""``BRIU``"""
BRIGHTNESS_UP = KeysMedia(0x6F, "BRIGHTNESS_UP")
"""``BRIGHTNESS_UP``"""

BRID = KeysMedia(0x70, "BRID")
"""``BRID``"""
BRIGHTNESS_DOWN = KeysMedia(0x70, "BRIGHTNESS_DOWN")
"""``BRIGHTNESS_DOWN``"""

MNXT = KeysMedia(0xB5, "MNXT")
"""``MNXT``"""
MEDIA_NEXT_TRACK = KeysMedia(0xB5, "MEDIA_NEXT_TRACK")
"""``MEDIA_NEXT_TRACK``"""

MPRV = KeysMedia(0xB6, "MPRV")
"""``MPRV``"""
MEDIA_PREV_TRACK = KeysMedia(0xB6, "MEDIA_PREV_TRACK")
"""``MEDIA_PREV_TRACK``"""

MSTP = KeysMedia(0xB7, "MSTP")
"""``MSTP``"""
MEDIA_STOP = KeysMedia(0xB7, "MEDIA_STOP")
"""``MEDIA_STOP``"""

MPLY = KeysMedia(0xCD, "MPLY")
"""``MPLY``"""
MEDIA_PLAY_PAUSE = KeysMedia(0xCD, "MEDIA_PLAY_PAUSE")
"""``MEDIA_PLAY_PAUSE``"""

EJCT = KeysMedia(0xB8, "EJCT")
"""``EJCT``"""
MEDIA_EJECT = KeysMedia(0xB8, "MEDIA_EJECT")
"""``MEDIA_EJECT``"""

MFFD = KeysMedia(0xB3, "MFFD")
"""``MFFD``"""
MEDIA_FAST_FORWARD = KeysMedia(0xB3, "MEDIA_FAST_FORWARD")
"""``MEDIA_FAST_FORWARD``"""

MRWD = KeysMedia(0xB4, "MRWD")
"""``MRWD``"""
MEDIA_REWIND = KeysMedia(0xB4, "MEDIA_REWIND")
"""``MEDIA_REWIND``"""

# fmt: off
__all__ = [
    "AUDIO_MUTE", "MUTE",
    "AUDIO_VOL_UP", "VOLU",
    "AUDIO_VOL_DOWN", "VOLD",
    "BRIGHTNESS_UP", "BRIU",
    "BRIGHTNESS_DOWN", "BRID",
    "MEDIA_NEXT_TRACK", "MNXT",
    "MEDIA_PREV_TRACK", "MPRV",
    "MEDIA_STOP", "MSTP",
    "MEDIA_PLAY_PAUSE", "MPLY",
    "MEDIA_EJECT", "EJCT",
    "MEDIA_FAST_FORWARD", "MFFD",
    "MEDIA_REWIND", "MRWD",
]
# fmt: on
