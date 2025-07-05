from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.consumer_control_code import ConsumerControlCode

from mkx.keys_abstract import KeysAbstract


class KeysMedia(KeysAbstract):
    """
    A media key that sends a Consumer Control code using Adafruit HID library.
    """

    def __init__(self, media_code: ConsumerControlCode, key_name: str):
        super().__init__()
        self.media_code = media_code
        self.key_name = key_name
        self._cc = None  # Lazy init

    def _ensure_cc(self):
        if self._cc is None:
            import usb_hid

            self._cc = ConsumerControl(usb_hid.devices)

    def on_press(self, _, __, ___):
        self._ensure_cc()
        self._cc.send(self.media_code)

    def on_release(self, _, __, ___):
        pass


# Media key definitions

PLAY_PAUSE = KeysMedia(ConsumerControlCode.PLAY_PAUSE, "PLAY/PAUSE")
STOP = KeysMedia(ConsumerControlCode.STOP, "STOP")

MUTE = KeysMedia(ConsumerControlCode.MUTE, "MUTE")
"""``MUTE``"""
AUDIO_MUTE = KeysMedia(ConsumerControlCode.MUTE, "AUDIO_MUTE")
"""``AUDIO_MUTE``"""

VOLU = KeysMedia(ConsumerControlCode.VOLUME_INCREMENT, "VOLU")
"""``VOLU``"""
AUDIO_VOL_UP = KeysMedia(ConsumerControlCode.VOLUME_INCREMENT, "AUDIO_VOL_UP")
"""``AUDIO_VOL_UP``"""
VOLUME_INCREMENT = KeysMedia(ConsumerControlCode.VOLUME_INCREMENT, "VOLUME_INCREMENT")
"""``VOLUME_INCREMENT``"""

VOLD = KeysMedia(ConsumerControlCode.VOLUME_DECREMENT, "VOLD")
"""``VOLD``"""
AUDIO_VOL_DOWN = KeysMedia(ConsumerControlCode.VOLUME_DECREMENT, "AUDIO_VOL_DOWN")
"""``AUDIO_VOL_DOWN``"""
VOLUME_DECREMENT = KeysMedia(ConsumerControlCode.VOLUME_DECREMENT, "VOLUME_DECREMENT")
"""``VOLUME_DECREMENT``"""

BRIU = KeysMedia(ConsumerControlCode.BRIGHTNESS_INCREMENT, "BRIU")
"""``BRIU``"""
BRIGHTNESS_UP = KeysMedia(ConsumerControlCode.BRIGHTNESS_INCREMENT, "BRIGHTNESS_UP")
"""``BRIGHTNESS_UP``"""
BRIGHTNESS_INCREMENT = KeysMedia(
    ConsumerControlCode.BRIGHTNESS_INCREMENT, "BRIGHTNESS_INCREMENT"
)
"""``BRIGHTNESS_INCREMENT``"""

BRID = KeysMedia(ConsumerControlCode.BRIGHTNESS_DECREMENT, "BRID")
"""``BRID``"""
BRIGHTNESS_DOWN = KeysMedia(ConsumerControlCode.BRIGHTNESS_DECREMENT, "BRIGHTNESS_DOWN")
"""``BRIGHTNESS_DOWN``"""
BRIGHTNESS_DECREMENT = KeysMedia(
    ConsumerControlCode.BRIGHTNESS_DECREMENT, "BRIGHTNESS_DECREMENT"
)
"""``BRIGHTNESS_DECREMENT``"""

MNXT = KeysMedia(ConsumerControlCode.SCAN_NEXT_TRACK, "MNXT")
"""``MNXT``"""
MEDIA_NEXT_TRACK = KeysMedia(ConsumerControlCode.SCAN_NEXT_TRACK, "MEDIA_NEXT_TRACK")
"""``MEDIA_NEXT_TRACK``"""
SCAN_NEXT_TRACK = KeysMedia(ConsumerControlCode.SCAN_NEXT_TRACK, "SCAN_NEXT_TRACK")
"""``SCAN_NEXT_TRACK``"""

MPRV = KeysMedia(ConsumerControlCode.SCAN_PREVIOUS_TRACK, "MPRV")
"""``MPRV``"""
MEDIA_PREV_TRACK = KeysMedia(
    ConsumerControlCode.SCAN_PREVIOUS_TRACK, "MEDIA_PREV_TRACK"
)
"""``MEDIA_PREV_TRACK``"""
SCAN_PREVIOUS_TRACK = KeysMedia(
    ConsumerControlCode.SCAN_PREVIOUS_TRACK, "SCAN_PREVIOUS_TRACK"
)
"""``SCAN_PREVIOUS_TRACK``"""

MSTP = KeysMedia(ConsumerControlCode.STOP, "MSTP")
"""``MSTP``"""
MEDIA_STOP = KeysMedia(ConsumerControlCode.STOP, "MEDIA_STOP")
"""``MEDIA_STOP``"""
STOP = KeysMedia(ConsumerControlCode.STOP, "STOP")
"""``STOP``"""

MPLY = KeysMedia(ConsumerControlCode.PLAY_PAUSE, "MPLY")
"""``MPLY``"""
MEDIA_PLAY_PAUSE = KeysMedia(ConsumerControlCode.PLAY_PAUSE, "MEDIA_PLAY_PAUSE")
"""``MEDIA_PLAY_PAUSE``"""
PLAY_PAUSE = KeysMedia(ConsumerControlCode.PLAY_PAUSE, "PLAY_PAUSE")
"""``PLAY_PAUSE``"""

EJCT = KeysMedia(ConsumerControlCode.EJECT, "EJCT")
"""``EJCT``"""
MEDIA_EJECT = KeysMedia(ConsumerControlCode.EJECT, "MEDIA_EJECT")
"""``MEDIA_EJECT``"""
EJECT = KeysMedia(ConsumerControlCode.EJECT, "EJECT")
"""``EJECT``"""

MFFD = KeysMedia(ConsumerControlCode.FAST_FORWARD, "MFFD")
"""``MFFD``"""
MEDIA_FAST_FORWARD = KeysMedia(ConsumerControlCode.FAST_FORWARD, "MEDIA_FAST_FORWARD")
"""``MEDIA_FAST_FORWARD``"""
FAST_FORWARD = KeysMedia(ConsumerControlCode.FAST_FORWARD, "FAST_FORWARD")
"""``FAST_FORWARD``"""

MRWD = KeysMedia(ConsumerControlCode.REWIND, "MRWD")
"""``MRWD``"""
MEDIA_REWIND = KeysMedia(ConsumerControlCode.REWIND, "MEDIA_REWIND")
"""``MEDIA_REWIND``"""
REWIND = KeysMedia(ConsumerControlCode.REWIND, "REWIND")
"""``REWIND``"""

MREC = KeysMedia(ConsumerControlCode.RECORD, "MREC")
"""``MRWD``"""
MEDIA_RECORD = KeysMedia(ConsumerControlCode.RECORD, "MEDIA_RECORD")
"""``MEDIA_RECORD``"""
RECORD = KeysMedia(ConsumerControlCode.RECORD, "RECORD")
"""``RECORD``"""

# fmt: off
__all__ = [
    "AUDIO_MUTE", "MUTE",
    "AUDIO_VOL_UP", "VOLU", "VOLUME_INCREMENT",
    "AUDIO_VOL_DOWN", "VOLD", "VOLUME_DECREMENT",
    "BRIGHTNESS_UP", "BRIU", "BRIGHTNESS_INCREMENT",
    "BRIGHTNESS_DOWN", "BRID", "BRIGHTNESS_DECREMENT",
    "MEDIA_NEXT_TRACK", "MNXT", "SCAN_NEXT_TRACK",
    "MEDIA_PREV_TRACK", "MPRV", "SCAN_PREVIOUS_TRACK",
    "MEDIA_STOP", "MSTP", "STOP",
    "MEDIA_PLAY_PAUSE", "MPLY", "PLAY_PAUSE",
    "MEDIA_EJECT", "EJCT", "EJECT",
    "MEDIA_FAST_FORWARD", "MFFD", "FAST_FORWARD",
    "MEDIA_REWIND", "MRWD", "REWIND",
    "MEDIA_RECORD", "MREC", "RECORD",
]
# fmt: on
