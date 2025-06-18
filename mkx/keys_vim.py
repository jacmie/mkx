from adafruit_hid.keyboard import Keyboard

from mkx.keys_abstract import KeysAbstract
from mkx.keys_standard import *
from mkx.keys_modifiers import M_LCTL, M_LSFT
from mkx.keys_sequence import SEQ
from mkx.keys_layers import TO
from mkx.keys_tapdance import TD
from mkx.manager_layers import LayersManager


class VIM(SEQ):
    def __init__(self, key_list: list[KeysAbstract], key_name: str):
        super().__init__(key_list)
        self.key_name = key_name


class VIM_L(SEQ):
    def __init__(self, key_list: list[KeysAbstract], key_name: str):
        super().__init__([])
        self.key_name = key_name
        self.static_keys = key_list

    def L(self, layer):
        if layer is not None:
            self._key_list = self.static_keys + [TO(layer)]
        return self


class VIM_TD(TD):
    def __init__(self, *keys: KeysAbstract, key_name: str):
        super().__init__(*keys, timeout=200)
        self.key_name = key_name

    def T(self, timeout):
        self._timeout = timeout
        return self


class VIM_VIS(KeysAbstract):
    def __init__(self, press: bool, key_name: str):
        super().__init__()
        self.press = press
        self.key_name = key_name
        self.key_layer = None

    def L(self, layer):
        if layer is not None:
            self.key_layer = TO(layer)
        return self

    def on_press(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        if self.key_layer is not None:
            self.key_layer.on_press(layer_manager, keyboard, timestamp)
        else:
            return

        if self.press:
            LSHIFT.on_press(layer_manager, keyboard, timestamp)
        else:
            LSHIFT.on_release(layer_manager, keyboard, timestamp)

    def on_release(self, _, __, ___):
        pass


# fmt: off

VI_HI_WO = VI_HIGLIGHT_WORD = VIM([
    M_LCTL(LEFT),
    M_LCTL(M_LSFT(RIGHT))
], "HIGL_W")

VI_HI_LI = VI_HIGLIGHT_LINE = VIM([
    HOME,
    M_LSFT(END)
], "HIGL_L")

VI_Y_WO = VI_YANK_WORD = SEQ([
    M_LCTL(LEFT),
    M_LCTL(M_LSFT(RIGHT)),
    M_LCTL(C),
    RIGHT
])

VI_Y_LI = VI_YANK_LINE = SEQ([
    HOME,
    M_LSFT(END),
    M_LCTL(C),
    RIGHT
])

VI_CUT_WO = VI_CUT_WORD = SEQ([
    VI_HI_WO,
    M_LCTL(X),
    RIGHT
])

VI_CUT_LI = VI_CUT_LINE = SEQ([
    VI_HI_LI,
    M_LCTL(X)#,
    # RIGHT
])

####

VI_MINS = VI_PRVL = VI_PREV_LINE = VIM([
    UP,
    HOME,
], "VI_PRVL")

VI_PLUS = VI_NXTL = VI_NEXT_LINE = VIM([
    DOWN,
    HOME,
], "VI_NXTL")

VI_W = VI_NXTW = VI_NEXT_WORD = VIM([
    M_LCTL(RIGHT),
], "VI_NXTW")

VI_E = VI_PRVW = VI_PREV_WORD = VIM([
    M_LCTL(LEFT),
], "VI_PRVW")

VI_R = VI_REPL = VI_REPLACE = VIM_L([
    INS,
], "VI_REPL")

VI_R_ESC = VIM_L([
    INS,
], "VI_R_ESC")

VI_Y = VI_YANK = VIM([
    M_LCTL(C),
], "VI_YANK")

VI_U = VI_UNDO =  VIM([
    M_LCTL(Z),
], "VI_UNDO")

VI_I = VI_INS = VI_INSERT = VIM_L([
], "VI_INS")

VI_O = VI_OPEN = VIM_L([
    END,
    ENTER,
], "VI_OPEN")

VI_P = VI_PAST = VI_PASTE = VIM([
    M_LCTL(V),
], "VI_PAST")

VI_A = VI_APND = VI_APPEND = VIM_L([
], "VI_APND")

VI_S = VI_SUBS = VI_SUBSTITUTE = VIM_L([
    VI_CUT_LI,
], "VI_SUBS")

VI_D = VI_DEL = VI_DELATE = VIM_TD(DEL, VI_CUT_LINE, key_name="VI_DEL")

VI_F = VI_FIND = VIM([
    M_LCTL(F),
], "VI_FIND")

VI_V = VI_VIS = VI_VISUAL = VIM_VIS(True, "VI_VIS")

VI_V_ESC = VIM_VIS(False, "VI_V_ESC")

__all__ = [
    "VIM", "VIM_L", "VIM_TD", "VIM_VIS",

    "VI_HI_WO", "VI_HIGLIGHT_WORD",
    "VI_HI_LI", "VI_HIGLIGHT_LINE",
    "VI_Y_WO", "VI_YANK_WORD",
    "VI_Y_LI", "VI_YANK_LINE",
    "VI_CUT_WO", "VI_CUT_WORD",
    "VI_CUT_LI", "VI_CUT_LINE",


    "VI_MINS", "VI_PRVL", "VI_PREV_LINE",
    "VI_PLUS", "VI_NXTL", "VI_NEXT_LINE",

    "VI_W", "VI_NXTW", "VI_NEXT_WORD",
    "VI_E", "VI_PRVW", "VI_PREV_WORD",

    "VI_R", "VI_REPL", "VI_REPLACE",
    "VI_R_ESC",

    "VI_Y", "VI_YANK",
    "VI_U", "VI_UNDO",
    "VI_I", "VI_INS", "VI_INSERT",
    "VI_O", "VI_OPEN",
    "VI_P", "VI_PAST", "VI_PASTE",

    "VI_A", "VI_APND", "VI_APPEND",
    "VI_S", "VI_SUBS", "VI_SUBSTITUTE",
    "VI_D", "VI_DEL", "VI_DELATE",
    "VI_F", "VI_FIND",

    "VI_V", "VI_VIS", "VI_VISUAL",
    "VI_V_ESC",
]

# fmt: on
