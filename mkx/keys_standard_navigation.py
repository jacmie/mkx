from adafruit_hid.keycode import Keycode

from mkx.keys_standard_core import KeysStandard

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

# fmt: off
__all__ = [
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
]
# fmt: on
