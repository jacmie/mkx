"""
Unit tests for Backlight Abstract base class.
Tests backlight abstraction for keyboard lighting.
"""

import pytest
from mkx.backlight_abstract import BacklightAbstract


class ConcreteBacklight(BacklightAbstract):
    """Concrete implementation of BacklightAbstract for testing"""

    def __init__(self):
        self.shine_called = False

    def shine(self):
        self.shine_called = True


class TestBacklightAbstract:
    """Test suite for BacklightAbstract"""

    def test_backlight_initialization(self):
        """Test backlight initializes correctly"""
        backlight = ConcreteBacklight()

        assert backlight.shine_called is False

    def test_backlight_shine(self):
        """Test backlight shine method"""
        backlight = ConcreteBacklight()

        backlight.shine()

        assert backlight.shine_called is True

    def test_abstract_backlight_not_implemented(self):
        """Test that abstract backlight raises NotImplementedError"""
        backlight = BacklightAbstract()

        with pytest.raises(NotImplementedError):
            backlight.shine()
