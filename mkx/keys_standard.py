from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from mkx.keys_abstract import KeysAbstract


class KeysStandard(KeysAbstract):
    """
    A standard key that sends a HID keycode using Adafruit HID library.
    """

    def __init__(self, key_code: Keycode, key_name: str):
        super().__init__()
        self.key_code = key_code
        self.key_name = key_name

    def on_press(self, keyboard: Keyboard, _):
        keyboard.press(self.key_code)

    def on_release(self, keyboard: Keyboard, _):
        keyboard.release(self.key_code)


# Standard key definitions

NO = KeysStandard(None, "None")
"""None key"""
XXXXXXX = KeysStandard(None, "XXXXXXX")
"""None key"""

# TRANSPARENT', 'TRNS' not implemented

A = KeysStandard(Keycode.A, "A")
"""``a`` and ``A``"""
B = KeysStandard(Keycode.B, "B")
"""``b`` and ``B``"""
C = KeysStandard(Keycode.C, "C")
"""``c`` and ``C``"""
D = KeysStandard(Keycode.D, "D")
"""``d`` and ``D``"""
E = KeysStandard(Keycode.E, "E")
"""``e`` and ``E``"""
F = KeysStandard(Keycode.F, "F")
"""``f`` and ``F``"""
G = KeysStandard(Keycode.G, "G")
"""``g`` and ``G``"""
H = KeysStandard(Keycode.H, "H")
"""``h`` and ``H``"""
I = KeysStandard(Keycode.I, "I")
"""``i`` and ``I``"""
J = KeysStandard(Keycode.J, "J")
"""``j`` and ``J``"""
K = KeysStandard(Keycode.K, "K")
"""``k`` and ``K``"""
L = KeysStandard(Keycode.L, "L")
"""``l`` and ``L``"""
M = KeysStandard(Keycode.M, "M")
"""``m`` and ``M``"""
N = KeysStandard(Keycode.N, "N")
"""``n`` and ``N``"""
O = KeysStandard(Keycode.O, "O")
"""``o`` and ``O``"""
P = KeysStandard(Keycode.P, "P")
"""``p`` and ``P``"""
Q = KeysStandard(Keycode.Q, "Q")
"""``q`` and ``Q``"""
R = KeysStandard(Keycode.R, "R")
"""``r`` and ``R``"""
S = KeysStandard(Keycode.S, "S")
"""``s`` and ``S``"""
T = KeysStandard(Keycode.T, "T")
"""``t`` and ``T``"""
U = KeysStandard(Keycode.U, "U")
"""``u`` and ``U``"""
V = KeysStandard(Keycode.V, "V")
"""``v`` and ``V``"""
W = KeysStandard(Keycode.W, "W")
"""``w`` and ``W``"""
X = KeysStandard(Keycode.X, "X")
"""``x`` and ``X``"""
Y = KeysStandard(Keycode.Y, "Y")
"""``y`` and ``Y``"""
Z = KeysStandard(Keycode.Z, "Z")
"""``z`` and ``Z```"""

ONE = KeysStandard(Keycode.ONE, "ONE")
"""``1`` and ``!``"""
N1 = KeysStandard(Keycode.ONE, "N1")
"""``1`` and ``!``"""
TWO = KeysStandard(Keycode.TWO, "TWO")
"""``2`` and ``@``"""
N2 = KeysStandard(Keycode.TWO, "N2")
"""``2`` and ``@``"""
THREE = KeysStandard(Keycode.THREE, "THREE")
"""``3`` and ``#``"""
N3 = KeysStandard(Keycode.THREE, "N3")
"""``3`` and ``#``"""
FOUR = KeysStandard(Keycode.FOUR, "FOUR")
"""``4`` and ``$``"""
N4 = KeysStandard(Keycode.FOUR, "N4")
"""``4`` and ``$``"""
FIVE = KeysStandard(Keycode.FIVE, "FIVE")
"""``5`` and ``%``"""
N5 = KeysStandard(Keycode.FIVE, "N5")
"""``5`` and ``%``"""
SIX = KeysStandard(Keycode.SIX, "SIX")
"""``6`` and ``^``"""
N6 = KeysStandard(Keycode.SIX, "N6")
"""``6`` and ``^``"""
SEVEN = KeysStandard(Keycode.SEVEN, "SEVEN")
"""``7`` and ``&``"""
N7 = KeysStandard(Keycode.SEVEN, "N7")
"""``7`` and ``&``"""
EIGHT = KeysStandard(Keycode.EIGHT, "EIGHT")
"""``8`` and ``*``"""
N8 = KeysStandard(Keycode.EIGHT, "N8")
"""``8`` and ``*``"""
NINE = KeysStandard(Keycode.NINE, "NINE")
"""``9`` and ``(``"""
N9 = KeysStandard(Keycode.NINE, "N9")
"""``9`` and ``(``"""
ZERO = KeysStandard(Keycode.ZERO, "ZERO")
"""``0`` and ``)``"""
N0 = KeysStandard(Keycode.ZERO, "N0")
"""``0`` and ``)``"""

ENTER = KeysStandard(Keycode.ENTER, "ENTER")
"""Enter (Return)"""
RETURN = KeysStandard(Keycode.ENTER, "RETURN")
"""Enter (Return)"""
ENT = KeysStandard(Keycode.ENTER, "ENT")
"""Enter (Return)"""

ESCAPE = KeysStandard(Keycode.ESCAPE, "ESCAPE")
"""Escape"""
ESC = KeysStandard(Keycode.ESCAPE, "ESC")
"""Escape"""

BACKSPACE = KeysStandard(Keycode.BACKSPACE, "BACKSPACE")
"""Delete backward (Backspace)"""
BSPACE = KeysStandard(Keycode.BACKSPACE, "BSPACE")
"""Delete backward (Backspace)"""
BSPC = KeysStandard(Keycode.BACKSPACE, "BSPC")
"""Delete backward (Backspace)"""

TAB = KeysStandard(Keycode.TAB, "TAB")
"""Tab and Backtab"""

SPACEBAR = KeysStandard(Keycode.SPACEBAR, "SPACEBAR")
"""Spacebar"""
SPACE = KeysStandard(Keycode.SPACEBAR, "SPACE")
"""Spacebar"""
SPC = KeysStandard(Keycode.SPACEBAR, "SPC")
"""Spacebar"""

MINUS = KeysStandard(Keycode.MINUS, "MINUS")
"""``-`` and ``_``"""
MINS = KeysStandard(Keycode.MINUS, "MINS")
"""``-`` and ``_``"""

EQUALS = KeysStandard(Keycode.EQUALS, "EQUALS")
"""``=`` and ``+``"""
EQUAL = KeysStandard(Keycode.EQUALS, "EQUAL")
"""``=`` and ``+``"""
EQL = KeysStandard(Keycode.EQUALS, "EQL")
"""``=`` and ``+``"""

LEFT_BRACKET = KeysStandard(Keycode.LEFT_BRACKET, "LEFT_BRACKET")
"""``[`` and ``{``"""
LBRACKET = KeysStandard(Keycode.LEFT_BRACKET, "LBRACKET")
"""``[`` and ``{``"""
LBRC = KeysStandard(Keycode.LEFT_BRACKET, "LBRC")
"""``[`` and ``{``"""

RIGHT_BRACKET = KeysStandard(Keycode.RIGHT_BRACKET, "RIGHT_BRACKET")
"""``]`` and ``}``"""
RBRACKET = KeysStandard(Keycode.RIGHT_BRACKET, "RBRACKET")
"""``]`` and ``}``"""
RBRC = KeysStandard(Keycode.RIGHT_BRACKET, "RBRC")
"""``]`` and ``}``"""

BACKSLASH = KeysStandard(Keycode.BACKSLASH, "BACKSLASH")
r"""``\` and `|``"""
BSLASH = KeysStandard(Keycode.BACKSLASH, "BSLASH")
r"""``\` and `|``"""
BSLS = KeysStandard(Keycode.BACKSLASH, "BSLS")
r"""``\` and `|``"""

POUND = KeysStandard(Keycode.POUND, "POUND")
"""``#`` and ``~`` (Non-US keyboard)"""

SEMICOLON = KeysStandard(Keycode.SEMICOLON, "SEMICOLON")
"""``;`` and ``:``"""
SCOLON = KeysStandard(Keycode.SEMICOLON, "SCOLON")
"""``;`` and ``:``"""
SCLN = KeysStandard(Keycode.SEMICOLON, "SCLN")
"""``;`` and ``:``"""

QUOTE = KeysStandard(Keycode.QUOTE, "QUOTE")
"""``'`` and ``"``"""
QUOT = KeysStandard(Keycode.QUOTE, "QUOT")
"""``'`` and ``"``"""

GRAVE_ACCENT = KeysStandard(Keycode.GRAVE_ACCENT, "GRAVE_ACCENT")
r""":literal:``\`` and ``~``"""
GRAVE = KeysStandard(Keycode.GRAVE_ACCENT, "GRAVE")
r""":literal:``\`` and ``~``"""
GRV = KeysStandard(Keycode.GRAVE_ACCENT, "GRV")
r""":literal:``\`` and ``~``"""
ZKHK = KeysStandard(Keycode.GRAVE_ACCENT, "ZKHK")
r""":literal:``\`` and ``~``"""

COMMA = KeysStandard(Keycode.COMMA, "COMMA")
"""``,`` and ``<``"""
COMM = KeysStandard(Keycode.COMMA, "COMM")
"""``,`` and ``<``"""

PERIOD = KeysStandard(Keycode.PERIOD, "PERIOD")
"""``.`` and ``>``"""
DOT = KeysStandard(Keycode.PERIOD, "DOT")
"""``.`` and ``>``"""

FORWARD_SLASH = KeysStandard(Keycode.FORWARD_SLASH, "FORWARD_SLASH")
"""``/`` and ``?``"""
SLASH = KeysStandard(Keycode.FORWARD_SLASH, "SLASH")
"""``/`` and ``?``"""
SLSH = KeysStandard(Keycode.FORWARD_SLASH, "SLSH")
"""``/`` and ``?``"""

CAPS_LOCK = KeysStandard(Keycode.CAPS_LOCK, "CAPS_LOCK")
"""Caps Lock"""
CAPSLOCK = KeysStandard(Keycode.CAPS_LOCK, "CAPSLOCK")
"""Caps Lock"""
CAPS = KeysStandard(Keycode.CAPS_LOCK, "CAPS")
"""Caps Lock"""
CLCK = KeysStandard(Keycode.CAPS_LOCK, "CLCK")
"""Caps Lock"""

F1 = KeysStandard(Keycode.F1, "F1")
"""Function key F1"""
F2 = KeysStandard(Keycode.F2, "F2")
"""Function key F2"""
F3 = KeysStandard(Keycode.F3, "F3")
"""Function key F3"""
F4 = KeysStandard(Keycode.F4, "F4")
"""Function key F4"""
F5 = KeysStandard(Keycode.F5, "F5")
"""Function key F5"""
F6 = KeysStandard(Keycode.F6, "F6")
"""Function key F6"""
F7 = KeysStandard(Keycode.F7, "F7")
"""Function key F7"""
F8 = KeysStandard(Keycode.F8, "F8")
"""Function key F8"""
F9 = KeysStandard(Keycode.F9, "F9")
"""Function key F9"""
F10 = KeysStandard(Keycode.F10, "F10")
"""Function key F10"""
F11 = KeysStandard(Keycode.F11, "F11")
"""Function key F11"""
F12 = KeysStandard(Keycode.F12, "F12")
"""Function key F12"""

PRINT_SCREEN = KeysStandard(Keycode.PRINT_SCREEN, "PRINT_SCREEN")
"""Print Screen (SysRq)"""
PSCREEN = KeysStandard(Keycode.PRINT_SCREEN, "PSCREEN")
"""Print Screen (SysRq)"""
PSCR = KeysStandard(Keycode.PRINT_SCREEN, "PSCR")
"""Print Screen (SysRq)"""

SCROLL_LOCK = KeysStandard(Keycode.SCROLL_LOCK, "SCROLL_LOCK")
"""Scroll Lock"""
SCROLLLOCK = KeysStandard(Keycode.SCROLL_LOCK, "SCROLLLOCK")
"""Scroll Lock"""
SLCK = KeysStandard(Keycode.SCROLL_LOCK, "SLCK")
"""Scroll Lock"""

PAUSE = KeysStandard(Keycode.PAUSE, "PAUSE")
"""Pause (Break)"""
PAUS = KeysStandard(Keycode.PAUSE, "PAUS")
"""Pause (Break)"""
BRK = KeysStandard(Keycode.PAUSE, "BRK")
"""Pause (Break)"""

INSERT = KeysStandard(Keycode.INSERT, "INSERT")
"""Insert"""
INS = KeysStandard(Keycode.INSERT, "INS")
"""Insert"""

HOME = KeysStandard(Keycode.HOME, "HOME")
"""Home (often moves to beginning of line)"""

PAGE_UP = KeysStandard(Keycode.PAGE_UP, "PAGE_UP")
"""Go back one page"""
PGUP = KeysStandard(Keycode.PAGE_UP, "PGUP")
"""Go back one page"""

DELETE = KeysStandard(Keycode.DELETE, "DELETE")
"""Delete forward"""
DEL = KeysStandard(Keycode.DELETE, "DEL")
"""Delete forward"""

END = KeysStandard(Keycode.END, "END")
"""End (often moves to end of line)"""

PAGE_DOWN = KeysStandard(Keycode.PAGE_DOWN, "PAGE_DOWN")
"""Go forward one page"""
PGDN = KeysStandard(Keycode.PAGE_DOWN, "PGDN")
"""Page Down"""

RIGHT_ARROW = KeysStandard(Keycode.RIGHT_ARROW, "RIGHT_ARROW")
"""Move the cursor right"""
RIGHT = KeysStandard(Keycode.RIGHT_ARROW, "RIGHT")
"""Move the cursor right"""
RGHT = KeysStandard(Keycode.RIGHT_ARROW, "RGHT")
"""Move the cursor right"""

LEFT_ARROW = KeysStandard(Keycode.LEFT_ARROW, "LEFT_ARROW")
"""Move the cursor left"""
LEFT = KeysStandard(Keycode.LEFT_ARROW, "LEFT")
"""Move the cursor left"""

DOWN_ARROW = KeysStandard(Keycode.DOWN_ARROW, "DOWN_ARROW")
"""Move the cursor down"""
DOWN = KeysStandard(Keycode.DOWN_ARROW, "DOWN")
"""Move the cursor down"""

UP_ARROW = KeysStandard(Keycode.UP_ARROW, "UP_ARROW")
"""Move the cursor up"""
UP = KeysStandard(Keycode.UP_ARROW, "UP")
"""Move the cursor up"""

KEYPAD_NUMLOCK = KeysStandard(Keycode.KEYPAD_NUMLOCK, "KEYPAD_NUMLOCK")
"""Num Lock (Clear on Mac)"""
NUMLOCK = KeysStandard(Keycode.KEYPAD_NUMLOCK, "NUMLOCK")
"""Num Lock (Clear on Mac)"""
NLCK = KeysStandard(Keycode.KEYPAD_NUMLOCK, "NLCK")
"""Num Lock (Clear on Mac)"""

KEYPAD_FORWARD_SLASH = KeysStandard(
    Keycode.KEYPAD_FORWARD_SLASH, "KEYPAD_FORWARD_SLASH"
)
"""Keypad ``/``"""
KP_SLASH = KeysStandard(Keycode.KEYPAD_FORWARD_SLASH, "KP_SLASH")
"""Keypad ``/``"""
PSLS = KeysStandard(Keycode.KEYPAD_FORWARD_SLASH, "PSLS")
"""Keypad ``/``"""

KEYPAD_ASTERISK = KeysStandard(Keycode.KEYPAD_ASTERISK, "KEYPAD_ASTERISK")
"""Keypad ``*``"""
KP_ASTERISK = KeysStandard(Keycode.KEYPAD_ASTERISK, "KP_ASTERISK")
"""Keypad ``*``"""
PAST = KeysStandard(Keycode.KEYPAD_ASTERISK, "PAST")
"""Keypad ``*``"""

KEYPAD_MINUS = KeysStandard(Keycode.KEYPAD_MINUS, "KEYPAD_MINUS")
"""Keypad ``-``"""
KP_MINUS = KeysStandard(Keycode.KEYPAD_MINUS, "KP_MINUS")
"""Keypad ``-``"""
PMNS = KeysStandard(Keycode.KEYPAD_MINUS, "PMNS")
"""Keypad ``-``"""

KEYPAD_PLUS = KeysStandard(Keycode.KEYPAD_PLUS, "KEYPAD_PLUS")
"""Keypad ``+``"""
KP_PLUS = KeysStandard(Keycode.KEYPAD_PLUS, "KP_PLUS")
"""Keypad ``+``"""
PPLS = KeysStandard(Keycode.KEYPAD_PLUS, "PPLS")
"""Keypad ``+``"""

KEYPAD_ENTER = KeysStandard(Keycode.KEYPAD_ENTER, "KEYPAD_ENTER")
"""Keypad Enter"""
KP_ENTER = KeysStandard(Keycode.KEYPAD_ENTER, "KP_ENTER")
"""Keypad Enter"""
PENT = KeysStandard(Keycode.KEYPAD_ENTER, "PENT")
"""Keypad Enter"""

KEYPAD_ONE = KeysStandard(Keycode.KEYPAD_ONE, "KEYPAD_ONE")
"""Keypad ``1`` and End"""
KP_1 = KeysStandard(Keycode.KEYPAD_ONE, "KP_1")
"""Keypad ``1`` and End"""
P1 = KeysStandard(Keycode.KEYPAD_ONE, "P1")
"""Keypad ``1`` and End"""
KEYPAD_TWO = KeysStandard(Keycode.KEYPAD_TWO, "KEYPAD_TWO")
"""Keypad ``2`` and Down Arrow"""
KP_2 = KeysStandard(Keycode.KEYPAD_TWO, "KP_2")
"""Keypad ``2`` and Down Arrow"""
P2 = KeysStandard(Keycode.KEYPAD_TWO, "P2")
"""Keypad ``2`` and Down Arrow"""
KEYPAD_THREE = KeysStandard(Keycode.KEYPAD_THREE, "KEYPAD_THREE")
"""Keypad ``3`` and PgDn"""
KP_3 = KeysStandard(Keycode.KEYPAD_THREE, "KP_3")
"""Keypad ``3`` and PgDn"""
P3 = KeysStandard(Keycode.KEYPAD_THREE, "P3")
"""Keypad ``3`` and PgDn"""
KEYPAD_FOUR = KeysStandard(Keycode.KEYPAD_FOUR, "KEYPAD_FOUR")
"""Keypad ``4`` and Left Arrow"""
KP_4 = KeysStandard(Keycode.KEYPAD_FOUR, "KP_4")
"""Keypad ``4`` and Left Arrow"""
P4 = KeysStandard(Keycode.KEYPAD_FOUR, "P4")
"""Keypad ``4`` and Left Arrow"""
KEYPAD_FIVE = KeysStandard(Keycode.KEYPAD_FIVE, "KEYPAD_FIVE")
"""Keypad ``5``"""
KP_5 = KeysStandard(Keycode.KEYPAD_FIVE, "KP_5")
"""Keypad ``5``"""
P5 = KeysStandard(Keycode.KEYPAD_FIVE, "P5")
"""Keypad ``5``"""
KEYPAD_SIX = KeysStandard(Keycode.KEYPAD_SIX, "KEYPAD_SIX")
"""Keypad ``6`` and Right Arrow"""
KP_6 = KeysStandard(Keycode.KEYPAD_SIX, "KP_6")
"""Keypad ``6`` and Right Arrow"""
P6 = KeysStandard(Keycode.KEYPAD_SIX, "P6")
"""Keypad ``6`` and Right Arrow"""
KEYPAD_SEVEN = KeysStandard(Keycode.KEYPAD_SEVEN, "KEYPAD_SEVEN")
"""Keypad ``7`` and Home"""
KP_7 = KeysStandard(Keycode.KEYPAD_SEVEN, "KP_7")
"""Keypad ``7`` and Home"""
P7 = KeysStandard(Keycode.KEYPAD_SEVEN, "P7")
"""Keypad ``7`` and Home"""
KEYPAD_EIGHT = KeysStandard(Keycode.KEYPAD_EIGHT, "KEYPAD_EIGHT")
"""Keypad ``8`` and Up Arrow"""
KP_8 = KeysStandard(Keycode.KEYPAD_EIGHT, "KP_8")
"""Keypad ``8`` and Up Arrow"""
P8 = KeysStandard(Keycode.KEYPAD_EIGHT, "P8")
"""Keypad ``8`` and Up Arrow"""
KEYPAD_NINE = KeysStandard(Keycode.KEYPAD_NINE, "KEYPAD_NINE")
"""Keypad ``9`` and PgUp"""
KP_9 = KeysStandard(Keycode.KEYPAD_NINE, "KP_9")
"""Keypad ``9`` and PgUp"""
P9 = KeysStandard(Keycode.KEYPAD_NINE, "P9")
"""Keypad ``9`` and PgUp"""
KEYPAD_ZERO = KeysStandard(Keycode.KEYPAD_ZERO, "KEYPAD_ZERO")
"""Keypad ``0`` and Ins"""
KP_0 = KeysStandard(Keycode.KEYPAD_ZERO, "KP_0")
"""Keypad ``0`` and Ins"""
P0 = KeysStandard(Keycode.KEYPAD_ZERO, "P0")
"""Keypad ``0`` and Ins"""

KEYPAD_PERIOD = KeysStandard(Keycode.KEYPAD_PERIOD, "KEYPAD_PERIOD")
"""Keypad ``.`` and Del"""
KP_DOT = KeysStandard(Keycode.KEYPAD_PERIOD, "KP_DOT")
"""Keypad ``.`` and Del"""
PDOT = KeysStandard(Keycode.KEYPAD_PERIOD, "PDOT")
"""Keypad ``.`` and Del"""

KEYPAD_BACKSLASH = KeysStandard(Keycode.KEYPAD_BACKSLASH, "KEYPAD_BACKSLASH")
"""Keypad ``\\` and `|`` (Non-US)"""
KP_BSLASH = KeysStandard(Keycode.KEYPAD_BACKSLASH, "KP_BSLASH")
"""Keypad ``\\` and `|`` (Non-US)"""
PBSL = KeysStandard(Keycode.KEYPAD_BACKSLASH, "PBSL")
"""Keypad ``\\` and `|`` (Non-US)"""

APPLICATION = KeysStandard(Keycode.APPLICATION, "APPLICATION")
"""Application: also known as the Menu key (Windows)"""
APP = KeysStandard(Keycode.APPLICATION, "APP")
"""Application: also known as the Menu key (Windows)"""

POWER = KeysStandard(Keycode.POWER, "POWER")
"""Power (Mac)"""
POW = KeysStandard(Keycode.POWER, "POW")
"""Power (Mac)"""

KEYPAD_EQUALS = KeysStandard(Keycode.KEYPAD_EQUALS, "KEYPAD_EQUALS")
"""Keypad ``=`` (Mac)"""
KP_EQUAL = KeysStandard(Keycode.KEYPAD_EQUALS, "KP_EQUAL")
"""Keypad ``=`` (Mac)"""
PEQL = KeysStandard(Keycode.KEYPAD_EQUALS, "PEQL")
"""Keypad ``=`` (Mac)"""

F13 = KeysStandard(Keycode.F13, "F13")
"""Function key F13 (Mac)"""
F14 = KeysStandard(Keycode.F14, "F14")
"""Function key F14 (Mac)"""
F15 = KeysStandard(Keycode.F15, "F15")
"""Function key F15 (Mac)"""
F16 = KeysStandard(Keycode.F16, "F16")
"""Function key F16 (Mac)"""
F17 = KeysStandard(Keycode.F17, "F17")
"""Function key F17 (Mac)"""
F18 = KeysStandard(Keycode.F18, "F18")
"""Function key F18 (Mac)"""
F19 = KeysStandard(Keycode.F19, "F19")
"""Function key F19 (Mac)"""
F20 = KeysStandard(Keycode.F20, "F20")
"""Function key F20"""
F21 = KeysStandard(Keycode.F21, "F21")
"""Function key F21"""
F22 = KeysStandard(Keycode.F22, "F22")
"""Function key F22"""
F23 = KeysStandard(Keycode.F23, "F23")
"""Function key F23"""
F24 = KeysStandard(Keycode.F24, "F24")
"""Function key F24"""

LEFT_CONTROL = KeysStandard(Keycode.LEFT_CONTROL, "LEFT_CONTROL")
"""Control modifier left of the spacebar"""
CONTROL = KeysStandard(Keycode.LEFT_CONTROL, "CONTROL")
"""Control modifier left of the spacebar"""
LCTRL = KeysStandard(Keycode.LEFT_CONTROL, "LCTRL")
"""Control modifier left of the spacebar"""
LCTL = KeysStandard(Keycode.LEFT_CONTROL, "LCTL")
"""Control modifier left of the spacebar"""

LEFT_SHIFT = KeysStandard(Keycode.LEFT_SHIFT, "LEFT_SHIFT")
"""Shift modifier left of the spacebar"""
SHIFT = KeysStandard(Keycode.LEFT_SHIFT, "SHIFT")
"""Shift modifier left of the spacebar"""
LSHIFT = KeysStandard(Keycode.LEFT_SHIFT, "LSHIFT")
"""Shift modifier left of the spacebar"""
LSFT = KeysStandard(Keycode.LEFT_SHIFT, "LSFT")
"""Shift modifier left of the spacebar"""

LEFT_ALT = KeysStandard(Keycode.LEFT_ALT, "LEFT_ALT")
"""Alt modifier left of the spacebar"""
ALT = KeysStandard(Keycode.LEFT_ALT, "ALT")
"""Alt modifier left of the spacebar"""
OPTION = KeysStandard(Keycode.LEFT_ALT, "OPTION")
"""Alt modifier left of the spacebar"""
OPT = KeysStandard(Keycode.LEFT_ALT, "OPT")
"""Alt modifier left of the spacebar"""
LALT = KeysStandard(Keycode.LEFT_ALT, "LALT")
"""Alt modifier left of the spacebar"""

LEFT_GUI = KeysStandard(Keycode.LEFT_GUI, "LEFT_GUI")
"""GUI modifier left of the spacebar"""
GUI = KeysStandard(Keycode.LEFT_GUI, "GUI")
"""GUI modifier left of the spacebar"""
WINDOWS = KeysStandard(Keycode.LEFT_GUI, "WINDOWS")
"""GUI modifier left of the spacebar"""
WIN = KeysStandard(Keycode.LEFT_GUI, "WIN")
"""GUI modifier left of the spacebar"""
COMMAND = KeysStandard(Keycode.LEFT_GUI, "COMMAND")
"""GUI modifier left of the spacebar"""
CMD = KeysStandard(Keycode.LEFT_GUI, "CMD")
"""GUI modifier left of the spacebar"""
LGUI = KeysStandard(Keycode.LEFT_GUI, "LGUI")
"""GUI modifier left of the spacebar"""
LCMD = KeysStandard(Keycode.LEFT_GUI, "LCMD")
"""Command modifier (Mac)"""
LWIN = KeysStandard(Keycode.LEFT_GUI, "LWIN")
"""Windows modifier (Windows keyboards)"""

RIGHT_CONTROL = KeysStandard(Keycode.RIGHT_CONTROL, "RIGHT_CONTROL")
"""Control modifier right of the spacebar"""
RCTRL = KeysStandard(Keycode.RIGHT_CONTROL, "RCTRL")
"""Control modifier right of the spacebar"""
RCTL = KeysStandard(Keycode.RIGHT_CONTROL, "RCTL")
"""Control modifier right of the spacebar"""

RIGHT_SHIFT = KeysStandard(Keycode.RIGHT_SHIFT, "RIGHT_SHIFT")
"""Shift modifier right of the spacebar"""
RSHIFT = KeysStandard(Keycode.RIGHT_SHIFT, "RSHIFT")
"""Shift modifier right of the spacebar"""
RSFT = KeysStandard(Keycode.RIGHT_SHIFT, "RSFT")
"""Shift modifier right of the spacebar"""

RIGHT_ALT = KeysStandard(Keycode.RIGHT_ALT, "RIGHT_ALT")
"""Alt modifier right of the spacebar"""
RALT = KeysStandard(Keycode.RIGHT_ALT, "RALT")
"""Alt modifier right of the spacebar"""

RIGHT_GUI = KeysStandard(Keycode.RIGHT_GUI, "RIGHT_GUI")
"""GUI modifier right of the spacebar"""
RGUI = KeysStandard(Keycode.RIGHT_GUI, "RGUI")
"""GUI modifier right of the spacebar"""
RCMD = KeysStandard(Keycode.RIGHT_GUI, "RCMD")
"""Command modifier (Mac)"""
RWIN = KeysStandard(Keycode.RIGHT_GUI, "RWIN")
"""Windows modifier (Windows keyboards)"""

# fmt: off
__all__ = [
    "KeysStandard",
    
    "NO", "XXXXXXX",

    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M",
    "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
    
    "ONE", "N1", "TWO", "N2", "THREE", "N3", "FOUR", "N4", "FIVE", "N5",
    "SIX", "N6", "SEVEN", "N7", "EIGHT", "N8", "NINE", "N9", "ZERO", "N0",

    "ENTER", "RETURN", "ENT", 
    "ESCAPE", "ESC", 
    "BACKSPACE", "BSPACE", "BSPC",
    "TAB", 
    "SPACEBAR", "SPACE", "SPC", 
    "MINUS", "MINS", 
    "EQUALS", "EQUAL", "EQL",
    "LEFT_BRACKET", "LBRACKET", "LBRC", 
    "RIGHT_BRACKET", "RBRACKET", "RBRC",
    "BACKSLASH", "BSLASH", "BSLS", 
    "POUND", 
    "SEMICOLON", "SCOLON", "SCLN",
    "QUOTE", "QUOT", 
    "GRAVE_ACCENT", "GRAVE", "GRV", "ZKHK", 
    "COMMA", "COMM",
    "PERIOD", "DOT", 
    "FORWARD_SLASH", "SLASH", "SLSH", 
    
    "CAPS_LOCK", "CAPSLOCK", "CAPS", "CLCK", 
    "F1", "F2", "F3", "F4", "F5", "F6", 
    "F7", "F8", "F9", "F10", "F11", "F12", 
    "PRINT_SCREEN", "PSCREEN", "PSCR", 
    "SCROLL_LOCK", "SCROLLLOCK",
    "SLCK", "PAUSE", "PAUS", "BRK", 
    "INSERT", "INS", 
    "HOME", 
    "PAGE_UP", "PGUP",
    "DELETE", "DEL", 
    "END", 
    "PAGE_DOWN", "PGDN", 

    "RIGHT_ARROW", "RIGHT", "RGHT",
    "LEFT_ARROW", "LEFT", 
    "DOWN_ARROW", "DOWN", 
    "UP_ARROW", "UP",

    "KEYPAD_NUMLOCK", "NUMLOCK", "NLCK", 
    "KEYPAD_FORWARD_SLASH", "KP_SLASH", "PSLS", 
    "KEYPAD_ASTERISK", "KP_ASTERISK", "PAST", 
    "KEYPAD_MINUS", "KP_MINUS", "PMNS", 
    "KEYPAD_PLUS", "KP_PLUS", "PPLS", 
    "KEYPAD_ENTER", "KP_ENTER", "PENT",

    "KEYPAD_ONE", "KP_1", "P1", 
    "KEYPAD_TWO", "KP_2", "P2", 
    "KEYPAD_THREE", "KP_3", "P3", 
    "KEYPAD_FOUR", "KP_4", "P4", 
    "KEYPAD_FIVE", "KP_5", "P5",
    "KEYPAD_SIX", "KP_6", "P6", 
    "KEYPAD_SEVEN", "KP_7", "P7", 
    "KEYPAD_EIGHT", "KP_8", "P8", 
    "KEYPAD_NINE", "KP_9", "P9", 
    "KEYPAD_ZERO", "KP_0", "P0",
    
    "KEYPAD_PERIOD", "KP_DOT", "PDOT",
    "KEYPAD_BACKSLASH", "KP_BSLASH", "PBSL",
    "KEYPAD_EQUALS", "KP_EQUAL", "PEQL",

    "APPLICATION", "APP",
    "POWER", "POW",

    "F13", "F14", "F15", "F16", "F17", "F18", "F19", 
    "F20", "F21", "F22", "F23", "F24",

    "LEFT_CONTROL", "CONTROL", "LCTRL", "LCTL",
    "LEFT_SHIFT", "SHIFT", "LSHIFT", "LSFT",
    "LEFT_ALT", "ALT", "OPTION", "OPT", "LALT",
    "LEFT_GUI", "GUI", "WINDOWS", "WIN", "COMMAND", "CMD", "LGUI", "LCMD", "LWIN",

    "RIGHT_CONTROL", "RCTRL", "RCTL",
    "RIGHT_SHIFT", "RSHIFT", "RSFT",
    "RIGHT_ALT", "RALT",
    "RIGHT_GUI", "RGUI", "RCMD", "RWIN",
]
# fmt: on
