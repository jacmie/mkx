class KeysAbstract:
    """
    Abstract base class for all key types.
    Subclasses must implement `on_press` and `on_release`.
    """

    def __init__(self):
        self._is_pressed = False

    def press(self, keyboard):
        if not self._is_pressed:
            self._is_pressed = True
            self.on_press(keyboard)

    def release(self, keyboard, timestamp):
        if self._is_pressed:
            self._is_pressed = False
            self.on_release(keyboard, timestamp)

    # @abstractmethod
    def on_press(self, keyboard, timestamp):
        pass

    # @abstractmethod
    def on_release(self, keyboard, timestamp):
        pass
