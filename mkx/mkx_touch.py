import time

from mkx.mkx_abstract import MKX_Abstract
from mkx.periphery_touch import PeripheryTouch
from mkx.slider_event import SliderEvent
from mkx.interface_touch_slider import InterfaceTouchSlider

from mkx.process_key_event import process_key_event
from mkx.error import halt_on_error
from mkx.ansi_colors import Ansi, Ansi256


class MKX_Touch(MKX_Abstract):
    def __init__(self):
        super().__init__()
        self.irq = False
        self.mpr121 = None
        self.peripherys_touch = []
        self.electrodes_map = {}

    def use_irq(self, irq_pin: bool):
        self.irq = irq_pin

    def add_periphery_touch(self, periphery_touch: PeripheryTouch):
        self.peripherys_touch.append(periphery_touch)

    def _init_keyboard(self):
        for iface in self.interfaces:
            # columns
            if hasattr(iface, "electrodes_col") and iface.electrodes_col:
                for addr_pin in iface.electrodes_col:
                    self.electrodes_map[addr_pin] = iface

            # rows
            if hasattr(iface, "electrodes_row") and iface.electrodes_row:
                for addr_pin in iface.electrodes_row:
                    self.electrodes_map[addr_pin] = iface

            # flat electrodes (if used)
            if hasattr(iface, "electrodes") and iface.electrodes:
                for addr_pin in iface.electrodes:
                    self.electrodes_map[addr_pin] = iface

        print(f"{Ansi256.MINT}{Ansi.BOLD}electrodes_map:{Ansi.RESET}")
        for key in sorted(self.electrodes_map.keys()):
            if isinstance(key, tuple) and len(key) == 2:
                address, pin = key
                iface = self.electrodes_map[key]
                print(
                    f"{Ansi256.SKY}(0x{address:02X}, {pin}): interface[{self.interfaces.index(iface)}]{Ansi.RESET}"
                )
        print()

        print(
            f"{Ansi256.MINT}{Ansi.BOLD}Periphery use2electrodes settings:{Ansi.RESET}"
        )
        for periphery in self.peripherys_touch:
            # set use2electrodes if not set explicitly, based on interfaces configuration
            if periphery.use2electrodes is None:
                periphery.use2electrodes = False
                for key, iface in self.electrodes_map.items():
                    if isinstance(key, tuple) and len(key) == 2:
                        address, pin = key
                        if address == periphery.address:
                            periphery.use2electrodes = bool(
                                hasattr(iface, "electrodes_col")
                                and iface.electrodes_col
                                and hasattr(iface, "electrodes_row")
                                and iface.electrodes_row
                            )
                            break
                # else:
                #     halt_on_error(
                #         f"No interface found with this address registered: 0x{periphery.address:02X}!\nCheck interfaces electrodes configuration.",
                #         status_led=getattr(self.layers_manager, "status_led", None),
                #     )

            print(
                f"{Ansi256.MINT}address 0x{periphery.address:02X}: {Ansi.RESET}"
                f"{Ansi256.PEACH}use2electrodes = {periphery.use2electrodes}{Ansi.RESET}"
            )
        print()

        super()._init_keyboard()

    def _collect_electrode_events(self):
        if not self.peripherys_touch:
            halt_on_error(
                "No periphery touch registered!",
                status_led=getattr(self.layers_manager, "status_led", None),
            )

        events = []

        for periphery in self.peripherys_touch:
            values = periphery.electrode_values()
            if values is None:
                continue

            for iface in self.interfaces:
                # Pass current layer to slider/wheel interfaces for layer-aware key selection
                if isinstance(iface, InterfaceTouchSlider):
                    interface_events = iface.process(
                        periphery.address,
                        values,
                        current_layer=self.layers_manager.get_top_layer(),
                    )
                else:
                    interface_events = iface.process(periphery.address, values)

                if interface_events:
                    events.extend(interface_events)

        return events

    def _handle_slider_event(self, event, now):
        action = "pressed" if event.is_pressed else "released"

        print(
            f"{Ansi.YELLOW}{Ansi.BOLD}"
            f"key: {event.key.key_name} {action}"
            f"{Ansi.RESET}"
        )

        if event.is_pressed:
            event.key.on_press(self.layers_manager, self.keyboard, now)
        else:
            event.key.on_release(self.layers_manager, self.keyboard, now)

        print()

    def run_once(self):
        # print(f"{Ansi.YELLOW}{Ansi.BOLD}=== run_once ==={Ansi.RESET}")
        if not self._ensure_ble():
            return

        now = time.monotonic_ns() // 1_000_000

        self.timed_keys_manager.update(self.layers_manager, self.keyboard, now)

        for event in self._collect_electrode_events():
            if isinstance(event, SliderEvent):
                self._handle_slider_event(event, now)
            else:
                logical_index, pressed = event
                process_key_event(self, "periphery_touch", logical_index, pressed, now)

        if self.backlight:
            self.backlight.shine()

        time.sleep(0.01)  # Keep CPU usage low

    def run_forever(self):
        self._init_keyboard()

        while True:
            self.run_once()
