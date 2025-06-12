import time
import json
import sys
import struct

from collections import OrderedDict

HEADER_BYTE = 0xB2
DEBOUNCE_MS = 5


class MessageParser:
    def __init__(self, max_message_size=256):
        self.buffer = b""
        self.max_message_size = max_message_size

    def parse(self, new_data: bytes, verbose=False) -> list[dict]:
        messages = []
        self.buffer += new_data

        if verbose:
            print("data:", self.buffer)

        while True:
            # Need at least header(1) + length(2)
            if len(self.buffer) < 3:
                break

            if self.buffer[0] != HEADER_BYTE:
                # Skip invalid byte
                print(f"Warning: skipping invalid header byte: {self.buffer[0]:02X}")
                self.buffer = self.buffer[1:]
                continue

            length = struct.unpack(">H", self.buffer[1:3])[0]

            # Check if full message is present
            if verbose:
                print("in buffer:", len(self.buffer), "data size:", 3 + length + 1)

            if len(self.buffer) < 3 + length + 1:
                # Wait for more data
                print("Wait for more data, break")
                break

            payload = self.buffer[3 : 3 + length]
            checksum = self.buffer[3 + length]

            computed_checksum = sum(payload) & 0xFF

            if checksum != computed_checksum:
                print(
                    f"Checksum mismatch! expected {checksum}, got {computed_checksum}"
                )
                # Skip this header and try next byte
                self.buffer = self.buffer[1:]
                continue

            try:
                line_str = payload.decode("ascii").strip()

                if verbose:
                    print("received:", line_str)

                parts = line_str.split(":")
                if len(parts) < 3:
                    print("Invalid message format:", line_str)
                else:
                    msg = OrderedDict()
                    msg["timestamp"] = int(parts[0])
                    msg["device_id"] = parts[1]
                    msg["type"] = parts[2]
                    msg["data"] = parts[3:]

                    messages.append(msg)

            except Exception as e:
                print("Failed to parse payload:", payload, "Error:", e)
                # Also discard header and try next byte
                self.buffer = self.buffer[1:]
                continue

            # Remove this message from the buffer
            self.buffer = self.buffer[3 + length + 1 :]

        if verbose:
            print("messages: ", messages, "\n")

        return messages


def encode_message(device_id: str, msg_type: str, data: dict, verbose=False) -> bytes:
    """
    Encodes a message in the format:
    HEADER(1) + LENGTH(2) + PAYLOAD(ascii) + CHECKSUM(1)
    """
    timestamp = time.monotonic_ns() // 1_000_000  # Timestamp in ms

    # Build the ascii payload: "timestamp:device_id:type:other_fields..."
    fields = [str(timestamp), device_id, msg_type]

    # Sort keys for stable order (optional)
    # for key in sorted(data.keys()):
    for key in data.keys():
        fields.append(str(data[key]))

    # Join all parts with ":"
    payload_str = ":".join(fields) + "\n"
    payload_bytes = payload_str.encode("ascii")

    # Compute length and checksum
    length = len(payload_bytes)
    checksum = sum(payload_bytes) & 0xFF

    # Pack everything
    message = bytearray()
    message.append(HEADER_BYTE)
    message += struct.pack(">H", length)  # 2 bytes, big endian
    message += payload_bytes
    message.append(checksum)

    if verbose:
        print(f"send: {payload_str.strip()} (len={length}, checksum={checksum})")

    return bytes(message)


def sync_messages(all_messages, now, verbose=False):
    adjusted_msg = []
    sync_offsets = {}

    for msg in all_messages:
        device_id = msg.get("device_id")
        if device_id is None:
            continue

        print("msg", msg)
        print("device_id", device_id)
        print("timestamp", msg["timestamp"])
        print("type", msg["type"])
        print("data", msg["data"])

        # Compute offset if not already done
        if device_id not in sync_offsets:
            sync_offsets[device_id] = now - msg["timestamp"]
            if verbose:
                print("sync_offset:", device_id, sync_offsets[device_id])

        # Adjust timestamp
        ordered_msg = OrderedDict(
            (
                ("timestamp", msg["timestamp"] + sync_offsets[device_id]),
                ("device_id", device_id),
                ("type", msg.get("type")),
                ("data", msg.get("data")),
            )
        )
        adjusted_msg.append(ordered_msg)

    # Sort globally by adjusted timestamp
    adjusted_msg.sort(key=lambda m: m["timestamp"])
    return adjusted_msg


def debounce(messages, verbose=False):
    debounced_msg = []
    key_states = {}

    # TO DO - Upgrade to keep key_states across Timeframes
    # if device_id not in self.key_states:
    #     self.key_states[device_id] = {}
    # key_states = self.key_states[device_id]

    for msg in messages:
        if msg.get("type") != "key_event":
            continue  # Ignore non-key_events

        timestamp = msg.get("timestamp")
        device_id = msg.get("device_id")
        type = msg.get("type")
        data_fields = msg.get("data")
        col = int(data_fields[0])
        row = int(data_fields[1])
        pressed = data_fields[2].lower() == "true"

        if None in (col, row, pressed):
            continue  # Skip malformed

        normalized_msg = {
            "timestamp": timestamp,
            "device_id": device_id,
            "type": type,
            "col": col,
            "row": row,
            "pressed": pressed,
        }
        print("normalized_msg:", normalized_msg)

        key = (device_id, col, row)
        state = key_states.get(key)

        if state is None:  # First time seeing this key
            key_states[key] = {"timestamp": timestamp, "pressed": pressed}
            debounced_msg.append(normalized_msg)
        elif state["pressed"] != pressed:
            if timestamp - state["timestamp"] >= DEBOUNCE_MS:
                key_states[key] = {"timestamp": timestamp, "pressed": pressed}
                debounced_msg.append(normalized_msg)
            elif verbose:
                print(
                    "debounced:",
                    key,
                    timestamp - state["timestamp"],
                    debounced_msg,
                )
        else:  # Same state, only update timestamp
            state["timestamp"] = timestamp

    return debounced_msg
