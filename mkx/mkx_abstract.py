import time

import usb_hid
from adafruit_hid.keyboard import Keyboard

from mkx.ble import BLE

from mkx.periphery_single import PeripherySingle
from mkx.interface_abstract import InterfaceAbstract
from mkx.keys_abstract import KeysAbstract

from mkx.layer_status_led_abstract import LayerStatusLedAbstract
from mkx.manager_layers import LayersManager
from mkx.timed_keys import TimedKeysManager
from mkx.keys_sticky import StickyKeyManager
from mkx.backlight_abstract import BacklightAbstract

from mkx.check import check
from mkx.process_key_event import process_key_event
from mkx.error import halt_on_error
from mkx.ansi_colors import Ansi, Ansi256


class MKX_Abstract:
    def __init__(self):
        print()
        print(f"{Ansi.BOLD}{Ansi256.LIGHT_GREEN}MKX -> Start:{Ansi.RESET}")
        print()

        self.col_size = 0
        self.row_size = 0
        self.keymap = []
        self.interfaces = []
        self.pressed_keys: dict[int, bool] = (
            {}
        )  # used to track time-dependent keys and prevent stuck keys when layers change while held

        self.timed_keys_manager = TimedKeysManager()
        self.sticky_key_manager = StickyKeyManager()
        self.layers_manager = LayersManager(default_layer=0)

        self.backlight = None

        self._use_ble = False
        self._ble = None

        self.periphery_single = None
        self.keyboard = None

    def use_ble(self, use_ble: bool):
        self._use_ble = use_ble

    def add_periphery_single(self, periphery_single: PeripherySingle):
        self.periphery_single = periphery_single

    def add_interface(self, interface: InterfaceAbstract):
        self.interfaces.append(interface)

    def add_layer_status_led(self, status_led: LayerStatusLedAbstract):
        self.layers_manager.add_layer_status_led(status_led)

    def add_keymap(
        self, keymap: list[list[KeysAbstract]], col_size: int, row_size: int
    ):
        self.keymap = keymap
        self.col_size = col_size
        self.row_size = row_size

        expected_size = col_size * row_size

        for layer_index, layer in enumerate(keymap):
            actual_size = len(layer)

            if actual_size != expected_size:
                halt_on_error(
                    (
                        f"Invalid keymap layer {layer_index}: "
                        f"expected {expected_size} keys "
                        f"({col_size}x{row_size}), "
                        f"got {actual_size}"
                    ),
                    status_led=getattr(self.layers_manager, "status_led", None),
                )

    def add_backlight(self, backlight: BacklightAbstract):
        self.backlight = backlight

    def _init_keyboard(self):
        if check(self.col_size, self.row_size, self.keymap, self.interfaces):
            halt_on_error(
                "Checking the keyboard Configuration failed!",
                status_led=getattr(self.layers_manager, "status_led", None),
            )

        if self._use_ble:
            self._ble = BLE()
            self._ble.init()
            self.keyboard = Keyboard(self._ble.devices)
        else:
            self.keyboard = Keyboard(usb_hid.devices)

    def _ensure_ble(self):
        if self._use_ble and self._ble:
            self._ble.ensure_advertising()
            return bool(self._ble.devices)
        return True

    def _get_interface(self, device_id):
        for interface in self.interfaces:
            if interface.device_id == device_id:
                return interface

        halt_on_error(
            f"No interface registered for device_id {device_id}!",
            status_led=getattr(self.layers_manager, "status_led", None),
        )

        return None

    def _get_logical_index(self, iface, col, row):
        try:
            return iface.logical_index(col, row)
        except IndexError as e:
            print(e)
            return None

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

    def run_forever(self):
        self._init_keyboard()

        while True:
            self.run_once()
