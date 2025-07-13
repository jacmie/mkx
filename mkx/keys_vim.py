from mkx.keys_abstract import KeysAbstract
from mkx.keys_standard import *
from mkx.keys_modifiers import M_LCTL, M_LSFT
from mkx.keys_sequence import SEQ
from mkx.keys_layers import TO
from mkx.keys_tapdance import TD


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


# fmt: off

VI_HW = VI_HI_WO = VI_HIGLIGHT_WORD = VIM([
    M_LCTL(LEFT),
    M_LCTL(M_LSFT(RIGHT))
], "HIGL_W")

VI_HL = VI_HI_LI = VI_HIGLIGHT_LINE = VIM([
    HOME,
    HOME,
    M_LSFT(END)
], "HIGL_L")

VI_YE = VI_Y_WO = VI_YANK_WORD = SEQ([
    M_LCTL(LEFT),
    M_LCTL(M_LSFT(RIGHT)),
    M_LCTL(C),
    RIGHT
])

VI_YL = VI_Y_LI = VI_YANK_LINE = SEQ([
    HOME,
    M_LSFT(END),
    M_LCTL(C),
    RIGHT
])

VI_CW = VI_CUT_WO = VI_CUT_WORD = SEQ([
    VI_HI_WO,
    M_LCTL(X),
    RIGHT
])

VI_CL = VI_CUT_LI = VI_CUT_LINE = SEQ([
    VI_HI_LI,
    M_LCTL(X),
    BSPACE
])

VI_DW = VI_DEL_WO = VI_DEL_WORD = SEQ([
    VI_HI_WO,
    BSPACE,
    RIGHT
])

VI_DL = VI_DEL_LI = VI_DEL_LINE = SEQ([
    VI_HI_LI,
    BSPACE,
    BSPACE
])

####

VI_MINS = VI_PRVL = VI_PREV_LINE = VIM([
    UP,
    HOME,
], "VI_PRVL")

VI_MVLU = VI_MV_LINE_UP = VIM([
    END,
    M_LSFT(HOME),
    M_LSFT(HOME),
    M_LCTL(X),
    BACKSPACE,
    HOME,
    HOME,
    ENTER,
    UP,
    M_LCTL(V),
], "VI_MVLU")

VI_MVLD = VI_MV_LINE_DOWN = VIM([
    END,
    M_LSFT(HOME),
    M_LSFT(HOME),
    M_LCTL(X),
    BACKSPACE,
    DOWN,
    DOWN,
    HOME,
    HOME,
    ENTER,
    UP,
    M_LCTL(V),
], "VI_MVLD")

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

VI_D = VI_DEL = VI_DELATE = VIM_TD(DEL, VI_DEL_LINE, key_name="VI_DEL")

VI_F = VI_FIND = VIM([
    M_LCTL(F),
], "VI_FIND")

VI_X = VI_CUT = VIM_TD(M_LCTL(X), VI_CUT_LINE, key_name="VI_CUT")

__all__ = [
    "VIM", "VIM_L", "VIM_TD", "VIM_VIS",

    "VI_HW", "VI_HI_WO", "VI_HIGLIGHT_WORD",
    "VI_HL", "VI_HI_LI", "VI_HIGLIGHT_LINE",
    "VI_YW", "VI_Y_WO", "VI_YANK_WORD",
    "VI_YL", "VI_Y_LI", "VI_YANK_LINE",
    "VI_CW", "VI_CUT_WO", "VI_CUT_WORD",
    "VI_CL", "VI_CUT_LI", "VI_CUT_LINE",
    "VI_DW", "VI_DEL_WO", "VI_DEL_WORD",
    "VI_DL", "VI_DEL_LI", "VI_DEL_LINE",

    "VI_MINS", "VI_PRVL", "VI_PREV_LINE",
    "VI_PLUS", "VI_NXTL", "VI_NEXT_LINE",
    "VI_MVLU", "VI_MV_LINE_UP",
    "VI_MVLD", "VI_MV_LINE_DOWN",

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
    "VI_X", "VI_CUT",
    "VI_F", "VI_FIND",
]

# fmt: on
