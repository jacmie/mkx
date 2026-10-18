import digitalio
import usb_hid
from adafruit_hid.keyboard import Keyboard

from mkx.ble import BLE

from mkx.interface_abstract import InterfaceAbstract
from mkx.keys_abstract import KeysAbstract

from mkx.layer_status_led_abstract import LayerStatusLedAbstract
from mkx.manager_layers import LayersManager
from mkx.timed_keys import TimedKeysManager
from mkx.keys_sticky import StickyKeyManager
from mkx.backlight_abstract import BacklightAbstract

from mkx.check import check
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

        self._interrupt_pins = []

        self.keyboard = None

    def use_ble(self, use_ble: bool):
        self._use_ble = use_ble

    def use_interrupt(self, pin_list):
        """Register one or more active-low interrupt pins (e.g. MCP23017 INTA/INTB wired
        open-drain to a shared MCU pin) used to skip matrix scanning when none are asserted.
        Currently used only in the MKX_Single class.
        """
        if not isinstance(pin_list, (list, tuple)):
            pin_list = [pin_list]

        for pin in pin_list:
            dio = digitalio.DigitalInOut(pin)
            dio.switch_to_input(pull=digitalio.Pull.UP)
            self._interrupt_pins.append(dio)

    def _should_scan(self) -> bool:
        if not self._interrupt_pins:
            return True

        return any(not pin.value for pin in self._interrupt_pins)

    def use_rp_pio(self, use_rp_pio: bool):
        """Explicitly enable/disable rp2pio-accelerated matrix scanning on RP2040/RP2350 boards.

        Must be called before peripheries (and their MatrixScanner) are constructed.
        """
        from mkx.matrix_scanner_rp_pio import set_enabled

        set_enabled(use_rp_pio)

    def use_keypad_scan(self, use_keypad_scan: bool):
        """Explicitly enable/disable the CircuitPython keypad.KeyMatrix background scanner.

        Must be called before peripheries (and their MatrixScanner) are constructed.
        """
        from mkx.matrix_scanner_keypad import set_enabled

        set_enabled(use_keypad_scan)

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

        print(
            f"{Ansi256.LIGHT_GREEN}Keyboard initialized successfully! {Ansi.BOLD}TYPE!!!{Ansi.RESET}"
        )
        print()

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

    def run_once(self):
        raise NotImplementedError("Subclasses must implement run_once()")

    def run_forever(self):
        self._init_keyboard()

        while True:
            self.run_once()
