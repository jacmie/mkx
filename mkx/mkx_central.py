import sys, time
import json
from collections import OrderedDict

import usb_hid
from adafruit_hid.keyboard import Keyboard

from mkx.interphace_abstract import InterfahceAbstract
from mkx.communication_message import sync_messages, debounce

from mkx.timed_keys import TimedKeys, TimedKeysManager
from mkx.manager_layers import LayersManager

from mkx.keys_sticky import SK, StickyKeyManager
from mkx.keys_layers import KeysLayer, LT, TT

from mkx.check import check

FRAME_INTERVAL_MS = 5
SYNC_INTERVAL_MS = 5000
PERIPHERAL_TIMEOUT_MS = 1000
DEBOUNCE_MS = 5

last_frame_time = time.monotonic_ns() // 1_000_000


class MKX_Central:
    def __init__(self, keymap=None, coord_mapping=None):
        print("MKX_Central -> Start:")
        self.col_size = 0
        self.row_size = 0
        self.keymap = keymap if keymap is not None else []
        self.coord_mapping = coord_mapping
        self.hid_mode = None
        self.hids = []
        self.interfaces = []  # List of interface to peripheries
        self.central_periphery = None

        self.last_frame_time = 0
        self.sync_offsets = {}  # Dictionary of offsets per interface
        self.debounce_state = {}  # Store debounced states per interface

        self.pressed_keys = (
            {}
        )  # Track pressed keys on the active layer even after layer change

        self.timed_keys_manager = TimedKeysManager()
        self.sticky_key_manager = StickyKeyManager()
        self.layers_manager = LayersManager(default_layer=0)

    def add_interface(self, interface: InterfahceAbstract):
        self.interfaces.append(interface)

    def add_keymap(self, keymap, col_size, row_size):
        self.keymap = keymap
        self.col_size = col_size
        self.row_size = row_size

        if not all(len(row) == col_size * row_size for row in keymap):
            print("Keymap layers must be rectangular and match given size!")
            sys.exit(1)

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

    def process_key_event(self, event_json):
        timestamp = event_json["timestamp"]
        device_id = event_json["device_id"]
        local_col = event_json["col"]
        local_row = event_json["row"]
        pressed = event_json["pressed"]

        # find the interface for this device_id
        iface = None
        for i in self.interfaces:
            if i.device_id == device_id:
                iface = i
                break
        if iface is None:
            print(f"No interface registered for device_id {device_id}")
            return

        # translate to flat index through the interface’s coordinate map
        try:
            logical_index = iface.logical_index(local_col, local_row)
        except IndexError as e:
            print(e)
            return

        key_pos = (device_id, logical_index)

        if pressed:
            active_layer = self.layers_manager.get_top_layer()

            try:
                key = self.keymap[active_layer][logical_index]
            except IndexError:
                print(
                    f"Key index {logical_index} out of bounds for layer {active_layer}"
                )
                return

            if key is None:
                return

            # Store keys for tracking release and avoid keys lock: key press -> layer changed -> key release
            self.pressed_keys[key_pos] = key

            if isinstance(key, KeysLayer):
                key.on_press(self.layers_manager, self.keyboard, timestamp)
                if not isinstance(key, LT) and not isinstance(key, TT):
                    return

            # Call on_press for all types of keys (except KeysLayer, which you already handled above)
            key.on_press(self.layers_manager, self.keyboard, timestamp)

            # If the key is time-based, register it *after* on_press so it's active
            if isinstance(key, TimedKeys):
                self.timed_keys_manager.register(key)

            print("key:", key.key_name, "pressed")

            if isinstance(key, SK):
                self.sticky_key_manager.register(key)

        else:
            # Retrieve previously stored KeysLayer key (if any)
            key = self.pressed_keys.pop(key_pos, None)

            if key is None:
                # Fallback: look up from top layer if not tracked
                active_layer = self.layers_manager.get_top_layer()
                try:
                    key = self.keymap[active_layer][logical_index]
                except IndexError:
                    print(
                        f"Key index {logical_index} out of bounds for layer {active_layer}"
                    )
                    return

                if key is None:
                    return

            if isinstance(key, KeysLayer):
                key.on_release(self.layers_manager, self.keyboard, timestamp)
                return

            print("key:", key.key_name, "released")

            key.on_release(self.layers_manager, self.keyboard, timestamp)

            if not isinstance(key, SK):
                self.sticky_key_manager.clear_stickies(self.keyboard, timestamp)

    def run_once(self):
        now = time.monotonic_ns() // 1_000_000  # Current time in ms

        if now - self.last_frame_time >= FRAME_INTERVAL_MS:
            frame_end = now + FRAME_INTERVAL_MS

            all_messages = []

            # Continuously receive data while we're within the frame time
            while True:
                if time.monotonic_ns() // 1_000_000 >= frame_end:
                    break

                self.central_periphery_send()

                # Loop over all interfaces to process received data
                for interface in self.interfaces:
                    data = interface.receive(verbose=True)
                    if data:
                        all_messages.extend(data)

                time.sleep(0.001)  # Keep CPU usage low
                # time.sleep(1)  # Keep CPU usage low

            sync_msg = sync_messages(
                all_messages, time.monotonic_ns() // 1_000_000, verbose=True
            )
            if sync_msg:
                print("sync_msg:", json.dumps(sync_msg))

            debounced_msg = debounce(sync_msg, verbose=True)
            if debounced_msg:
                print("debounced_msg:", json.dumps(debounced_msg))

            # AddOns TO DO

            self.timed_keys_manager.update(
                self.layers_manager, self.keyboard, time.monotonic_ns() // 1_000_000
            )

            for key_event in debounced_msg:
                self.process_key_event(key_event)
                print("")

            self.last_frame_time = frame_end

    def run_forever(self):
        self.keyboard = Keyboard(usb_hid.devices)

        if check(self.col_size, self.row_size, self.keymap, self.interfaces):
            sys.exit(1)

        self.last_frame_time = time.monotonic_ns() // 1_000_000
        while True:
            self.run_once()


# dynamic throttling Pseudocode:
# if active_keys:
#     loop_delay = 1  # ms — high responsiveness
# elif recent_key_activity < 500 ms:
#     loop_delay = 5  # ms — balance
# else:
#     loop_delay = 10–20  # ms — power saving
