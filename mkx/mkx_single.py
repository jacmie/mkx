import time

from mkx.mkx_abstract import MKX_Abstract
from mkx.periphery_single import PeripherySingle

from mkx.process_key_event import process_key_event
from mkx.error import halt_on_error


class MKX_Single(MKX_Abstract):
    def __init__(self):
        super().__init__()
        self.periphery_single = None

    def add_periphery_single(self, periphery_single: PeripherySingle):
        self.periphery_single = periphery_single

    def _collect_key_events(self):
        if not self.periphery_single:
            halt_on_error(
                "No periphery single registered!",
                status_led=getattr(self.layers_manager, "status_led", None),
            )

        iface = self._get_interface(self.periphery_single.device_id)
        if iface is None:
            halt_on_error(
                "No interface single registered!",
                status_led=getattr(self.layers_manager, "status_led", None),
            )

        raw_events = self.periphery_single.get_key_events()
        if not raw_events:
            return []

        events = []

        # translate to flat index through the interface’s coordinate map
        for local_col, local_row, pressed in raw_events:
            logical_index = self._get_logical_index(iface, local_col, local_row)
            if logical_index is None:
                continue

            events.append((logical_index, pressed))

        return events

    def run_once(self):
        if not self._ensure_ble():
            return

        now = time.monotonic_ns() // 1_000_000

        self.timed_keys_manager.update(self.layers_manager, self.keyboard, now)

        for event in self._collect_key_events():
            logical_index, pressed = event

            process_key_event(
                self, self.periphery_single.device_id, logical_index, pressed, now
            )

        if self.backlight:
            self.backlight.shine()

        time.sleep(0.001)  # Keep CPU usage low
