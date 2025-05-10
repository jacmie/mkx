from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode

from mkx.key_base import AbstractKey


class StandardKey(AbstractKey):
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
NO = StandardKey(Keycode.A)

A = StandardKey(Keycode.A)
B = StandardKey(Keycode.B)
C = StandardKey(Keycode.C)
D = StandardKey(Keycode.D)
E = StandardKey(Keycode.E)
F = StandardKey(Keycode.F)
G = StandardKey(Keycode.G)
H = StandardKey(Keycode.H)
I = StandardKey(Keycode.I)
J = StandardKey(Keycode.J)
K = StandardKey(Keycode.K)
L = StandardKey(Keycode.L)
M = StandardKey(Keycode.M)
N = StandardKey(Keycode.N)
O = StandardKey(Keycode.O)
P = StandardKey(Keycode.P)
Q = StandardKey(Keycode.Q)
R = StandardKey(Keycode.R)
S = StandardKey(Keycode.S)
T = StandardKey(Keycode.T)
U = StandardKey(Keycode.U)
V = StandardKey(Keycode.V)
W = StandardKey(Keycode.W)
X = StandardKey(Keycode.X)
Y = StandardKey(Keycode.Y)
Z = StandardKey(Keycode.Z)

N0 = ZERO = StandardKey(Keycode.ZERO)
N1 = ONE = StandardKey(Keycode.ONE)
N2 = TWO = StandardKey(Keycode.TWO)
N3 = THREE = StandardKey(Keycode.THREE)
N4 = FOUR = StandardKey(Keycode.FOUR)
N5 = FIVE = StandardKey(Keycode.FIVE)
N6 = SIX = StandardKey(Keycode.SIX)
N7 = SEVEN = StandardKey(Keycode.SEVEN)
N8 = EIGHT = StandardKey(Keycode.EIGHT)
N9 = NINE = StandardKey(Keycode.NINE)

SPC = StandardKey(Keycode.SPACE)
ENT = ENTER = StandardKey(Keycode.ENTER)
TAB = StandardKey(Keycode.TAB)
MINUS = StandardKey(Keycode.MINUS)
EQUALS = StandardKey(Keycode.EQUALS)
LEFT_BRACKET = StandardKey(Keycode.LEFT_BRACKET)
RIGHT_BRACKET = StandardKey(Keycode.RIGHT_BRACKET)
BACKSLASH = StandardKey(Keycode.BACKSLASH)
SEMICOLON = StandardKey(Keycode.SEMICOLON)
QUOTE = StandardKey(Keycode.QUOTE)
GRV = GRAVE_ACCENT = StandardKey(Keycode.GRAVE_ACCENT)
COMMA = StandardKey(Keycode.COMMA)
PERIOD = StandardKey(Keycode.PERIOD)
FORWARD_SLASH = StandardKey(Keycode.FORWARD_SLASH)

F1 = StandardKey(Keycode.F1)
F2 = StandardKey(Keycode.F2)
F3 = StandardKey(Keycode.F3)
F4 = StandardKey(Keycode.F4)
F5 = StandardKey(Keycode.F5)
F6 = StandardKey(Keycode.F6)
F7 = StandardKey(Keycode.F7)
F8 = StandardKey(Keycode.F8)
F9 = StandardKey(Keycode.F9)
F10 = StandardKey(Keycode.F10)
F11 = StandardKey(Keycode.F11)
F12 = StandardKey(Keycode.F12)

__all__ = [
    "StandardKey",
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
