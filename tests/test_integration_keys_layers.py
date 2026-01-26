"""
Integration test example: Testing key communication with layer manager and keyboard
"""

from mkx.keys_standard import KeysStandard
from tests.conftest import MockKeycode


class TestKeysWithLayerIntegration:
    """Integration tests combining keys with layer management"""

    def test_key_press_changes_layer(self, mock_keyboard, layer_manager):
        """Test pressing a key while on different layers"""
        key_a = KeysStandard(MockKeycode.A, "A")
        key_b = KeysStandard(MockKeycode.B, "B")

        # Start on layer 0
        assert layer_manager.get_top_layer() == 0

        key_a.press(layer_manager, mock_keyboard, 0)
        assert MockKeycode.A in mock_keyboard.pressed_keys

        # Switch to layer 1
        layer_manager.activate_layer(1)
        assert layer_manager.get_top_layer() == 1

        # Press different key on layer 1
        key_a.release(layer_manager, mock_keyboard, 100)
        key_b.press(layer_manager, mock_keyboard, 100)

        assert MockKeycode.B in mock_keyboard.pressed_keys
        assert MockKeycode.A not in mock_keyboard.pressed_keys

    def test_simultaneous_keys_different_layers(self, mock_keyboard, layer_manager):
        """Test multiple keys pressed with layer switching"""
        key_a = KeysStandard(MockKeycode.A, "A")
        key_b = KeysStandard(MockKeycode.B, "B")
        key_c = KeysStandard(MockKeycode.C, "C")

        # Press A on layer 0
        key_a.press(layer_manager, mock_keyboard, 0)
        assert MockKeycode.A in mock_keyboard.pressed_keys

        # Switch to layer 1 and press B
        layer_manager.activate_layer(1)
        key_b.press(layer_manager, mock_keyboard, 50)

        # Should have both A and B pressed
        assert MockKeycode.A in mock_keyboard.pressed_keys
        assert MockKeycode.B in mock_keyboard.pressed_keys

        # Switch to layer 2
        layer_manager.activate_layer(2)
        key_c.press(layer_manager, mock_keyboard, 100)

        # All three should be pressed
        assert mock_keyboard.press_count >= 3

    def test_key_release_on_layer_change(self, mock_keyboard, layer_manager):
        """Test that changing layers doesn't affect key state"""
        key = KeysStandard(MockKeycode.A, "A")

        key.press(layer_manager, mock_keyboard, 0)

        # Change layers
        layer_manager.activate_layer(1)
        layer_manager.activate_layer(2)

        # Key should still be pressed
        assert key._is_pressed is True
        assert MockKeycode.A in mock_keyboard.pressed_keys

        # Now release
        key.release(layer_manager, mock_keyboard, 100)
        assert key._is_pressed is False

    def test_multiple_layer_toggles_with_keys(self, mock_keyboard, layer_manager):
        """Test rapid layer toggling with key presses"""
        key_a = KeysStandard(MockKeycode.A, "A")
        key_b = KeysStandard(MockKeycode.B, "B")

        key_a.press(layer_manager, mock_keyboard, 0)
        assert layer_manager.get_top_layer() == 0

        for i in range(1, 5):
            layer_manager.activate_layer(i)
            assert layer_manager.get_top_layer() == i

        # Key should still be active
        assert key_a._is_pressed is True

        # Release and check final state
        key_a.release(layer_manager, mock_keyboard, 500)
        assert key_a._is_pressed is False

    def test_keyboard_state_consistency(self, mock_keyboard, layer_manager):
        """Test keyboard maintains consistent state across layer changes"""
        keys = [
            KeysStandard(MockKeycode.A, "A"),
            KeysStandard(MockKeycode.B, "B"),
            KeysStandard(MockKeycode.C, "C"),
        ]

        # Press all keys
        for i, key in enumerate(keys):
            key.press(layer_manager, mock_keyboard, i * 10)

        assert mock_keyboard.press_count == 3

        # Change layers multiple times
        for layer in range(1, 4):
            layer_manager.activate_layer(layer)

        # All keys should still be pressed
        for key in keys:
            assert key._is_pressed is True

        # Release all
        for i, key in enumerate(keys):
            key.release(layer_manager, mock_keyboard, 100 + i * 10)

        assert all(not key._is_pressed for key in keys)


class TestComplexKeyboardScenarios:
    """Test realistic keyboard usage scenarios"""

    def test_typing_with_layers(self, mock_keyboard, layer_manager):
        """Simulate typing on multiple layers"""
        # Layer 0: alphabetic keys
        keys_alpha = {
            "a": KeysStandard(MockKeycode.A, "A"),
            "b": KeysStandard(MockKeycode.B, "B"),
            "c": KeysStandard(MockKeycode.C, "C"),
        }

        # Layer 1: number keys (different mapping)
        keys_numbers = {
            "a": KeysStandard(MockKeycode.A, "A"),  # Can be same or different
        }

        # Simulate typing "abc" on layer 0
        sequence = [
            (0, "a", 0, 50),  # (layer, key, press_time, release_time)
            (0, "b", 60, 110),
            (0, "c", 120, 170),
        ]

        for layer, key_name, press_t, release_t in sequence:
            if layer != layer_manager.get_top_layer():
                layer_manager.set_active_layer(layer)

            keys_alpha[key_name].press(layer_manager, mock_keyboard, press_t)
            keys_alpha[key_name].release(layer_manager, mock_keyboard, release_t)

        # Should have recorded 3 key presses
        assert mock_keyboard.press_count == 3

    def test_layer_switching_with_modifiers(self, mock_keyboard, layer_manager):
        """Test switching layers while modifier keys are active"""
        base_key = KeysStandard(MockKeycode.A, "A")
        modifier = KeysStandard(MockKeycode.TAB, "MOD")

        # Press modifier
        modifier.press(layer_manager, mock_keyboard, 0)
        assert MockKeycode.TAB in mock_keyboard.pressed_keys

        # Switch layers
        layer_manager.activate_layer(1)
        layer_manager.activate_layer(2)

        # Modifier should still be active
        assert MockKeycode.TAB in mock_keyboard.pressed_keys

        # Press base key on new layer
        base_key.press(layer_manager, mock_keyboard, 100)

        # Both should be active
        assert MockKeycode.TAB in mock_keyboard.pressed_keys
        assert MockKeycode.A in mock_keyboard.pressed_keys
