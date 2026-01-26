"""
Unit tests for standard key functionality.
Tests key press/release with various key codes.
"""

from mkx.keys_standard import KeysStandard
from tests.conftest import MockKeycode


class TestKeysStandard:
    """Test suite for KeysStandard key type"""

    def test_standard_key_initialization(self):
        """Test that standard keys initialize correctly"""
        key = KeysStandard(MockKeycode.A, "A")
        assert key.key_code == MockKeycode.A
        assert key.key_name == "A"
        assert key._is_pressed is False

    def test_standard_key_press(self, mock_keyboard, layer_manager):
        """Test standard key press sends correct HID keycode"""
        key = KeysStandard(MockKeycode.A, "A")

        key.press(layer_manager, mock_keyboard, 0)

        assert key._is_pressed is True
        assert MockKeycode.A in mock_keyboard.pressed_keys
        assert mock_keyboard.press_count == 1

    def test_standard_key_release(self, mock_keyboard, layer_manager):
        """Test standard key release sends correct HID keycode"""
        key = KeysStandard(MockKeycode.A, "A")

        # Press first
        key.press(layer_manager, mock_keyboard, 0)
        assert MockKeycode.A in mock_keyboard.pressed_keys

        # Then release
        key.release(layer_manager, mock_keyboard, 100)

        assert key._is_pressed is False
        assert MockKeycode.A not in mock_keyboard.pressed_keys
        assert MockKeycode.A in mock_keyboard.released_keys
        assert mock_keyboard.release_count == 1

    def test_standard_key_press_release_sequence(self, mock_keyboard, layer_manager):
        """Test full press-release sequence"""
        key = KeysStandard(MockKeycode.ENTER, "ENTER")

        key.press(layer_manager, mock_keyboard, 0)
        assert mock_keyboard.press_count == 1
        assert MockKeycode.ENTER in mock_keyboard.pressed_keys

        key.release(layer_manager, mock_keyboard, 100)
        assert mock_keyboard.release_count == 1
        assert MockKeycode.ENTER not in mock_keyboard.pressed_keys

    def test_standard_key_no_press_twice(self, mock_keyboard, layer_manager):
        """Test that pressing twice doesn't send duplicate press event"""
        key = KeysStandard(MockKeycode.B, "B")

        key.press(layer_manager, mock_keyboard, 0)
        initial_count = mock_keyboard.press_count

        # Try to press again without releasing
        key.press(layer_manager, mock_keyboard, 50)

        # Press count should not increase
        assert mock_keyboard.press_count == initial_count

    def test_standard_key_no_release_twice(self, mock_keyboard, layer_manager):
        """Test that releasing twice doesn't send duplicate release event"""
        key = KeysStandard(MockKeycode.C, "C")

        key.press(layer_manager, mock_keyboard, 0)
        key.release(layer_manager, mock_keyboard, 100)
        initial_count = mock_keyboard.release_count

        # Try to release again
        key.release(layer_manager, mock_keyboard, 150)

        # Release count should not increase
        assert mock_keyboard.release_count == initial_count

    def test_standard_key_with_none_keycode(self, mock_keyboard, layer_manager):
        """Test standard key with None keycode (e.g., NO/XXXXXXX)"""
        key = KeysStandard(None, "NONE")

        # Should not raise an exception
        key.press(layer_manager, mock_keyboard, 0)
        key.release(layer_manager, mock_keyboard, 100)

        assert key._is_pressed is False

    def test_multiple_keys_pressed_simultaneously(self, mock_keyboard, layer_manager):
        """Test multiple keys can be pressed simultaneously"""
        key_a = KeysStandard(MockKeycode.A, "A")
        key_b = KeysStandard(MockKeycode.B, "B")

        key_a.press(layer_manager, mock_keyboard, 0)
        key_b.press(layer_manager, mock_keyboard, 10)

        assert MockKeycode.A in mock_keyboard.pressed_keys
        assert MockKeycode.B in mock_keyboard.pressed_keys
        assert mock_keyboard.press_count == 2

    def test_multiple_keys_released_independently(self, mock_keyboard, layer_manager):
        """Test multiple keys can be released independently"""
        key_a = KeysStandard(MockKeycode.A, "A")
        key_b = KeysStandard(MockKeycode.B, "B")

        key_a.press(layer_manager, mock_keyboard, 0)
        key_b.press(layer_manager, mock_keyboard, 10)

        # Release only key_a
        key_a.release(layer_manager, mock_keyboard, 100)

        assert key_a._is_pressed is False
        assert key_b._is_pressed is True
        assert MockKeycode.A not in mock_keyboard.pressed_keys
        assert MockKeycode.B in mock_keyboard.pressed_keys
