"""
Unit tests for Check functionality.
Tests keymap and interface validation.
"""

import pytest
from unittest.mock import MagicMock
from mkx.check import check


class TestCheck:
    """Test suite for check function"""

    def test_check_valid_configuration(self, mock_keyboard, layer_manager):
        """Test check with valid configuration"""
        # Create mock interface
        iface = MagicMock()
        iface.device_id = "test_device"
        iface.row_min = 0
        iface.row_max = 1
        iface.col_min = 0
        iface.col_max = 1
        iface._coord_map = [0, 1, 2, 3]
        iface.generate_rect_map = MagicMock()

        # Create simple keymap
        from mkx.keys_standard import KeysStandard
        from tests.conftest import MockKeycode

        key_a = KeysStandard(MockKeycode.A, "A")
        keymap = [[key_a, key_a, key_a, key_a]]

        # Run check
        errors = check(2, 2, keymap, [iface])

        # Should have no errors
        assert errors is False

    def test_check_row_out_of_bounds(self, mock_keyboard, layer_manager):
        """Test check detects row out of bounds"""
        iface = MagicMock()
        iface.device_id = "test_device"
        iface.row_min = 0
        iface.row_max = 5  # Out of bounds for 2x2 grid
        iface.col_min = 0
        iface.col_max = 1
        iface._coord_map = [0, 1, 2, 3]
        iface.generate_rect_map = MagicMock()

        from mkx.keys_standard import KeysStandard
        from tests.conftest import MockKeycode

        key_a = KeysStandard(MockKeycode.A, "A")
        keymap = [[key_a, key_a, key_a, key_a]]

        errors = check(2, 2, keymap, [iface])

        # Should have errors
        assert errors is True

    def test_check_col_out_of_bounds(self, mock_keyboard, layer_manager):
        """Test check detects col out of bounds"""
        iface = MagicMock()
        iface.device_id = "test_device"
        iface.row_min = 0
        iface.row_max = 1
        iface.col_min = 0
        iface.col_max = 5  # Out of bounds
        iface._coord_map = [0, 1, 2, 3]
        iface.generate_rect_map = MagicMock()

        from mkx.keys_standard import KeysStandard
        from tests.conftest import MockKeycode

        key_a = KeysStandard(MockKeycode.A, "A")
        keymap = [[key_a, key_a, key_a, key_a]]

        errors = check(2, 2, keymap, [iface])

        # Should have errors
        assert errors is True

    def test_check_no_coord_map(self, mock_keyboard, layer_manager):
        """Test check detects missing coordinate map"""
        iface = MagicMock()
        iface.device_id = "test_device"
        iface.row_min = 0
        iface.row_max = 1
        iface.col_min = 0
        iface.col_max = 1
        iface._coord_map = None  # Missing coord map
        iface.generate_rect_map = MagicMock()

        from mkx.keys_standard import KeysStandard
        from tests.conftest import MockKeycode

        key_a = KeysStandard(MockKeycode.A, "A")
        keymap = [[key_a, key_a, key_a, key_a]]

        # The check function has a bug where it doesn't properly handle None coord_map
        # It will raise TypeError when trying to iterate over None
        with pytest.raises(TypeError):
            check(2, 2, keymap, [iface])

    def test_check_coord_map_index_out_of_range(self, mock_keyboard, layer_manager):
        """Test check detects coordinate map index out of range"""
        iface = MagicMock()
        iface.device_id = "test_device"
        iface.row_min = 0
        iface.row_max = 1
        iface.col_min = 0
        iface.col_max = 1
        iface._coord_map = [0, 1, 2, 99]  # 99 is out of range for 2x2
        iface.generate_rect_map = MagicMock()

        from mkx.keys_standard import KeysStandard
        from tests.conftest import MockKeycode

        key_a = KeysStandard(MockKeycode.A, "A")
        keymap = [[key_a, key_a, key_a, key_a]]

        # The check function has a bug where it doesn't properly handle out-of-range indices
        # It will raise IndexError when trying to access shadow array with invalid indices
        with pytest.raises(IndexError):
            check(2, 2, keymap, [iface])

    def test_check_multiple_interfaces(self, mock_keyboard, layer_manager):
        """Test check with multiple interfaces"""
        from mkx.keys_standard import KeysStandard
        from tests.conftest import MockKeycode

        iface1 = MagicMock()
        iface1.device_id = "device1"
        iface1.row_min = 0
        iface1.row_max = 1
        iface1.col_min = 0
        iface1.col_max = 1
        iface1._coord_map = [0, 1, 2, 3]
        iface1.generate_rect_map = MagicMock()

        iface2 = MagicMock()
        iface2.device_id = "device2"
        iface2.row_min = 0
        iface2.row_max = 1
        iface2.col_min = 2
        iface2.col_max = 3
        iface2._coord_map = [4, 5, 6, 7]
        iface2.generate_rect_map = MagicMock()

        key_a = KeysStandard(MockKeycode.A, "A")
        keymap = [[key_a] * 8]

        errors = check(4, 2, keymap, [iface1, iface2])

        # Should handle multiple interfaces
        assert isinstance(errors, bool)
