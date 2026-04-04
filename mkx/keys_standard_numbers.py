from adafruit_hid.keycode import Keycode

from mkx.keys_standard_core import KeysStandard

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

# fmt: off
__all__ = [
    "ONE", "N1", "TWO", "N2", "THREE", "N3", "FOUR", "N4", "FIVE", "N5",
    "SIX", "N6", "SEVEN", "N7", "EIGHT", "N8", "NINE", "N9", "ZERO", "N0",
]
# fmt: on
