"""
Unit tests for LayerManager functionality.
Tests layer activation, deactivation, and state management.
"""

from mkx.manager_layers import LayersManager


class TestLayersManager:
    """Test suite for LayerManager"""

    def test_layer_manager_initialization(self):
        """Test LayerManager initializes with correct default layer"""
        manager = LayersManager(default_layer=0)

        assert manager.default_layer == 0
        assert manager.get_top_layer() == 0
        assert manager.active_layers == [0]

    def test_layer_manager_custom_default_layer(self):
        """Test LayerManager with custom default layer"""
        manager = LayersManager(default_layer=2)

        assert manager.default_layer == 2
        assert manager.get_top_layer() == 2
        assert manager.active_layers == [2]

    def test_activate_layer(self):
        """Test activating a new layer"""
        manager = LayersManager(default_layer=0)

        manager.activate_layer(1)

        assert manager.get_top_layer() == 1
        assert 1 in manager.active_layers
        assert manager.active_layers == [0, 1]

    def test_activate_multiple_layers(self):
        """Test activating multiple layers"""
        manager = LayersManager(default_layer=0)

        manager.activate_layer(1)
        manager.activate_layer(2)

        assert manager.get_top_layer() == 2
        assert manager.active_layers == [0, 1, 2]

    def test_activate_already_active_layer(self):
        """Test activating an already active layer (without prioritize)"""
        manager = LayersManager(default_layer=0)
        manager.activate_layer(1)

        manager.activate_layer(1)

        # Should not add duplicate
        assert manager.active_layers == [0, 1]

    def test_activate_with_prioritize(self):
        """Test activating layer with prioritize flag moves it to top"""
        manager = LayersManager(default_layer=0)
        manager.activate_layer(1)
        manager.activate_layer(2)

        # Now prioritize layer 1 - should move to end
        manager.activate_layer(1, prioritize=True)

        assert manager.active_layers == [0, 2, 1]
        assert manager.get_top_layer() == 1

    def test_deactivate_layer(self):
        """Test deactivating a layer"""
        manager = LayersManager(default_layer=0)
        manager.activate_layer(1)
        manager.activate_layer(2)

        manager.deactivate_layer(1)

        assert 1 not in manager.active_layers
        assert manager.active_layers == [0, 2]

    def test_cannot_deactivate_default_layer(self):
        """Test that default layer cannot be deactivated"""
        manager = LayersManager(default_layer=0)
        manager.activate_layer(1)

        manager.deactivate_layer(0)

        # Default layer should still be active
        assert 0 in manager.active_layers
        assert manager.active_layers == [0, 1]

    def test_deactivate_nonexistent_layer(self):
        """Test deactivating a layer that's not active does nothing"""
        manager = LayersManager(default_layer=0)
        manager.activate_layer(1)

        manager.deactivate_layer(5)

        assert manager.active_layers == [0, 1]

    def test_set_active_layer(self):
        """Test set_active_layer replaces all layers"""
        manager = LayersManager(default_layer=0)
        manager.activate_layer(1)
        manager.activate_layer(2)

        manager.set_active_layer(3)

        assert manager.active_layers == [3]
        assert manager.get_top_layer() == 3

    def test_set_default_layer(self):
        """Test set_default_layer changes default and updates active layers"""
        manager = LayersManager(default_layer=0)
        manager.set_active_layer(1)

        manager.set_default_layer(2)

        assert manager.default_layer == 2
        # New default should be inserted at beginning if not already present
        assert 2 in manager.active_layers

    def test_toggle_layer_off(self):
        """Test toggling an active layer off"""
        manager = LayersManager(default_layer=0)
        manager.activate_layer(1)

        manager.toggle_layer(1)

        assert 1 not in manager.active_layers

    def test_toggle_layer_on(self):
        """Test toggling an inactive layer on"""
        manager = LayersManager(default_layer=0)

        manager.toggle_layer(1)

        assert 1 in manager.active_layers
        assert manager.get_top_layer() == 1

    def test_toggle_layer_with_prioritize(self):
        """Test toggling layer with prioritize when already active"""
        manager = LayersManager(default_layer=0)
        manager.activate_layer(1)
        manager.activate_layer(2)

        # Toggle layer 1 with prioritize (should move to top since it's active)
        manager.toggle_layer(1, prioritize=True)

        assert manager.active_layers == [0, 2]  # Layer 1 deactivated

    def test_get_top_layer_empty(self):
        """Test get_top_layer with empty active_layers returns default"""
        manager = LayersManager(default_layer=0)
        manager.active_layers = []

        assert manager.get_top_layer() == 0

    def test_status_led_update_on_activate(self):
        """Test that status LED is updated when layer is activated"""
        from unittest.mock import Mock

        manager = LayersManager(default_layer=0)
        mock_led = Mock()
        manager.add_layer_status_led(mock_led)

        manager.activate_layer(1)

        # Status LED update should be called
        assert mock_led.update_status_led.called

    def test_status_led_update_on_deactivate(self):
        """Test that status LED is updated when layer is deactivated"""
        from unittest.mock import Mock

        manager = LayersManager(default_layer=0)
        manager.activate_layer(1)
        mock_led = Mock()
        manager.add_layer_status_led(mock_led)

        manager.deactivate_layer(1)

        # Status LED update should be called
        assert mock_led.update_status_led.called

    def test_complex_layer_sequence(self):
        """Test complex sequence of layer operations"""
        manager = LayersManager(default_layer=0)

        manager.activate_layer(1)
        manager.activate_layer(2)
        assert manager.get_top_layer() == 2

        manager.toggle_layer(2)
        assert manager.get_top_layer() == 1

        manager.activate_layer(3)
        assert manager.get_top_layer() == 3

        manager.deactivate_layer(1)
        assert 1 not in manager.active_layers
        assert manager.get_top_layer() == 3
