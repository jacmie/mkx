import sys, time
import json
from collections import OrderedDict

from mkx.mkx_abstract import MKX_Abstract

from mkx.communication_message import sync_messages, debounce

FRAME_INTERVAL_MS = 5


class MKX_Central(MKX_Abstract):
    def __init__(self, keymap=None):
        super().__init__(keymap)

    def add_central_periphery(self, central_periphery):
        self.central_periphery = central_periphery

    def send_to(self, device_id: str, msg_type: str, data: dict):
        adapter = self.adapters.get(device_id)
        if adapter and adapter.is_connected():
            adapter.send(msg_type, data)
        else:
            print(f"[{device_id}] not connected, can't send")

    def central_periphery_send(self):
        if self.central_periphery:
            signal = self.central_periphery.get_key_events()
            for col, row, pressed in signal:
                self.central_periphery.send(
                    "key_event",
                    OrderedDict(
                        [("col", col), ("row", row), ("pressed", pressed)],
                    ),
                    verbose=False,
                )

    def process_key_event_msg(self, event_json):
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

        super().process_key_event(device_id, logical_index, pressed, timestamp)

    def run_once(self):
        if self._use_ble:
            self._ble.ensure_advertising()

            if not self._ble.devices:
                return

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
                self.process_key_event_msg(key_event)
                print("")

            if self.backlight:
                self.backlight.shine()

            self.last_frame_time = frame_end


# dynamic throttling Pseudocode:
# if active_keys:
#     loop_delay = 1  # ms — high responsiveness
# elif recent_key_activity < 500 ms:
#     loop_delay = 5  # ms — balance
# else:
#     loop_delay = 10–20  # ms — power saving
