import sys, time
import json
from collections import OrderedDict

import usb_hid
from adafruit_hid.keyboard import Keyboard

from mkx.interphace_abstract import InterfahceAbstract
from mkx.communication_message import sync_messages, debounce

from mkx.timed_keys import TimedKeys, TimedKeysManager
from mkx.keys_sticky import SK, StickyKeyManager
from mkx.keys_layers import KeysLayer, LayersManager

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

            # Only store KeysLayer keys for tracking release
            if isinstance(key, KeysLayer):
                self.pressed_keys[key_pos] = key

            if isinstance(key, KeysLayer):
                key.on_press(self.layers_manager, self.keyboard, timestamp)
                return

            if isinstance(key, TimedKeys):
                self.timed_keys_manager.register(key)

            print("key:", key.key_name, "pressed")

            if isinstance(key, SK):
                self.sticky_key_manager.register(key)

            key.on_press(self.keyboard, timestamp)

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

            key.on_release(self.keyboard, timestamp)

            if not isinstance(key, SK):
                self.sticky_key_manager.clear_stickies(self.keyboard, timestamp)

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

                    time.sleep(0.001)  # Keep CPU usage low

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
                self.keyboard, time.monotonic_ns() // 1_000_000
            )

            for key_event in debounced_msg:
                self.process_key_event(key_event)
                print("")

            self.last_frame_time = frame_end

    def run_forever(self):
        self.keyboard = Keyboard(usb_hid.devices)
        self.check()
        self.last_frame_time = time.monotonic_ns() // 1_000_000
        while True:
            self.run_once()

    def check(self):
        total_rows = self.row_size
        total_cols = self.col_size
        keymap_size = total_rows * total_cols

        print(f"\n=== KEYMAP-CHECK (layer 0) ===")

        for iface in self.interfaces:
            name = getattr(iface, "device_id", "unknown")

            iface.generate_rect_map(12)

            # -------------------------------------------------
            # 1.  Bounds check
            # -------------------------------------------------
            errors = False
            for dim, val, limit in [
                ("row_min", iface.row_min, total_rows),
                ("row_max", iface.row_max, total_rows),
                ("col_min", iface.col_min, total_cols),
                ("col_max", iface.col_max, total_cols),
            ]:
                if not (0 <= val < limit):
                    print(f"[ERROR] {name}: {dim}={val} out of bounds 0-{limit-1}")
                    errors = True

            # coordinate map presence
            cmap = getattr(iface, "_coord_map", None)
            if cmap is None:
                print(f"[WARNING] {name}: no coordinate map set")
                continue

            # -------------------------------------------------
            # 2.  Coordinate‑map index range check
            # -------------------------------------------------
            for i, idx in enumerate(cmap):
                if not (0 <= idx < keymap_size):
                    print(
                        f"[ERROR] {name}: coord_map[{i}]={idx} out of range 0-{keymap_size-1}"
                    )
                    errors = True

            # -------------------------------------------------
            # 3.  Build a shadow matrix for visualisation
            # -------------------------------------------------
            shadow = [["·" for _ in range(total_cols)] for _ in range(total_rows)]

            for local_i, flat_idx in enumerate(cmap):
                r, c = divmod(flat_idx, total_cols)
                try:
                    key_obj = self.keymap[0][flat_idx]
                except IndexError:
                    key_obj = None

                char = str(key_obj.key_name) if key_obj is not None else "None"
                # shorten long names so grid stays narrow
                char = char[:8]
                shadow[r][c] = char

            # -------------------------------------------------
            # 4.  Print results
            # -------------------------------------------------
            print(
                "\n[{}] covers rows {}-{}, cols {}-{}".format(
                    name, iface.row_min, iface.row_max, iface.col_min, iface.col_max
                )
            )

            if errors:
                print("  (Errors above)")

            # pretty‑print shadow
            for r in range(total_rows):
                row_str = "  ".join(f"{cell:>8}" for cell in shadow[r])
                print(row_str)


# dynamic throttling Pseudocode:
# if active_keys:
#     loop_delay = 1  # ms — high responsiveness
# elif recent_key_activity < 500 ms:
#     loop_delay = 5  # ms — balance
# else:
#     loop_delay = 10–20  # ms — power saving
