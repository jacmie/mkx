"""
Unit tests for Interface Abstract base class.
Tests interface abstraction for device communication.
"""

import pytest
from mkx.interface_abstract import InterfaceAbstract


class ConcreteInterface(InterfaceAbstract):
    """Concrete implementation of InterfaceAbstract for testing"""

    def __init__(self, device_id, col_min, row_min, col_max, row_max):
        super().__init__(device_id, col_min, row_min, col_max, row_max)
        self._connected = True

    def is_connected(self):
        return self._connected

    def reconnect(self):
        self._connected = True

    def receive(self, verbose=False):
        return []

    def send(self, msg_type, data, verbose=False):
        pass


class TestInterfaceAbstract:
    """Test suite for InterfaceAbstract"""

    def test_interface_initialization(self):
        """Test interface initializes correctly"""
        iface = ConcreteInterface("device1", 0, 0, 3, 3)

        assert iface.device_id == "device1"
        assert iface.col_min == 0
        assert iface.row_min == 0
        assert iface.col_max == 3
        assert iface.row_max == 3

    def test_interface_num_rows_cols(self):
        """Test num_rows and num_cols calculation"""
        iface = ConcreteInterface("device1", 0, 0, 3, 2)

        assert iface.num_rows == 3  # 0, 1, 2 = 3 rows
        assert iface.num_cols == 4  # 0, 1, 2, 3 = 4 cols

    def test_interface_set_coord_map(self):
        """Test setting coordinate map"""
        iface = ConcreteInterface("device1", 0, 0, 1, 1)

        coord_list = [0, 1, 2, 3]
        iface.set_coord_map(coord_list)

        assert iface._coord_map == coord_list

    def test_interface_set_coord_map_wrong_size(self):
        """Test that wrong coord_map size raises error"""
        iface = ConcreteInterface("device1", 0, 0, 1, 1)

        # 2x2 = 4 expected, but providing 3
        with pytest.raises(ValueError):
            iface.set_coord_map([0, 1, 2])

    def test_interface_logical_index(self):
        """Test logical_index conversion"""
        iface = ConcreteInterface("device1", 0, 0, 1, 1)
        iface.set_coord_map([0, 1, 2, 3])

        # Local (0,0) should map to index 0
        assert iface.logical_index(0, 0) == 0
        # Local (1,0) should map to index 1
        assert iface.logical_index(1, 0) == 1
        # Local (0,1) should map to index 2
        assert iface.logical_index(0, 1) == 2
        # Local (1,1) should map to index 3
        assert iface.logical_index(1, 1) == 3

    def test_interface_logical_index_out_of_bounds(self):
        """Test logical_index with out of bounds access"""
        iface = ConcreteInterface("device1", 0, 0, 1, 1)
        iface.set_coord_map([0, 1, 2, 3])

        with pytest.raises(IndexError):
            iface.logical_index(2, 2)

    def test_interface_generate_rect_map(self):
        """Test generate_rect_map"""
        iface = ConcreteInterface("device1", 0, 0, 2, 1)
        iface.generate_rect_map(3)  # Keymap width = 3

        # Should generate map for 2x3 grid
        assert len(iface._coord_map) == 6

    def test_interface_is_connected(self):
        """Test is_connected"""
        iface = ConcreteInterface("device1", 0, 0, 1, 1)

        assert iface.is_connected() is True

    def test_interface_reconnect(self):
        """Test reconnect"""
        iface = ConcreteInterface("device1", 0, 0, 1, 1)

        iface._connected = False
        assert iface.is_connected() is False

        iface.reconnect()
        assert iface.is_connected() is True

    def test_interface_ensure_connection(self):
        """Test ensure_connection"""
        iface = ConcreteInterface("device1", 0, 0, 1, 1)

        result = iface.ensure_connection()

        # Should return True when connected
        assert result is True

    def test_interface_abstract_methods(self):
        """Test that abstract methods raise NotImplementedError"""
        iface = InterfaceAbstract("device1", 0, 0, 1, 1)

        with pytest.raises(NotImplementedError):
            iface.is_connected()

        with pytest.raises(NotImplementedError):
            iface.reconnect()

        with pytest.raises(NotImplementedError):
            iface.receive()

        with pytest.raises(NotImplementedError):
            iface.send("test", {})
