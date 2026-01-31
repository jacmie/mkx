"""
Unit tests for Periphery Abstract base class.
Tests periphery abstraction for matrix scanning and communication.
"""

import pytest
from unittest.mock import MagicMock, patch
from mkx.periphery_abstract import PeripheryAbstract
from mkx.diode_orientation import DiodeOrientation


class ConcretePeriphery(PeripheryAbstract):
    """Concrete implementation of PeripheryAbstract for testing"""

    def __init__(self, device_id, col_pins, row_pins, **kwargs):
        with patch('mkx.matrix_scanner.MatrixScanner'):
            super().__init__(device_id, col_pins, row_pins, **kwargs)
        self.sent_messages = []

    def receive(self, verbose=False):
        return []

    def send(self, msg_type, data, verbose=False):
        self.sent_messages.append({"type": msg_type, "data": data})


class TestPeripheryAbstract:
    """Test suite for PeripheryAbstract"""

    def test_periphery_initialization(self):
        """Test periphery initializes correctly"""
        col_pins = [MagicMock() for _ in range(3)]
        row_pins = [MagicMock() for _ in range(4)]

        periphery = ConcretePeriphery("device1", col_pins, row_pins)

        assert periphery.device_id == "device1"

    def test_periphery_device_id_default(self):
        """Test periphery with default device_id"""
        col_pins = [MagicMock()]
        row_pins = [MagicMock()]

        periphery = ConcretePeriphery(None, col_pins, row_pins)

        assert periphery.device_id == "unknown"

    def test_periphery_diode_orientation(self):
        """Test periphery accepts diode orientation"""
        col_pins = [MagicMock()]
        row_pins = [MagicMock()]

        periphery = ConcretePeriphery(
            "device1",
            col_pins,
            row_pins,
            diode_orientation=DiodeOrientation.ROW2COL
        )

        assert periphery.device_id == "device1"

    def test_periphery_get_key_events(self):
        """Test periphery get_key_events delegates to matrix_scanner"""
        col_pins = [MagicMock()]
        row_pins = [MagicMock()]

        periphery = ConcretePeriphery("device1", col_pins, row_pins)
        periphery.matrix_scanner.get_key_events = MagicMock(return_value=[(0, 0, True)])

        events = periphery.get_key_events()

        assert len(events) == 1

    def test_periphery_send_message(self):
        """Test periphery send method"""
        col_pins = [MagicMock()]
        row_pins = [MagicMock()]

        periphery = ConcretePeriphery("device1", col_pins, row_pins)

        periphery.send("test_type", {"key": "value"})

        assert len(periphery.sent_messages) == 1
        assert periphery.sent_messages[0]["type"] == "test_type"

    def test_periphery_receive_message(self):
        """Test periphery receive method"""
        col_pins = [MagicMock()]
        row_pins = [MagicMock()]

        periphery = ConcretePeriphery("device1", col_pins, row_pins)

        messages = periphery.receive()

        assert messages == []

    def test_abstract_periphery_receive_not_implemented(self):
        """Test that abstract receive raises NotImplementedError"""
        col_pins = [MagicMock()]
        row_pins = [MagicMock()]

        with patch('mkx.matrix_scanner.MatrixScanner'):
            periphery = PeripheryAbstract("device1", col_pins, row_pins)

        with pytest.raises(NotImplementedError):
            periphery.receive()

    def test_abstract_periphery_send_not_implemented(self):
        """Test that abstract send raises NotImplementedError"""
        col_pins = [MagicMock()]
        row_pins = [MagicMock()]

        with patch('mkx.matrix_scanner.MatrixScanner'):
            periphery = PeripheryAbstract("device1", col_pins, row_pins)

        with pytest.raises(NotImplementedError):
            periphery.send("test", {})
