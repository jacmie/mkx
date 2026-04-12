"""
Standard keyboard key definitions - collected from category modules.

This module gathers all standard key definitions from specialized category files
and re-exports them for convenience. Each category file can be imported individually
for more granular control.
"""

# Import the class
from mkx.keys_standard_core import KeysStandard

# Import all key definitions from category modules
from mkx.keys_standard_letters import *
from mkx.keys_standard_numbers import *
from mkx.keys_standard_punctuation import *
from mkx.keys_standard_functions import *
from mkx.keys_standard_navigation import *
from mkx.keys_standard_numpad import *
from mkx.keys_standard_modifiers import *
from mkx.keys_standard_special import *

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
