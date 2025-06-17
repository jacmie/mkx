from adafruit_hid.keyboard import Keyboard

from mkx.keys_abstract import KeysAbstract
from mkx.manager_layers import LayersManager


class SEQ(KeysAbstract):
    def __init__(self, key_list: list[KeysAbstract]):
        super().__init__()
        self._key_list = key_list
        self.key_name = "SEQ(keys[])"

    def on_press(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        for key in self._key_list:
            key.on_press(layer_manager, keyboard, timestamp)
            key.on_release(layer_manager, keyboard, timestamp)

    def on_release(self, _, __, ___):
        pass
