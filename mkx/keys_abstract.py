from adafruit_hid.keyboard import Keyboard

from mkx.manager_layers import LayersManager


class KeysAbstract:
    """
    Abstract base class for all key types.
    Subclasses must implement `on_press` and `on_release`.
    """

    def __init__(self):
        self._is_pressed = False

    def press(self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int):
        if not self._is_pressed:
            self._is_pressed = True
            self.on_press(layer_manager, keyboard, timestamp)

    def release(self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int):
        if self._is_pressed:
            self._is_pressed = False
            self.on_release(layer_manager, keyboard, timestamp)

    def on_press(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        raise NotImplementedError(
            "Subclass of the KeysAbstract must implement on_press()"
        )

    def on_release(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        raise NotImplementedError(
            "Subclass of the KeysAbstract must implement on_release()"
        )
