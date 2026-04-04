"""
Function key definitions (F1-F24).
"""

from adafruit_hid.keycode import Keycode

from mkx.keys_standard_core import KeysStandard

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

# fmt: off
__all__ = [
    "F1", "F2", "F3", "F4", "F5", "F6",
    "F7", "F8", "F9", "F10", "F11", "F12",
    "F13", "F14", "F15", "F16", "F17", "F18", "F19",
    "F20", "F21", "F22", "F23", "F24",
]
# fmt: on
