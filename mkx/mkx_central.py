import time
from collections import OrderedDict

from adafruit_hid.keycode import Keycode

from mkx.connect_periphery_abstract import ConnectPeripheryAbstract
from mkx.communication_message import sync_messages, debounce

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

    def run_once(self):
        now = time.monotonic_ns() // 1_000_000  # Current time in ms

        if now - self.last_frame_time >= FRAME_INTERVAL_MS:
            frame_end = now + FRAME_INTERVAL_MS

            all_messages = []

            # Loop over all interfaces to process received data
            for interface in self.interfaces:
                # Continuously receive data while we're within the frame time
                while True:
                    if time.monotonic_ns() // 1_000_000 >= frame_end:
                        break

                    self.central_periphery_send()

                    data = interface.receive(verbose=True)

                    if data:
                        all_messages.extend(data)

                    time.sleep(0.005)  # Keep CPU usage low

            messages_per_device = {}

            for msg in all_messages:
                device_id = msg.get("device_id")

                if device_id not in messages_per_device:
                    messages_per_device[device_id] = []

                messages_per_device[device_id].append(msg)

            sync_msg = sync_messages(
                self, messages_per_device, time.monotonic_ns() // 1_000_000
            )
            debounce(sync_msg)

            # Keys logicself,

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
