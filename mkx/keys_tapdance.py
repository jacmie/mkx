from adafruit_hid.keyboard import Keyboard

from mkx.keys_abstract import KeysAbstract
from mkx.timed_keys import TimedKeys


class TD(KeysAbstract, TimedKeys):
    def __init__(self, *keys: KeysAbstract, timeout=200):
        KeysAbstract.__init__(self)
        TimedKeys.__init__(self)
        self.key_name = "TD"
        self._keys = list(keys)
        self._timeout = timeout
        self._tap_count = 0
        self._last_timestamp = 0

    def on_press(self, _, __, timestamp: int):
        if (timestamp - self._last_timestamp) > self._timeout:
            self._tap_count = 0  # Reset tap count on timeout

        self._tap_count += 1
        self._last_timestamp = timestamp
        self.start_timer(timestamp)

    def on_release(self, _, __, ___):
        # Wait until timeout to act (handled in check_time)
        pass

    def check_time(self, keyboard: Keyboard, timestamp: int):
        if self._pressed_time is None:
            return

        if (timestamp - self._pressed_time) >= self._timeout:
            if self._tap_count <= len(self._keys):
                selected_key = self._keys[self._tap_count - 1]
                selected_key.on_press(keyboard, timestamp)
                selected_key.on_release(keyboard, timestamp)
            else:
                print("TapDance: tap count exceeds defined keys")

            self._tap_count = 0
            self.stop_timer()


# TD_D = TD(D, DEL, timeout=150)
