import time
import json


class MessageParser:
    def __init__(self):
        self.buffer = b""

    def parse(self, new_data: bytes) -> list[dict]:
        messages = []
        self.buffer += new_data
        while b"\n" in self.buffer:
            line, self.buffer = self.buffer.split(b"\n", 1)
            try:
                msg = json.loads(line.decode().strip())
                messages.append(msg)
            except Exception as e:
                print("Failed to parse line:", line, "Error:", e)
        return messages


def encode_message(msg_type: str, data: dict) -> bytes:
    """
    Generic messages example in newline-delimited JSON format, timestamp, type, data:
    {"timestamp": 112345678, "type": "key", "col": 1, "row": 2, "pressed": true}
    {"timestamp": 112345678, "type": "battery", "voltage": 3.73}
    {"timestamp": 112345678, "type": "led_status", "color": "green"}
    {"timestamp": 112345678, "type": "encoder", "delta": -1}
    """
    msg = {
        "timestamp": time.monotonic_ns() // 1_000_000,  # Timestamp in milliseconds
        "type": msg_type,
    }
    msg.update(data)
    try:
        return (json.dumps(msg) + "\n").encode()
    except Exception as e:
        print("Message encode error:", e)
        return b""
