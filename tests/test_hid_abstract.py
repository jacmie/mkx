"""
Unit tests for HID Abstract base class.
Tests HID device interface implementation.
"""

import pytest
from mkx.hid_abstract import HID_abstract


class ConcreteHIDDevice(HID_abstract):
    """Concrete implementation of HID_abstract for testing"""

    def __init__(self):
        self.sent_keys = []

    def send_key(self, keycode: int, pressed: bool):
        self.sent_keys.append((keycode, pressed))


class TestHIDAbstract:
    """Test suite for HID_abstract base class"""

    def test_hid_abstract_cannot_instantiate(self):
        """Test that HID_abstract cannot be directly instantiated"""
        hid = HID_abstract()

        # Should raise NotImplementedError when calling send_key
        with pytest.raises(NotImplementedError):
            hid.send_key(0x04, True)

    def test_hid_abstract_send_key_not_implemented(self):
        """Test that send_key raises NotImplementedError"""
        hid = HID_abstract()

        with pytest.raises(
            NotImplementedError,
            match="Subclass of the HID_abstract must implement send_key",
        ):
            hid.send_key(123, True)

    def test_concrete_hid_device_send_key_press(self):
        """Test concrete HID device sends key press"""
        hid = ConcreteHIDDevice()

        hid.send_key(0x04, True)

        assert len(hid.sent_keys) == 1
        assert hid.sent_keys[0] == (0x04, True)

    def test_concrete_hid_device_send_key_release(self):
        """Test concrete HID device sends key release"""
        hid = ConcreteHIDDevice()

        hid.send_key(0x04, False)

        assert len(hid.sent_keys) == 1
        assert hid.sent_keys[0] == (0x04, False)

    def test_concrete_hid_device_multiple_keys(self):
        """Test concrete HID device sends multiple keys"""
        hid = ConcreteHIDDevice()

        hid.send_key(0x04, True)  # A press
        hid.send_key(0x05, True)  # B press
        hid.send_key(0x04, False)  # A release
        hid.send_key(0x05, False)  # B release

        assert len(hid.sent_keys) == 4
        assert hid.sent_keys[0] == (0x04, True)
        assert hid.sent_keys[1] == (0x05, True)
        assert hid.sent_keys[2] == (0x04, False)
        assert hid.sent_keys[3] == (0x05, False)

    def test_hid_device_zero_keycode(self):
        """Test HID device with zero keycode"""
        hid = ConcreteHIDDevice()

        hid.send_key(0, True)

        assert hid.sent_keys[0] == (0, True)

    def test_hid_device_large_keycode(self):
        """Test HID device with large keycode value"""
        hid = ConcreteHIDDevice()

        hid.send_key(255, True)

        assert hid.sent_keys[0] == (255, True)
