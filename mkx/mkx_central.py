import sys, time
import json
from collections import OrderedDict

from mkx.mkx_abstract import MKX_Abstract
from mkx.periphery_central import PeripheryCentral

from mkx.communication_message import sync_messages, debounce
from mkx.process_key_event import process_key_event

FRAME_INTERVAL_MS = 5


class MKX_Central(MKX_Abstract):
    def __init__(self):
        super().__init__()
        self.periphery_central = None
        self.last_frame_time = 0

    def add_periphery_central(self, periphery_central: PeripheryCentral):
        self.periphery_central = periphery_central

    def _periphery_central_send(self):
        if self.periphery_central:
            signal = self.periphery_central.get_key_events()
            for col, row, pressed in signal:
                self.periphery_central.send(
                    "key_event",
                    OrderedDict(
                        [("col", col), ("row", row), ("pressed", pressed)],
                    ),
                    verbose=False,
                )
        else:
            print("No periphery central registered!")
            exit(1)

    def send_to(self, device_id: str, msg_type: str, data: dict):
        adapter = self.adapters.get(device_id)
        if adapter and adapter.is_connected():
            adapter.send(msg_type, data)
        else:
            print(f"[{device_id}] not connected, can't send")

    def _process_key_event_msg(self, event_json):
        timestamp = event_json["timestamp"]
        device_id = event_json["device_id"]
        local_col = event_json["col"]
        local_row = event_json["row"]
        pressed = event_json["pressed"]

        # find the interface for this device_id
        iface = self._get_interface(device_id)
        if iface is None:
            print(f"No interface registered for device_id {device_id}!")
            exit(1)

        # translate to flat index through the interface’s coordinate map
        logical_index = self._get_logical_index(iface, local_col, local_row)
        if logical_index is None:
            return

        process_key_event(self, device_id, logical_index, pressed, timestamp)

    def run_once(self):
        if not self._ensure_ble():
            return

        now = time.monotonic_ns() // 1_000_000  # Current time in ms

        if now - self.last_frame_time >= FRAME_INTERVAL_MS:
            frame_end = now + FRAME_INTERVAL_MS

            all_messages = []

            # Continuously receive data while we're within the frame time
            while True:
                if time.monotonic_ns() // 1_000_000 >= frame_end:
                    break

                self._periphery_central_send()

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

            self.timed_keys_manager.update(
                self.layers_manager, self.keyboard, time.monotonic_ns() // 1_000_000
            )

            for key_event in debounced_msg:
                self._process_key_event_msg(key_event)
                print("")

            if self.backlight:
                self.backlight.shine()

            self.last_frame_time = frame_end

    def run_forever(self):
        self._init_keyboard()

        self.last_frame_time = time.monotonic_ns() // 1_000_000
        while True:
            self.run_once()
