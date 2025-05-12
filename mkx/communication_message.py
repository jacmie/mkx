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
    {"timestamp": 112345678, "type": "key", "col": 1, "row": 2, "pressed": true}
    {"timestamp": 112345678, "type": "battery", "voltage": 3.73}
    {"timestamp": 112345678, "type": "led_status", "color": "green"}
    {"timestamp": 112345678, "type": "encoder", "delta": -1}
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
