"""
Unit tests for KeysAbstract base class.
Tests the abstract key implementation and press/release behavior.
"""

import pytest
from unittest.mock import MagicMock
from mkx.keys_abstract import KeysAbstract
from tests.conftest import MockKeycode, MockKeyboard


class ConcreteKey(KeysAbstract):
    """Concrete implementation of KeysAbstract for testing"""

    def __init__(self, key_name="TEST_KEY"):
        super().__init__()
        self.key_name = key_name
        self.press_count = 0
        self.release_count = 0

    def on_press(self, layer_manager, keyboard, timestamp):
        self.press_count += 1

    def on_release(self, layer_manager, keyboard, timestamp):
        self.release_count += 1


class TestKeysAbstract:
    """Test suite for KeysAbstract base class"""

    def test_abstract_key_initialization(self):
        """Test that abstract keys initialize correctly"""
        key = ConcreteKey("MY_KEY")
        assert key._is_pressed is False
        assert key.press_count == 0
        assert key.release_count == 0

    def test_abstract_key_press_calls_on_press(self, mock_keyboard, layer_manager):
        """Test that press() calls on_press()"""
        key = ConcreteKey()
        key.press(layer_manager, mock_keyboard, 0)

        assert key._is_pressed is True
        assert key.press_count == 1

    def test_abstract_key_release_calls_on_release(self, mock_keyboard, layer_manager):
        """Test that release() calls on_release()"""
        key = ConcreteKey()
        key.press(layer_manager, mock_keyboard, 0)
        key.release(layer_manager, mock_keyboard, 100)

        assert key._is_pressed is False
        assert key.release_count == 1

    def test_abstract_key_press_prevents_duplicate_press(
        self, mock_keyboard, layer_manager
    ):
        """Test that pressing an already-pressed key doesn't trigger on_press again"""
        key = ConcreteKey()
        key.press(layer_manager, mock_keyboard, 0)
        key.press(layer_manager, mock_keyboard, 50)

        assert key.press_count == 1  # Should only call on_press once
        assert key._is_pressed is True

    def test_abstract_key_release_prevents_duplicate_release(
        self, mock_keyboard, layer_manager
    ):
        """Test that releasing an already-released key doesn't trigger on_release"""
        key = ConcreteKey()
        key.press(layer_manager, mock_keyboard, 0)
        key.release(layer_manager, mock_keyboard, 100)
        key.release(layer_manager, mock_keyboard, 150)

        assert key.release_count == 1  # Should only call on_release once
        assert key._is_pressed is False

    def test_abstract_key_not_implemented_errors(self):
        """Test that KeysAbstract methods raise NotImplementedError"""
        key = KeysAbstract()

        with pytest.raises(NotImplementedError):
            key.on_press(None, None, 0)

        with pytest.raises(NotImplementedError):
            key.on_release(None, None, 0)

    def test_abstract_key_full_press_release_cycle(self, mock_keyboard, layer_manager):
        """Test a complete press-release cycle"""
        key = ConcreteKey()

        key.press(layer_manager, mock_keyboard, 0)
        assert key._is_pressed is True
        assert key.press_count == 1
        assert key.release_count == 0

        key.release(layer_manager, mock_keyboard, 100)
        assert key._is_pressed is False
        assert key.press_count == 1
        assert key.release_count == 1

    def test_abstract_key_multiple_press_release_cycles(
        self, mock_keyboard, layer_manager
    ):
        """Test multiple press-release cycles"""
        key = ConcreteKey()

        for i in range(3):
            key.press(layer_manager, mock_keyboard, i * 100)
            assert key._is_pressed is True

            key.release(layer_manager, mock_keyboard, i * 100 + 50)
            assert key._is_pressed is False

        assert key.press_count == 3
        assert key.release_count == 3
