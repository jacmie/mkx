from adafruit_hid.keyboard import Keyboard

from mkx.keys_abstract import KeysAbstract


class TimedKeys:
    def __init__(self):
        self._active = False
        self._pressed_time = None

    def start_timer(self, timestamp: int):
        self._pressed_time = timestamp
        self._active = True

    def stop_timer(self):
        self._active = False
        self._pressed_time = None

    def check_time(self, keyboard: Keyboard, timestamp: int):
        """Called each frame while active."""
        raise NotImplementedError("Subclasses must implement check_time")


class TimedKeysManager:
    def __init__(self):
        self._active_keys = set()

    def register(self, key: KeysAbstract):
        if isinstance(key, TimedKeys):
            self._active_keys.add(key)

    def update(self, keyboard: Keyboard, timestamp: int):
        for key in list(self._active_keys):
            key.check_time(keyboard, timestamp)
            if not getattr(key, "_active", False):
                self._active_keys.remove(key)
