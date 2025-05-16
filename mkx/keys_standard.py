from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from mkx.keys_abstract import KeysAbstract


class KeysStandard(KeysAbstract):
    """
    A standard key that sends a HID keycode using Adafruit HID library.
    """

    def __init__(self, keycode):
        super().__init__()
        self.keycode = keycode

    def on_press(self, keyboard: Keyboard):
        keyboard.press(self.keycode)

    def on_release(self, keyboard: Keyboard):
        keyboard.release(self.keycode)


# Hardcoded standard key definitions
NO = KeysStandard(Keycode.A)

A = KeysStandard(Keycode.A)
B = KeysStandard(Keycode.B)
C = KeysStandard(Keycode.C)
D = KeysStandard(Keycode.D)
E = KeysStandard(Keycode.E)
F = KeysStandard(Keycode.F)
G = KeysStandard(Keycode.G)
H = KeysStandard(Keycode.H)
I = KeysStandard(Keycode.I)
J = KeysStandard(Keycode.J)
K = KeysStandard(Keycode.K)
L = KeysStandard(Keycode.L)
M = KeysStandard(Keycode.M)
N = KeysStandard(Keycode.N)
O = KeysStandard(Keycode.O)
P = KeysStandard(Keycode.P)
Q = KeysStandard(Keycode.Q)
R = KeysStandard(Keycode.R)
S = KeysStandard(Keycode.S)
T = KeysStandard(Keycode.T)
U = KeysStandard(Keycode.U)
V = KeysStandard(Keycode.V)
W = KeysStandard(Keycode.W)
X = KeysStandard(Keycode.X)
Y = KeysStandard(Keycode.Y)
Z = KeysStandard(Keycode.Z)

N0 = ZERO = KeysStandard(Keycode.ZERO)
N1 = ONE = KeysStandard(Keycode.ONE)
N2 = TWO = KeysStandard(Keycode.TWO)
N3 = THREE = KeysStandard(Keycode.THREE)
N4 = FOUR = KeysStandard(Keycode.FOUR)
N5 = FIVE = KeysStandard(Keycode.FIVE)
N6 = SIX = KeysStandard(Keycode.SIX)
N7 = SEVEN = KeysStandard(Keycode.SEVEN)
N8 = EIGHT = KeysStandard(Keycode.EIGHT)
N9 = NINE = KeysStandard(Keycode.NINE)

SPC = KeysStandard(Keycode.SPACE)
ENT = ENTER = KeysStandard(Keycode.ENTER)
TAB = KeysStandard(Keycode.TAB)
MINUS = KeysStandard(Keycode.MINUS)
EQUALS = KeysStandard(Keycode.EQUALS)
LEFT_BRACKET = KeysStandard(Keycode.LEFT_BRACKET)
RIGHT_BRACKET = KeysStandard(Keycode.RIGHT_BRACKET)
BACKSLASH = KeysStandard(Keycode.BACKSLASH)
SEMICOLON = KeysStandard(Keycode.SEMICOLON)
QUOTE = KeysStandard(Keycode.QUOTE)
GRV = GRAVE_ACCENT = KeysStandard(Keycode.GRAVE_ACCENT)
COMMA = KeysStandard(Keycode.COMMA)
PERIOD = KeysStandard(Keycode.PERIOD)
FORWARD_SLASH = KeysStandard(Keycode.FORWARD_SLASH)

F1 = KeysStandard(Keycode.F1)
F2 = KeysStandard(Keycode.F2)
F3 = KeysStandard(Keycode.F3)
F4 = KeysStandard(Keycode.F4)
F5 = KeysStandard(Keycode.F5)
F6 = KeysStandard(Keycode.F6)
F7 = KeysStandard(Keycode.F7)
F8 = KeysStandard(Keycode.F8)
F9 = KeysStandard(Keycode.F9)
F10 = KeysStandard(Keycode.F10)
F11 = KeysStandard(Keycode.F11)
F12 = KeysStandard(Keycode.F12)

__all__ = [
    "KeysStandard",
    "NO",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
    "N0",
    "N1",
    "N2",
    "N3",
    "N4",
    "N5",
    "N6",
    "N7",
    "N8",
    "N9",
    "ZERO",
    "ONE",
    "TWO",
    "THREE",
    "FOUR",
    "FIVE",
    "SIX",
    "SEVEN",
    "EIGHT",
    "NINE",
    "SPC",
    "SPACE",
    "ENTER",
    "TAB",
    "MINUS",
    "EQUALS",
    "LEFT_BRACKET",
    "RIGHT_BRACKET",
    "BACKSLASH",
    "SEMICOLON",
    "QUOTE",
    "GRAVE_ACCENT",
    "COMMA",
    "PERIOD",
    "FORWARD_SLASH",
    "F1",
    "F2",
    "F3",
    "F4",
    "F5",
    "F6",
    "F7",
    "F8",
    "F9",
    "F10",
    "F11",
    "F12",
]


# Initialize the keyboard
# kbd = Keyboard(usb_hid.devices)

# # Simulate pressing and releasing the key
# key_a.press(kbd, timestamp=123.456)
# key_a.release(kbd, timestamp=123.789)
