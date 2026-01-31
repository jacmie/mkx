"""
Unit tests for Layer Status LED functionality.
Tests LED status indicators for keyboard layers.
"""

import pytest
from mkx.layer_status_led_abstract import LayerStatusLedAbstract


class ConcreteLayerStatusLED(LayerStatusLedAbstract):
    """Concrete implementation for testing"""

    def __init__(self):
        super().__init__()
        self.updated_layers = []

    def update_status_led(self, layer):
        """Track which layers were updated"""
        self.updated_layers.append(layer)


class TestLayerStatusLEDAbstract:
    """Test suite for LayerStatusLedAbstract"""

    def test_led_initialization(self):
        """Test LED initializes correctly"""
        led = ConcreteLayerStatusLED()

        assert led is not None

    def test_led_update_status(self):
        """Test LED responds to status update"""
        led = ConcreteLayerStatusLED()

        led.update_status_led(0)

        assert len(led.updated_layers) == 1
        assert led.updated_layers[0] == 0

    def test_led_multiple_updates(self):
        """Test LED handles multiple status updates"""
        led = ConcreteLayerStatusLED()

        led.update_status_led(0)
        led.update_status_led(1)
        led.update_status_led(2)

        assert len(led.updated_layers) == 3
        assert led.updated_layers == [0, 1, 2]

    def test_abstract_led_cannot_instantiate(self):
        """Test that abstract LED raises NotImplementedError"""
        led = LayerStatusLedAbstract()

        with pytest.raises(NotImplementedError):
            led.update_status_led(0)
