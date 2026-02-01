import sys, time

import usb_hid
from adafruit_hid.keyboard import Keyboard

from mkx.ble import BLE

from mkx.interface_abstract import InterfaceAbstract

from mkx.layer_status_led_abstract import LayerStatusLedAbstract
from mkx.manager_layers import LayersManager
from mkx.timed_keys import TimedKeysManager
from mkx.keys_sticky import StickyKeyManager
from mkx.backlight_abstract import BacklightAbstract

from mkx.check import check
from mkx.process_key_event import process_key_event as _process_key_event

FRAME_INTERVAL_MS = 5


class MKX_Abstract:
    def __init__(self, keymap=None):
        print("MKX -> Start:")

        self.col_size = 0
        self.row_size = 0
        self.keymap = keymap or []
        self.interfaces = []

        self.last_frame_time = 0
        self.pressed_keys = {}

        self.timed_keys_manager = TimedKeysManager()
        self.sticky_key_manager = StickyKeyManager()
        self.layers_manager = LayersManager(default_layer=0)

        self.backlight = None

        self._use_ble = False
        self._ble = None

        self.keyboard = None

    def _init_keyboard(self):
        if check(self.col_size, self.row_size, self.keymap, self.interfaces):
            sys.exit(1)

        if self._use_ble:
            self._ble = BLE()
            self._ble.init()
            self.keyboard = Keyboard(self._ble.devices)
        else:
            self.keyboard = Keyboard(usb_hid.devices)

    def use_ble(self, use_ble: bool):
        self._use_ble = use_ble

    def add_interface(self, interface: InterfaceAbstract):
        self.interfaces.append(interface)

    def add_layer_status_led(self, status_led: LayerStatusLedAbstract):
        self.layers_manager.add_layer_status_led(status_led)

    def add_keymap(self, keymap, col_size, row_size):
        self.keymap = keymap
        self.col_size = col_size
        self.row_size = row_size

        if not all(len(row) == col_size * row_size for row in keymap):
            print("Keymap layers must be rectangular and match given size!")
            sys.exit(1)

    def add_backlight(self, backlight: BacklightAbstract):
        self.backlight = backlight

    def process_key_event(self, device_id, logical_index, pressed, timestamp):
        _process_key_event(self, device_id, logical_index, pressed, timestamp)

    def run_once(self):
        # if self._use_ble:
        #     self._ble.ensure_advertising()

        #     if not self._ble.devices:
        #         return

        # now = time.monotonic_ns() // 1_000_000
        # if now - self.last_frame_time < FRAME_INTERVAL_MS:
        #     return

        # events = self.collect_key_events()

        # self.timed_keys_manager.update(self.layers_manager, self.keyboard, now)

        # for event in events:
        #     self.process_key_event(event)

        # if self.backlight:
        #     self.backlight.shine()

        # self.last_frame_time = now
        pass

    def run_forever(self):
        if self._init_keyboard():
            sys.exit(1)

        self.last_frame_time = time.monotonic_ns() // 1_000_000
        while True:
            self.run_once()
