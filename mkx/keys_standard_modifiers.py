from adafruit_hid.keycode import Keycode

from mkx.keys_standard_core import KeysStandard

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
