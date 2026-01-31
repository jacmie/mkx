"""
Unit tests for Communication Message functionality.
Tests message parsing, encoding, and synchronization.
"""

from mkx.communication_message import (
    MessageParser,
    encode_message,
    sync_messages,
    debounce,
)


class TestMessageParser:
    """Test suite for MessageParser class"""

    def test_message_parser_initialization(self):
        """Test MessageParser initializes correctly"""
        parser = MessageParser()

        assert parser.buffer == b""
        assert parser.max_message_size == 256

    def test_message_parser_custom_max_size(self):
        """Test MessageParser with custom max message size"""
        parser = MessageParser(max_message_size=512)

        assert parser.max_message_size == 512

    def test_message_parser_empty_data(self):
        """Test MessageParser with empty data"""
        parser = MessageParser()

        result = parser.parse(b"")

        assert result == []
        assert parser.buffer == b""

    def test_message_parser_partial_message(self):
        """Test MessageParser with partial message"""
        parser = MessageParser()

        # Just header + length (3 bytes), not complete
        result = parser.parse(b"\xb2\x00\x10")

        # Should wait for more data
        assert result == []
        assert len(parser.buffer) == 3


class TestEncodeMessage:
    """Test suite for encode_message function"""

    def test_encode_message_basic(self):
        """Test basic message encoding"""
        device_id = "device1"
        msg_type = "key_event"
        data = {"col": 0, "row": 1}

        encoded = encode_message(device_id, msg_type, data)

        # Should start with header byte
        assert encoded[0] == 0xB2

    def test_encode_message_structure(self):
        """Test message structure contains required fields"""
        device_id = "test_device"
        msg_type = "test_type"
        data = {"field": "value"}

        encoded = encode_message(device_id, msg_type, data, verbose=False)

        # Verify basic structure
        assert len(encoded) > 5  # Header(1) + Length(2) + Payload + Checksum(1)

    def test_encode_message_different_types(self):
        """Test encoding messages with different types"""
        types = ["key_event", "config_update", "status"]
        data = {"test": True}

        for msg_type in types:
            encoded = encode_message("device1", msg_type, data)
            assert isinstance(encoded, bytes)
            assert encoded[0] == 0xB2

    def test_encode_message_empty_data(self):
        """Test encoding message with empty data"""
        encoded = encode_message("device1", "test", {})

        assert isinstance(encoded, bytes)
        assert encoded[0] == 0xB2


class TestSyncMessages:
    """Test suite for sync_messages function"""

    def test_sync_messages_single_message(self):
        """Test syncing single message"""
        message = {
            "timestamp": 1000,
            "device_id": "device1",
            "type": "key_event",
            "data": [],
        }

        result = sync_messages([message], 2000)

        assert len(result) == 1
        assert result[0]["device_id"] == "device1"

    def test_sync_messages_multiple_devices(self):
        """Test syncing messages from multiple devices"""
        messages = [
            {
                "timestamp": 1000,
                "device_id": "device1",
                "type": "key_event",
                "data": [],
            },
            {
                "timestamp": 1100,
                "device_id": "device2",
                "type": "key_event",
                "data": [],
            },
        ]

        result = sync_messages(messages, 2000)

        assert len(result) == 2

    def test_sync_messages_sorted_by_timestamp(self):
        """Test that synced messages are sorted by timestamp"""
        messages = [
            {
                "timestamp": 2000,
                "device_id": "device1",
                "type": "key_event",
                "data": [],
            },
            {
                "timestamp": 1000,
                "device_id": "device1",
                "type": "key_event",
                "data": [],
            },
        ]

        result = sync_messages(messages, 3000)

        # Should be sorted by adjusted timestamp
        assert result[0]["timestamp"] <= result[1]["timestamp"]

    def test_sync_messages_empty_list(self):
        """Test syncing empty message list"""
        result = sync_messages([], 1000)

        assert result == []


class TestDebounce:
    """Test suite for debounce function"""

    def test_debounce_empty_messages(self):
        """Test debouncing empty message list"""
        result = debounce([])

        assert result == []

    def test_debounce_non_key_events(self):
        """Test that non-key events are ignored"""
        messages = [
            {"timestamp": 1000, "device_id": "device1", "type": "status", "data": []}
        ]

        result = debounce(messages)

        # Non-key events should be ignored
        assert result == []

    def test_debounce_key_event_structure(self):
        """Test debouncing key event with correct structure"""
        messages = [
            {
                "timestamp": 1000,
                "device_id": "device1",
                "type": "key_event",
                "data": ["0", "1", "true"],
            }
        ]

        result = debounce(messages)

        assert len(result) > 0
        assert result[0]["col"] == 0
        assert result[0]["row"] == 1
        assert result[0]["pressed"] is True

    def test_debounce_state_transition(self):
        """Test debouncing with state transitions"""
        messages = [
            {
                "timestamp": 1000,
                "device_id": "device1",
                "type": "key_event",
                "data": ["0", "0", "true"],
            },
            {
                "timestamp": 1020,
                "device_id": "device1",
                "type": "key_event",
                "data": ["0", "0", "false"],
            },
        ]

        result = debounce(messages)

        # Both should be included if time difference exceeds debounce threshold
        assert len(result) >= 1
