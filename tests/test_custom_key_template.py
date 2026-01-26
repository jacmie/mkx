"""
Example test file showing how to write tests for new key types.
Copy and adapt this for testing other key implementations.
"""

from mkx.keys_abstract import KeysAbstract


class CustomKey(KeysAbstract):
    """Example custom key implementation for testing"""

    def __init__(self, name: str):
        super().__init__()
        self.name = name
        self.press_count = 0
        self.release_count = 0

    def on_press(self, layer_manager, keyboard, timestamp):
        self.press_count += 1

    def on_release(self, layer_manager, keyboard, timestamp):
        self.release_count += 1


class TestCustomKey:
    """Example test class for custom key"""

    def test_custom_key_basic(self, layer_manager):
        """Test basic custom key functionality"""
        key = CustomKey("CUSTOM")

        assert key.name == "CUSTOM"
        assert key.press_count == 0
        assert key.release_count == 0

    def test_custom_key_press_release(self, mock_keyboard, layer_manager):
        """Test custom key press and release"""
        key = CustomKey("CUSTOM")

        key.press(layer_manager, mock_keyboard, 0)
        assert key.press_count == 1
        assert key._is_pressed is True

        key.release(layer_manager, mock_keyboard, 100)
        assert key.release_count == 1
        assert key._is_pressed is False

    def test_custom_key_with_timestamps(self, mock_keyboard, layer_manager):
        """Test custom key with various timestamps"""
        key = CustomKey("TIMED")

        timestamps = [0, 100, 200, 300, 500, 1000]

        for i, ts in enumerate(timestamps):
            if i % 2 == 0:
                key.press(layer_manager, mock_keyboard, ts)
            else:
                key.release(layer_manager, mock_keyboard, ts)

        # Should have 3 press and 3 release calls
        assert key.press_count == 3
        assert key.release_count == 3


# Template for testing new key types:
"""
import pytest
from mkx.keys_XXX import KeyXXX
from tests.conftest import MockKeycode


class TestKeyXXX:
    '''Test suite for KeyXXX'''
    
    def test_keyxxx_initialization(self):
        '''Test initialization'''
        key = KeyXXX(...)
        assert key.property == expected_value
    
    def test_keyxxx_press(self, mock_keyboard, layer_manager):
        '''Test press behavior'''
        key = KeyXXX(...)
        key.press(layer_manager, mock_keyboard, 0)
        # Assert expected behavior
    
    def test_keyxxx_release(self, mock_keyboard, layer_manager):
        '''Test release behavior'''
        key = KeyXXX(...)
        key.release(layer_manager, mock_keyboard, 100)
        # Assert expected behavior
"""
