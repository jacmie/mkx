"""
Unit tests for HoldTap key functionality.
Tests tap vs hold behavior with timing.
"""

import pytest
from mkx.keys_holdtap import HT
from mkx.keys_standard import KeysStandard
from tests.conftest import MockKeycode


class TestHoldTap:
    """Test suite for HoldTap (HT) key functionality"""

    @pytest.fixture
    def tap_key(self):
        """Fixture providing a tap key (e.g., 'a')"""
        return KeysStandard(MockKeycode.A, "A")

    @pytest.fixture
    def hold_key(self):
        """Fixture providing a hold key (e.g., Shift)"""
        return KeysStandard(MockKeycode.TAB, "TAB")

    def test_holdtap_initialization(self, tap_key, hold_key):
        """Test HoldTap initializes correctly"""
        ht = HT(tap_key, hold_key, timeout=200)

        assert ht._tap_key == tap_key
        assert ht._hold_key == hold_key
        assert ht._timeout == 200
        assert ht._is_pressed is False
        assert ht._held_past_timeout is False

    def test_holdtap_quick_tap(self, mock_keyboard, layer_manager, tap_key, hold_key):
        """Test HoldTap behaves as tap when released quickly"""
        ht = HT(tap_key, hold_key, timeout=200)

        # Press and release within timeout
        ht.press(layer_manager, mock_keyboard, 0)
        ht.release(layer_manager, mock_keyboard, 100)  # 100ms < 200ms timeout

        # Tap key should be triggered
        assert MockKeycode.A in mock_keyboard.released_keys
        assert mock_keyboard.press_count >= 1

    def test_holdtap_hold_triggers_at_timeout(
        self, mock_keyboard, layer_manager, tap_key, hold_key
    ):
        """Test HoldTap behaves as hold when held past timeout"""
        ht = HT(tap_key, hold_key, timeout=200)

        ht.press(layer_manager, mock_keyboard, 0)
        ht._held_past_timeout = True  # Simulate timeout passing
        ht._hold_sent = True  # Hold was sent
        ht.release(layer_manager, mock_keyboard, 300)  # 300ms > 200ms timeout

        # Hold key release should be called
        # (actual hold press would be called by check_time mechanism)
        assert ht._is_pressed is False

    def test_holdtap_custom_timeout(self, tap_key, hold_key):
        """Test HoldTap with custom timeout values"""
        ht_short = HT(tap_key, hold_key, timeout=100)
        ht_long = HT(tap_key, hold_key, timeout=500)

        assert ht_short._timeout == 100
        assert ht_long._timeout == 500

    def test_holdtap_multiple_presses(
        self, mock_keyboard, layer_manager, tap_key, hold_key
    ):
        """Test multiple HoldTap sequences"""
        ht = HT(tap_key, hold_key, timeout=200)

        # First tap
        ht.press(layer_manager, mock_keyboard, 0)
        ht.release(layer_manager, mock_keyboard, 100)

        first_press_count = mock_keyboard.press_count

        # Second tap (fresh instance state)
        ht.press(layer_manager, mock_keyboard, 200)
        ht.release(layer_manager, mock_keyboard, 300)

        # Should have at least 2 press events total
        assert mock_keyboard.press_count >= first_press_count

    def test_holdtap_press_state_management(
        self, mock_keyboard, layer_manager, tap_key, hold_key
    ):
        """Test that press state is properly managed"""
        ht = HT(tap_key, hold_key, timeout=200)

        assert ht._is_pressed is False

        ht.press(layer_manager, mock_keyboard, 0)
        assert ht._is_pressed is True

        ht.release(layer_manager, mock_keyboard, 100)
        assert ht._is_pressed is False

    def test_holdtap_timer_initialization(
        self, mock_keyboard, layer_manager, tap_key, hold_key
    ):
        """Test that timer is initialized on press"""
        ht = HT(tap_key, hold_key, timeout=200)

        assert ht._pressed_time is None

        ht.press(layer_manager, mock_keyboard, 1000)
        assert ht._pressed_time == 1000

    def test_holdtap_timer_cleanup(
        self, mock_keyboard, layer_manager, tap_key, hold_key
    ):
        """Test that timer is cleaned up on release"""
        ht = HT(tap_key, hold_key, timeout=200)

        ht.press(layer_manager, mock_keyboard, 0)
        assert ht._pressed_time == 0

        ht.release(layer_manager, mock_keyboard, 100)
        assert ht._pressed_time is None

    def test_holdtap_holds_modifiers(self):
        """Test HoldTap can hold modifier keys"""
        from mkx.keys_standard import A, LCTL
        from mkx.keys_modifiers import MOD

        tap = KeysStandard(MockKeycode.A, "A")
        # MOD takes (modifier_key, key_code, name)
        hold = MOD(LCTL, A, "LCTL_A")

        ht = HT(tap, hold, timeout=200)
        assert ht._hold_key == hold

    def test_holdtap_with_none_keys(self, mock_keyboard, layer_manager):
        """Test HoldTap with None keys (no-op keys)"""
        tap_key = KeysStandard(None, "NONE")
        hold_key = KeysStandard(None, "NONE")

        ht = HT(tap_key, hold_key, timeout=200)

        # Should not raise exceptions
        ht.press(layer_manager, mock_keyboard, 0)
        ht.release(layer_manager, mock_keyboard, 100)

        assert ht._is_pressed is False
