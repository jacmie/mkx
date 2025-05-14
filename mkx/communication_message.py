import time
import json
from collections import OrderedDict


class MessageParser:
    REQUIRED_FIELDS = ["timestamp", "device_id", "type"]

    def __init__(self):
        self.buffer = b""

    def parse(self, new_data: bytes, verbose=False) -> list[dict]:
        messages = []
        self.buffer += new_data
        while b"\n" in self.buffer:
            line, self.buffer = self.buffer.split(b"\n", 1)
            try:
                line_str = line.decode().strip()

                if verbose:
                    print("receive:", line_str)  # Keeps the order of the sent message

                msg = json.loads(line_str)  # After this json order may be lost

                if self._validate_message(msg):
                    messages.append(msg)
                else:
                    print("Invalid message structure:", msg)
            except Exception as e:
                print("Failed to parse line:", line, "Error:", e)
        return messages

    def _validate_message(self, msg: dict) -> bool:
        return all(field in msg for field in self.REQUIRED_FIELDS)


def encode_message(device_id: str, msg_type: str, data: dict, verbose=False) -> bytes:
    """
    Generic messages example in newline-delimited JSON format, timestamp, type, data:
    {"timestamp": 112345678, "device_id": "central", "type": "key", "col": 1, "row": 2, "pressed": true}
    {"timestamp": 112345678, "device_id": "central", "type": "battery", "voltage": 3.73}
    {"timestamp": 112345678, "device_id": "central", "type": "led_status", "color": "green"}
    {"timestamp": 112345678, "device_id": "central", "type": "encoder", "delta": -1}
    """
    msg = OrderedDict()
    msg["timestamp"] = time.monotonic_ns() // 1_000_000  # Timestamp in milliseconds
    msg["device_id"] = device_id
    msg["type"] = msg_type
    msg.update(data)
    try:
        if verbose:
            print("send:", json.dumps(msg))
        return (json.dumps(msg) + "\n").encode()
    except Exception as e:
        print("Message encode error:", e)
        return b""


RESYNC_INTERVAL_MS = 5000  # 5 seconds


def sync_messages(self, messages_per_device, now):
    adjusted_messages = {}
    sync_offsets = {}

    for device_id, messages in messages_per_device.items():
        adjusted = []
        if not messages:
            adjusted_messages[device_id] = adjusted
            continue

        # Will resync every timeframe in the MKX_Central
        if device_id not in sync_offsets:
            sync_offsets[device_id] = now - messages[0].get("timestamp")

        for msg in messages:
            msg["timestamp"] = msg.get("timestamp") + sync_offsets[device_id]
            adjusted.append(msg)

        adjusted_messages[device_id] = adjusted

    return adjusted_messages


DEBOUNCE_MS = 5


def debounce(messages_per_device):
    debounced_messages = {}

    for device_id, messages in messages_per_device.items():
        debounced_msg = []
        key_states = {}

        # if device_id not in self.key_states:
        #     self.key_states[device_id] = {}

        # key_states = self.key_states[device_id]

        for msg in messages:
            if msg.get("type") != "key_event":
                continue  # Ignore non-key_events

            timestamp = msg.get("timestamp")
            col = msg.get("col")
            row = msg.get("row")
            pressed = msg.get("pressed")

            if None in (col, row, pressed):
                continue  # Skip malformed

            key = (col, row)
            state_info = key_states.get(key)

            if state_info is None:  # First time seeing this key
                key_states[key] = {"timestamp": timestamp, "pressed": pressed}
                debounced_msg.append(msg)
            elif state_info["pressed"] != pressed:
                if timestamp - state_info["timestamp"] >= DEBOUNCE_MS:
                    key_states[key] = {"timestamp": timestamp, "pressed": pressed}
                    debounced_msg.append(msg)
            else:  # Same state, only update timestamp
                state_info["timestamp"] = timestamp

        if debounced_msg:
            debounced_messages[device_id] = debounced_msg

    return debounced_messages
