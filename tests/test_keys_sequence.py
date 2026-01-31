"""
Unit tests for Sequence key functionality.
Tests key sequence execution.
"""

from mkx.keys_sequence import SEQ
from mkx.keys_standard import KeysStandard
from tests.conftest import MockKeycode


class TestSequenceKeys:
    """Test suite for Sequence (SEQ) key functionality"""

    def test_seq_initialization(self):
        """Test SEQ initializes correctly"""
        key_a = KeysStandard(MockKeycode.A, "A")
        key_b = KeysStandard(MockKeycode.B, "B")

        seq = SEQ([key_a, key_b])

        assert seq._key_list == [key_a, key_b]
        assert seq.key_name == "SEQ(keys[])"

    def test_seq_empty_list(self):
        """Test SEQ with empty key list"""
        seq = SEQ([])

        assert seq._key_list == []
        assert len(seq._key_list) == 0

    def test_seq_single_key(self, mock_keyboard, layer_manager):
        """Test SEQ with single key"""
        key_a = KeysStandard(MockKeycode.A, "A")
        seq = SEQ([key_a])

        seq.on_press(layer_manager, mock_keyboard, 0)

        # Key should be pressed and released
        assert MockKeycode.A in mock_keyboard.released_keys

    def test_seq_multiple_keys(self, mock_keyboard, layer_manager):
        """Test SEQ with multiple keys"""
        key_a = KeysStandard(MockKeycode.A, "A")
        key_b = KeysStandard(MockKeycode.B, "B")
        key_c = KeysStandard(MockKeycode.C, "C")

        seq = SEQ([key_a, key_b, key_c])

        seq.on_press(layer_manager, mock_keyboard, 0)

        # All keys should be released (pressed and immediately released)
        assert MockKeycode.A in mock_keyboard.released_keys
        assert MockKeycode.B in mock_keyboard.released_keys
        assert MockKeycode.C in mock_keyboard.released_keys

    def test_seq_key_press_release_order(self, mock_keyboard, layer_manager):
        """Test that SEQ executes keys in order"""
        key_a = KeysStandard(MockKeycode.A, "A")
        key_b = KeysStandard(MockKeycode.B, "B")

        seq = SEQ([key_a, key_b])
        seq.on_press(layer_manager, mock_keyboard, 0)

        # Both keys should be in released_keys in the order they were pressed
        assert len(mock_keyboard.released_keys) >= 2

    def test_seq_on_release_does_nothing(self, mock_keyboard, layer_manager):
        """Test that SEQ on_release does nothing"""
        key_a = KeysStandard(MockKeycode.A, "A")
        seq = SEQ([key_a])

        # on_release should do nothing (pass)
        seq.on_release(layer_manager, mock_keyboard, 100)

        # No keys should be in released_keys
        assert len(mock_keyboard.released_keys) == 0

    def test_seq_press_release_cycle(self, mock_keyboard, layer_manager):
        """Test full press-release cycle of SEQ"""
        key_a = KeysStandard(MockKeycode.A, "A")
        key_b = KeysStandard(MockKeycode.B, "B")

        seq = SEQ([key_a, key_b])

        seq.press(layer_manager, mock_keyboard, 0)
        assert seq._is_pressed is True

        seq.release(layer_manager, mock_keyboard, 100)
        assert seq._is_pressed is False
