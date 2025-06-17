from adafruit_hid.keyboard import Keyboard

from mkx.keys_abstract import KeysAbstract
from mkx.keys_standard import LCTL, LSFT, LALT, LGUI, RCTL, RSFT, RALT, RGUI

from mkx.manager_layers import LayersManager


class MOD(KeysAbstract):
    def __init__(self, key_mod: KeysAbstract, key_code: KeysAbstract, key_name: str):
        super().__init__()
        self._key_mod = key_mod
        self._key_code = key_code
        self.key_name = key_name

    def on_press(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        self._key_mod.on_press(layer_manager, keyboard, timestamp)
        self._key_code.on_press(layer_manager, keyboard, timestamp)
        self._key_code.on_release(layer_manager, keyboard, timestamp)
        self._key_mod.on_release(layer_manager, keyboard, timestamp)

    def on_release(self, _, __, ___):
        pass


class M_LCTL(MOD):
    def __init__(self, key_code: KeysAbstract):
        super().__init__(LCTL, key_code, f"M_LCTL({key_code.key_name})")


class M_LSFT(MOD):
    def __init__(self, key_code: KeysAbstract):
        super().__init__(LSFT, key_code, f"M_LSFT({key_code.key_name})")


class M_LALT(MOD):
    def __init__(self, key_code: KeysAbstract):
        super().__init__(LALT, key_code, f"M_LALT({key_code.key_name})")


class M_LGUI(MOD):
    def __init__(self, key_code: KeysAbstract):
        super().__init__(LGUI, key_code, f"M_LGUI({key_code.key_name})")


class M_RCTL(MOD):
    def __init__(self, key_code: KeysAbstract):
        super().__init__(RCTL, key_code, f"M_RCTL({key_code.key_name})")


class M_RSFT(MOD):
    def __init__(self, key_code: KeysAbstract):
        super().__init__(RSFT, key_code, f"M_RSFT({key_code.key_name})")


class M_RALT(MOD):
    def __init__(self, key_code: KeysAbstract):
        super().__init__(RALT, key_code, f"M_RALT({key_code.key_name})")


class M_RGUI(MOD):
    def __init__(self, key_code: KeysAbstract):
        super().__init__(RGUI, key_code, f"M_RGUI({key_code.key_name})")
