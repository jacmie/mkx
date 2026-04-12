from adafruit_hid.keycode import Keycode

from mkx.keys_standard_core import KeysStandard

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

# fmt: off
__all__ = [
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
]
# fmt: on
