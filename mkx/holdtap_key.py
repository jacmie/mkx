from key_base import AbstractKey


class HoldTapKey(AbstractKey):
    def __init__(self, position, tap_keycode, hold_keycode, timeout=200):
        super().__init__(position)
        self.tap_keycode = tap_keycode
        self.hold_keycode = hold_keycode
        self.timeout = timeout
        self._pressed_time = None
        self._hold_sent = False

    def on_press(self, keyboard, timestamp):
        self._pressed_time = timestamp
        self._hold_sent = False
        # You might delay action here until you know if it's a tap or hold

    def on_release(self, keyboard, timestamp):
        duration = timestamp - self._pressed_time
        if duration < self.timeout and not self._hold_sent:
            keyboard.send(self.tap_keycode)
        else:
            keyboard.release(self.hold_keycode)

    def maybe_check_hold(self, keyboard, timestamp):
        if not self._hold_sent and (timestamp - self._pressed_time >= self.timeout):
            keyboard.send(self.hold_keycode)
            self._hold_sent = True


# HT_ESC_CTRL = lambda pos: HoldTapKey(pos, Keycode.ESCAPE, Keycode.LEFT_CONTROL)
# keymap = [[A, HT_ESC_CTRL, B]]
