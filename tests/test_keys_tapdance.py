"""
Unit tests for Tap Dance key functionality.
Tests multi-tap key behavior.
"""

from mkx.keys_tapdance import TD
from mkx.keys_standard import KeysStandard
from tests.conftest import MockKeycode


class TestTapDanceKeys:
    """Test suite for Tap Dance (TD) key functionality"""

    def test_td_initialization(self):
        """Test TD initializes correctly"""
        key_single = KeysStandard(MockKeycode.A, "A")
        key_double = KeysStandard(MockKeycode.B, "B")

        td = TD(key_single, key_double)

        assert td._keys == [key_single, key_double]
        assert td._tap_count == 0
        assert td._timeout == 200

    def test_td_with_custom_timeout(self):
        """Test TD with custom timeout"""
        key_single = KeysStandard(MockKeycode.A, "A")
        key_double = KeysStandard(MockKeycode.B, "B")

        td = TD(key_single, key_double, timeout=300)

        assert td._timeout == 300
        assert len(td._keys) == 2

    def test_td_with_single_key(self):
        """Test TD with single key"""
        key = KeysStandard(MockKeycode.A, "A")

        td = TD(key)

        assert len(td._keys) == 1
        assert td._keys[0] == key

    def test_td_with_multiple_keys(self):
        """Test TD with multiple keys (triple tap, etc)"""
        key_a = KeysStandard(MockKeycode.A, "A")
        key_b = KeysStandard(MockKeycode.B, "B")
        key_c = KeysStandard(MockKeycode.C, "C")

        td = TD(key_a, key_b, key_c)

        assert len(td._keys) == 3

    def test_td_press_increments_tap_count(self, mock_keyboard, layer_manager):
        """Test TD press increments tap count"""
        key_single = KeysStandard(MockKeycode.A, "A")
        key_double = KeysStandard(MockKeycode.B, "B")

        td = TD(key_single, key_double)

        assert td._tap_count == 0

        td.on_press(layer_manager, mock_keyboard, 0)

        assert td._tap_count == 1

    def test_td_press_release_cycle(self, mock_keyboard, layer_manager):
        """Test full TD press-release cycle"""
        key_single = KeysStandard(MockKeycode.A, "A")
        key_double = KeysStandard(MockKeycode.B, "B")

        td = TD(key_single, key_double)

        td.press(layer_manager, mock_keyboard, 0)
        assert td._is_pressed is True

        td.release(layer_manager, mock_keyboard, 100)
        assert td._is_pressed is False

    def test_td_initialization_with_name(self):
        """Test TD initializes with correct name"""
        key = KeysStandard(MockKeycode.A, "A")

        td = TD(key)

        assert td.key_name == "TD"
