import time

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
        self.interfaces = []
        self.central_periphery = None

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

    def run_once(self):
        now = time.monotonic_ns() // 1_000_000

        if now - last_frame_time >= FRAME_INTERVAL_MS:
            frame_start = last_frame_time
            frame_end = last_frame_time + FRAME_INTERVAL_MS

            if self.central_periphery:
                signal = self.central_periphery.get_key_events()
                # print("dd", signal)
                for col, row, pressed in signal:
                    self.central_periphery.send(
                        "key_event",
                        {"col": col, "row": row, "pressed": pressed},
                        # "key_event", {"row": 1, "col": 2, "pressed": True}
                    )

            for interface in self.interfaces:
                # Apply time sync TO DO

                # Receive
                # print("interface: ", interface)
                data = interface.receive()
                print("data: ", data)

                # Debouncing TO DO

                # Keys logic

                # AddOns TO DO

                # process_key_event(self, row, col, pressed)
                # self.hids[0].send_key(Keycode.A, True)  # Press "a"
                # self.hids[0].send_key(Keycode.A, False)  # Release "a"

                # msg = self.hids[0].send_key(3, True)
                # print("msg: ", msg)

        time.sleep(0.5)

    def run_forever(self):
        while True:
            self.run_once()


# while True:
#     now = time.monotonic_ns() // 1_000_000

#     if now - last_frame_time >= FRAME_INTERVAL_MS:
#         frame_start = last_frame_time
#         frame_end = last_frame_time + FRAME_INTERVAL_MS

#         # Combine debounced states across all peripherals
#         global_key_states = {}

#         for pid, pdata in peripherals.items():
#             # Skip disconnected peripherals
#             if now - pdata["last_seen"] > PERIPHERAL_TIMEOUT_MS:
#                 continue

#             # Apply time sync
#             offset = pdata["sync_offset"]
#             frame_events = [
#                 (t + offset, key, state)
#                 for t, key, state in pdata["event_queue"]
#                 if frame_start <= (t + offset) < frame_end
#             ]

#             # Remove processed events
#             pdata["event_queue"] = [
#                 e for e in pdata["event_queue"] if (e[0] + offset) >= frame_end
#             ]

#             # Debounce per peripheral
#             for t_adj, key, new_state in frame_events:
#                 ds = pdata["debounce_state"]
#                 prev = ds.get(key)

#                 if prev is None:
#                     ds[key] = {"state": new_state, "timestamp": t_adj}
#                     global_key_states[key] = new_state
#                 else:
#                     if prev["state"] != new_state:
#                         if t_adj - prev["timestamp"] >= DEBOUNCE_MS:
#                             ds[key] = {"state": new_state, "timestamp": t_adj}
#                             global_key_states[key] = new_state
#                     else:
#                         ds[key]["timestamp"] = t_adj
#                         global_key_states[key] = new_state

#         # Merge states: final list of pressed keys
#         pressed_keys = [
#             key for key, state in global_key_states.items() if state == "down"
#         ]

#         send_hid_report(pressed_keys)
#         last_frame_time = frame_end
