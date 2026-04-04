from adafruit_hid.keycode import Keycode

from mkx.keys_standard_core import KeysStandard

NO = KeysStandard(None, "None")
"""None key"""
XXXXXXX = KeysStandard(None, "XXXXXXX")
"""None key"""

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

CAPS_LOCK = KeysStandard(Keycode.CAPS_LOCK, "CAPS_LOCK")
"""Caps Lock"""
CAPSLOCK = KeysStandard(Keycode.CAPS_LOCK, "CAPSLOCK")
"""Caps Lock"""
CAPS = KeysStandard(Keycode.CAPS_LOCK, "CAPS")
"""Caps Lock"""
CLCK = KeysStandard(Keycode.CAPS_LOCK, "CLCK")
"""Caps Lock"""

PRINT_SCREEN = KeysStandard(Keycode.PRINT_SCREEN, "PRINT_SCREEN")
"""Print Screen (SysRq)"""
PSCREEN = KeysStandard(Keycode.PRINT_SCREEN, "PSCREEN")
"""Print Screen (SysRq)"""
PSCR = KeysStandard(Keycode.PRINT_SCREEN, "PSCR")
"""Print Screen (SysRq)"""

SCROLL_LOCK = KeysStandard(Keycode.SCROLL_LOCK, "SCROLL_LOCK")
"""Scroll Lock"""
SCROLLOCK = KeysStandard(Keycode.SCROLL_LOCK, "SCROLLOCK")
"""Scroll Lock"""
SLCK = KeysStandard(Keycode.SCROLL_LOCK, "SLCK")
"""Scroll Lock"""

PAUSE = KeysStandard(Keycode.PAUSE, "PAUSE")
"""Pause (Break)"""
PAUS = KeysStandard(Keycode.PAUSE, "PAUS")
"""Pause (Break)"""
BRK = KeysStandard(Keycode.PAUSE, "BRK")
"""Pause (Break)"""

APPLICATION = KeysStandard(Keycode.APPLICATION, "APPLICATION")
"""Application: also known as the Menu key (Windows)"""
APP = KeysStandard(Keycode.APPLICATION, "APP")
"""Application: also known as the Menu key (Windows)"""

POWER = KeysStandard(Keycode.POWER, "POWER")
"""Power (Mac)"""
POW = KeysStandard(Keycode.POWER, "POW")
"""Power (Mac)"""

# fmt: off
__all__ = [
    "NO", "XXXXXXX",
    "ENTER", "RETURN", "ENT",
    "ESCAPE", "ESC",
    "BACKSPACE", "BSPACE", "BSPC",
    "TAB",
    "SPACEBAR", "SPACE", "SPC",
    "CAPS_LOCK", "CAPSLOCK", "CAPS", "CLCK",
    "PRINT_SCREEN", "PSCREEN", "PSCR",
    "SCROLL_LOCK", "SCROLLOCK", "SLCK",
    "PAUSE", "PAUS", "BRK",
    "APPLICATION", "APP",
    "POWER", "POW",
]
# fmt: on
