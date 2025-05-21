from adafruit_hid.keyboard import Keyboard

from mkx.keys_abstract import KeysAbstract


class SK(KeysAbstract):
    def __init__(self, key: KeysAbstract, defer_release=False, retap_cancel=True):
        self.key_name = "SK"
        self._key = key
        self._active = False
        self._defer_release = defer_release
        self._retap_cancel = retap_cancel
        self._pressed = False
        self._interrupted = False
        self._interrupted_key_down = False

    def on_press(self, keyboard: Keyboard, timestamp: int):
        if self._active and self._retap_cancel:
            self.clear(keyboard, timestamp)
        elif not self._active:
            self._key.on_press(keyboard, timestamp)
            self._active = True
            self._pressed = True
            self._interrupted = False
            self._interrupted_key_down = False

    def on_release(self, keyboard: Keyboard, timestamp: int):
        self._pressed = False
        if self._active and not self._defer_release:
            if self._interrupted and not self._interrupted_key_down:
                # Only release if the interrupting key is no longer pressed
                self.clear(keyboard, timestamp)

    def clear(self, keyboard: Keyboard, timestamp: int):
        if self._active:
            self._key.on_release(keyboard, timestamp)
            self._active = False
            self._pressed = False
            self._interrupted = False
            self._interrupted_key_down = False


class StickyKeyManager:
    def __init__(self):
        self._active_sticky_keys = []

    def register(self, key: KeysAbstract):
        if isinstance(key, SK) and key not in self._active_sticky_keys:
            self._active_sticky_keys.append(key)

    def clear_stickies(self, keyboard: Keyboard, timestamp: int):
        for sticky in self._active_sticky_keys:
            sticky.clear(keyboard, timestamp)
        self._active_sticky_keys.clear()
