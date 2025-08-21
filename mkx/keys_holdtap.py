from adafruit_hid.keyboard import Keyboard

from mkx.keys_abstract import KeysAbstract
from mkx.timed_keys import TimedKeys
from mkx.manager_layers import LayersManager


class HT(KeysAbstract, TimedKeys):
    def __init__(self, tap_key: KeysAbstract, hold_key: KeysAbstract, timeout=200):
        KeysAbstract.__init__(self)
        TimedKeys.__init__(self)
        self.key_name = "HT"
        self._tap_key = tap_key
        self._hold_key = hold_key
        self._timeout = timeout

        self._held_past_timeout = False
        self._hold_sent = False

    def on_press(self, _, __, timestamp: int):
        self._held_past_timeout = False
        self._hold_sent = False
        self.start_timer(timestamp)

    def on_release(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        if self._pressed_time is None:
            print("HT.on_release called without valid press time!")
            return

        duration = timestamp - self._pressed_time

        if self._held_past_timeout:
            if self._hold_sent:
                self._hold_key.on_release(layer_manager, keyboard, timestamp)
            else:
                print("HT: hold timeout passed but hold was not sent!")
        else:
            duration = timestamp - self._pressed_time
            if duration < self._timeout:
                self._tap_key.on_press(layer_manager, keyboard, timestamp)
                self._tap_key.on_release(layer_manager, keyboard, timestamp)
            else:
                print("HT: tap too late, ignoring!")

        self.stop_timer()

    def check_time(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        if self._pressed_time is None:
            return

        if not self._held_past_timeout and (
            timestamp - self._pressed_time >= self._timeout
        ):
            self._hold_key.on_press(layer_manager, keyboard, timestamp)
            self._held_past_timeout = True
            self._hold_sent = True
