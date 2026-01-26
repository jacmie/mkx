"""
Pytest configuration and shared fixtures for mkx tests.
Provides mocks for hardware-dependent CircuitPython libraries.
"""

import pytest
from unittest.mock import MagicMock
import sys


# Mock CircuitPython-specific modules that won't be available on desktop
class MockKeycode:
    """Mock Adafruit HID Keycode - includes all standard keyboard keycodes"""

    # Letters A-Z
    A = 0x04
    B = 0x05
    C = 0x06
    D = 0x07
    E = 0x08
    F = 0x09
    G = 0x0A
    H = 0x0B
    I = 0x0C
    J = 0x0D
    K = 0x0E
    L = 0x0F
    M = 0x10
    N = 0x11
    O = 0x12
    P = 0x13
    Q = 0x14
    R = 0x15
    S = 0x16
    T = 0x17
    U = 0x18
    V = 0x19
    W = 0x1A
    X = 0x1B
    Y = 0x1C
    Z = 0x1D

    # Numbers 0-9
    ONE = 0x1E
    TWO = 0x1F
    THREE = 0x20
    FOUR = 0x21
    FIVE = 0x22
    SIX = 0x23
    SEVEN = 0x24
    EIGHT = 0x25
    NINE = 0x26
    ZERO = 0x27

    # Special keys
    ENTER = 0x28
    ESCAPE = 0x29
    BACKSPACE = 0x2A
    TAB = 0x2B
    SPACEBAR = 0x2C
    MINUS = 0x2D
    EQUALS = 0x2E
    LEFT_BRACKET = 0x2F
    RIGHT_BRACKET = 0x30
    BACKSLASH = 0x31
    POUND = 0x32
    SEMICOLON = 0x33
    QUOTE = 0x34
    GRAVE_ACCENT = 0x35
    COMMA = 0x36
    PERIOD = 0x37
    FORWARD_SLASH = 0x38
    CAPS_LOCK = 0x39

    # Function keys F1-F24
    F1 = 0x3A
    F2 = 0x3B
    F3 = 0x3C
    F4 = 0x3D
    F5 = 0x3E
    F6 = 0x3F
    F7 = 0x40
    F8 = 0x41
    F9 = 0x42
    F10 = 0x43
    F11 = 0x44
    F12 = 0x45
    F13 = 0x64
    F14 = 0x65
    F15 = 0x66
    F16 = 0x67
    F17 = 0x68
    F18 = 0x69
    F19 = 0x6A
    F20 = 0x6B
    F21 = 0x6C
    F22 = 0x6D
    F23 = 0x6E
    F24 = 0x6F

    # Print/Scroll/Pause
    PRINT_SCREEN = 0x46
    SCROLL_LOCK = 0x47
    PAUSE = 0x48

    # Navigation keys
    INSERT = 0x49
    HOME = 0x4A
    PAGE_UP = 0x4B
    DELETE = 0x4C
    END = 0x4D
    PAGE_DOWN = 0x4E
    RIGHT_ARROW = 0x4F
    LEFT_ARROW = 0x50
    DOWN_ARROW = 0x51
    UP_ARROW = 0x52

    # Keypad keys
    KEYPAD_NUMLOCK = 0x53
    KEYPAD_FORWARD_SLASH = 0x54
    KEYPAD_ASTERISK = 0x55
    KEYPAD_MINUS = 0x56
    KEYPAD_PLUS = 0x57
    KEYPAD_ENTER = 0x58
    KEYPAD_ONE = 0x59
    KEYPAD_TWO = 0x5A
    KEYPAD_THREE = 0x5B
    KEYPAD_FOUR = 0x5C
    KEYPAD_FIVE = 0x5D
    KEYPAD_SIX = 0x5E
    KEYPAD_SEVEN = 0x5F
    KEYPAD_EIGHT = 0x60
    KEYPAD_NINE = 0x61
    KEYPAD_ZERO = 0x62
    KEYPAD_PERIOD = 0x63
    KEYPAD_BACKSLASH = 0x64
    KEYPAD_EQUALS = 0x65

    # Application/System keys
    APPLICATION = 0x66
    POWER = 0x67

    # Modifier keys
    LEFT_CONTROL = 0x70
    LEFT_SHIFT = 0x71
    LEFT_ALT = 0x72
    LEFT_GUI = 0x73
    RIGHT_CONTROL = 0x74
    RIGHT_SHIFT = 0x75
    RIGHT_ALT = 0x76
    RIGHT_GUI = 0x77


class MockDigitalIO:
    """Mock digitalio module"""

    class Pull:
        UP = 1
        DOWN = 0

    class DigitalInOut:
        def __init__(self, pin):
            self.pin = pin
            self._value = 0
            self._direction = "input"

        def switch_to_input(self, pull=None):
            self._direction = "input"
            self.pull = pull

        def switch_to_output(self, value=False):
            self._direction = "output"
            self._value = value

        @property
        def value(self):
            return self._value

        @value.setter
        def value(self, val):
            self._value = val


class MockKeyboard:
    """Mock Adafruit HID Keyboard"""

    def __init__(self):
        self.pressed_keys = []
        self.released_keys = []
        self.press_count = 0
        self.release_count = 0

    def press(self, keycode):
        if keycode is not None and keycode not in self.pressed_keys:
            self.pressed_keys.append(keycode)
            self.press_count += 1

    def release(self, keycode):
        if keycode is not None and keycode in self.pressed_keys:
            self.pressed_keys.remove(keycode)
            self.released_keys.append(keycode)
            self.release_count += 1

    def write(self, buf):
        """Mock write method for raw reports"""
        pass

    def reset_buffer(self):
        """Reset internal buffer"""
        pass


# Mock modules before importing mkx
# Create mock modules with proper attributes to avoid coverage issues
adafruit_hid_mock = MagicMock()
adafruit_hid_keyboard_mock = MagicMock()
adafruit_hid_keyboard_mock.Keyboard = MockKeyboard
adafruit_hid_keycode_mock = MagicMock()
adafruit_hid_keycode_mock.Keycode = MockKeycode
adafruit_hid_mouse_mock = MagicMock()
keypad_mock = MagicMock()
time_mock = MagicMock()
digitalio_mock = MagicMock()
digitalio_mock.Pull = MockDigitalIO.Pull
digitalio_mock.DigitalInOut = MockDigitalIO.DigitalInOut

sys.modules["adafruit_hid"] = adafruit_hid_mock
sys.modules["adafruit_hid.keyboard"] = adafruit_hid_keyboard_mock
sys.modules["adafruit_hid.keycode"] = adafruit_hid_keycode_mock
sys.modules["adafruit_hid.mouse"] = adafruit_hid_mouse_mock
sys.modules["keypad"] = keypad_mock
sys.modules["time"] = time_mock
sys.modules["digitalio"] = digitalio_mock

# Add mkx to path for imports
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


@pytest.fixture
def mock_keyboard():
    """Fixture providing a mock Keyboard instance"""
    return MockKeyboard()


@pytest.fixture
def layer_manager():
    """Fixture providing a LayerManager instance"""
    from mkx.manager_layers import LayersManager

    return LayersManager(default_layer=0)
