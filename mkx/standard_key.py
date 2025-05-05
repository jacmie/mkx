from key_base import AbstractKey


class StandardKey(AbstractKey):
    def __init__(self, position, keycode):
        super().__init__(position)
        self.keycode = keycode

    def on_press(self, keyboard, timestamp):
        keyboard.press(self.keycode)

    def on_release(self, keyboard, timestamp):
        keyboard.release(self.keycode)
