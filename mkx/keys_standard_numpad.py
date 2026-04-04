from adafruit_hid.keycode import Keycode

from mkx.keys_standard_core import KeysStandard

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

KEYPAD_EQUALS = KeysStandard(Keycode.KEYPAD_EQUALS, "KEYPAD_EQUALS")
"""Keypad ``=`` (Mac)"""
KP_EQUAL = KeysStandard(Keycode.KEYPAD_EQUALS, "KP_EQUAL")
"""Keypad ``=`` (Mac)"""
PEQL = KeysStandard(Keycode.KEYPAD_EQUALS, "PEQL")
"""Keypad ``=`` (Mac)"""

# fmt: off
__all__ = [
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
]
# fmt: on
