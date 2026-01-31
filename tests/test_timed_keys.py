"""
Unit tests for Timed Keys functionality.
Tests time-based key behavior and timing management.
"""

import pytest
from unittest.mock import MagicMock
from mkx.timed_keys import TimedKeys, TimedKeysManager


class ConcreteTimedKey(TimedKeys):
    """Concrete implementation of TimedKeys for testing"""

    def __init__(self):
        super().__init__()
        self.check_time_called = False

    def check_time(self, layers_manager, keyboard, timestamp):
        self.check_time_called = True


class TestTimedKeys:
    """Test suite for TimedKeys"""

    def test_timed_key_initialization(self):
        """Test TimedKeys initializes correctly"""
        key = ConcreteTimedKey()

        assert key._active is False
        assert key._pressed_time is None

    def test_timed_key_start_timer(self):
        """Test TimedKeys start_timer"""
        key = ConcreteTimedKey()

        key.start_timer(1000)

        assert key._active is True
        assert key._pressed_time == 1000

    def test_timed_key_stop_timer(self):
        """Test TimedKeys stop_timer"""
        key = ConcreteTimedKey()

        key.start_timer(1000)
        assert key._active is True

        key.stop_timer()

        assert key._active is False
        assert key._pressed_time is None

    def test_timed_key_timer_lifecycle(self):
        """Test full timer lifecycle"""
        key = ConcreteTimedKey()

        key.start_timer(1000)
        assert key._active is True
        assert key._pressed_time == 1000

        key.stop_timer()
        assert key._active is False

    def test_timed_key_multiple_timers(self):
        """Test multiple timer start-stop cycles"""
        key = ConcreteTimedKey()

        # First cycle
        key.start_timer(1000)
        assert key._pressed_time == 1000
        key.stop_timer()

        # Second cycle
        key.start_timer(2000)
        assert key._pressed_time == 2000
        key.stop_timer()

    def test_timed_key_check_time_not_implemented(self):
        """Test that check_time must be implemented"""
        key = TimedKeys()

        with pytest.raises(NotImplementedError):
            key.check_time(None, None, 1000)

    def test_concrete_check_time(self):
        """Test concrete implementation of check_time"""
        key = ConcreteTimedKey()

        key.check_time(None, None, 1000)

        assert key.check_time_called is True


class TestTimedKeysManager:
    """Test suite for TimedKeysManager"""

    def test_timed_keys_manager_initialization(self):
        """Test TimedKeysManager initializes correctly"""
        manager = TimedKeysManager()

        assert manager._active_keys == set()

    def test_register_timed_key(self):
        """Test registering a timed key"""
        key = ConcreteTimedKey()
        manager = TimedKeysManager()

        manager.register(key)

        assert key in manager._active_keys

    def test_register_non_timed_key(self):
        """Test registering a non-TimedKeys key (should not be added)"""
        manager = TimedKeysManager()

        # Create a mock key that's not a TimedKeys
        mock_key = MagicMock()

        manager.register(mock_key)

        # Non-TimedKeys should not be added
        assert len(manager._active_keys) == 0

    def test_update_calls_check_time(self):
        """Test that update calls check_time on registered keys"""
        key = ConcreteTimedKey()
        manager = TimedKeysManager()

        manager.register(key)
        key._active = True

        manager.update(None, None, 1000)

        assert key.check_time_called is True

    def test_update_removes_inactive_keys(self):
        """Test that update removes inactive keys"""
        key = ConcreteTimedKey()
        manager = TimedKeysManager()

        manager.register(key)
        key._active = True

        # Make the key inactive
        key._active = False

        manager.update(None, None, 1000)

        # Key should be removed from active set
        assert key not in manager._active_keys

    def test_update_empty_manager(self):
        """Test update with no registered keys"""
        manager = TimedKeysManager()

        # Should not raise an error
        manager.update(None, None, 1000)
