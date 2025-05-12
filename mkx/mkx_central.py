import time
from collections import OrderedDict

from adafruit_hid.keycode import Keycode

from mkx.connect_periphery_abstract import ConnectPeripheryAbstract

FRAME_INTERVAL_MS = 10
SYNC_INTERVAL_MS = 5000
PERIPHERAL_TIMEOUT_MS = 1000
DEBOUNCE_MS = 5

last_frame_time = time.monotonic_ns() // 1_000_000


class MKX_Central:
    def __init__(self, keymap=None, coord_mapping=None):
        self.keymap = keymap if keymap is not None else []
        self.coord_mapping = coord_mapping
        self.hid_mode = None
        self.hids = []
        self.interfaces = []  # List of interface to peripheries
        self.central_periphery = None

        self.last_frame_time = 0
        self.sync_offsets = {}  # Dictionary of offsets per interface
        self.debounce_state = {}  # Store debounced states per interface

    def add_interface(self, interface: ConnectPeripheryAbstract):
        self.interfaces.append(interface)

    def poll(self):
        for device_id, adapter in self.adapters.items():
            if not adapter.is_connected():
                adapter.reconnect()
            try:
                messages = adapter.receive()
                for msg in messages:
                    print(f"[{device_id}] {msg}")
            except Exception as e:
                print(f"[{device_id}] poll error: {e}")

    def send_to(self, device_id: str, msg_type: str, data: dict):
        adapter = self.adapters.get(device_id)
        if adapter and adapter.is_connected():
            adapter.send(msg_type, data)
        else:
            print(f"[{device_id}] not connected, can't send")

    def broadcast(self, msg_type: str, data: dict):
        for adapter in self.adapters.values():
            if adapter.is_connected():
                adapter.send(msg_type, data)

    def process_key_event(self, row, col, pressed):
        pos = (row, col)
        if pos not in self.keymap:
            return None
        keycode = self.keymap[pos]
        if pressed:
            self.held_keys[pos] = True
            return (keycode, True)
        elif pos in self.held_keys:
            del self.held_keys[pos]
            return (keycode, False)

    def central_periphery_send(self):
        if self.central_periphery:
            signal = self.central_periphery.get_key_events()
            # print("dd", signal)
            for col, row, pressed in signal:
                self.central_periphery.send(
                    "key_event",
                    OrderedDict(
                        [("col", col), ("row", row), ("pressed", pressed)],
                    ),
                    verbose=False,
                    # "key_event", {"row": 1, "col": 2, "pressed": True}
                )

    def process_debounce(self, interface, timestamp, msg):
        # Implement debouncing logic here for the keys
        key = msg.get("key")  # Assuming key is part of the message
        if key:
            if interface not in self.debounce_state:
                self.debounce_state[interface] = {}

            debounce_info = self.debounce_state[interface].get(key)

            # If it's the first event for this key, process it
            if debounce_info is None:
                self.debounce_state[interface][key] = {
                    "timestamp": timestamp,
                    "state": msg["state"],
                }
                self.process_key_event(interface, key, msg["state"])
            else:
                # If the state is different (press/release), check debounce period
                if debounce_info["state"] != msg["state"]:
                    if timestamp - debounce_info["timestamp"] >= DEBOUNCE_MS:
                        # Apply debounce threshold, then process the event
                        self.debounce_state[interface][key] = {
                            "timestamp": timestamp,
                            "state": msg["state"],
                        }
                        self.process_key_event(interface, key, msg["state"])
                else:
                    # If the state hasn't changed, just update the timestamp
                    self.debounce_state[interface][key]["timestamp"] = timestamp

    def run_once(self):
        now = time.monotonic_ns() // 1_000_000  # Current time in ms

        if now - self.last_frame_time >= FRAME_INTERVAL_MS:
            frame_end = now + FRAME_INTERVAL_MS

            # Loop over all interfaces to process received data
            for interface in self.interfaces:
                all_messages = []

                # Continuously receive data while we're within the frame time
                while True:
                    now = time.monotonic_ns() // 1_000_000
                    if now >= frame_end:
                        break

                    if interface.device_id == "central":
                        self.central_periphery_send()

                    data = interface.receive(verbose=True)

                    if data:
                        all_messages.extend(data)

                    time.sleep(0.005)  # Keep CPU usage low

                # Process all accumulated messages
                for msg in all_messages:
                    timestamp = msg.get("timestamp")

                    # Sync time for this interface
                    if interface not in self.sync_offsets:
                        host_now = now
                        self.sync_offsets[interface] = host_now - timestamp

                    # adjusted_ts = timestamp + self.sync_offsets[interface]
                    # self.process_debounce(interface, adjusted_ts, msg)

            # Keys logic

            # AddOns TO DO

            # process_key_event(self, row, col, pressed)
            # self.hids[0].send_key(Keycode.A, True)  # Press "a"
            # self.hids[0].send_key(Keycode.A, False)  # Release "a"

            # msg = self.hids[0].send_key(3, True)
            # print("msg: ", msg)

            self.last_frame_time = frame_end

        time.sleep(0.01)  # Maintain reasonable loop rate

    def run_forever(self):
        self.last_frame_time = time.monotonic_ns() // 1_000_000
        while True:
            self.run_once()
