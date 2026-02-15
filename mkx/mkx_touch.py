import time

from mkx.mkx_abstract import MKX_Abstract
from mkx.periphery_touch import PeripheryTouch

from mkx.process_key_event import process_key_event
from mkx.error import halt_on_error
from mkx.ansi_colors import Ansi, Ansi256


class MKX_Touch(MKX_Abstract):
    def __init__(self):
        super().__init__()
        self.irq = False
        self.mpr121 = None
        self.last_state = [False] * 12  # track last state of each electrode
        self.peripherys_touch = []
        self.electrodes_map = {}
        self.last_touch_state = {}

    def use_irq(self, irq_pin: bool):
        self.irq = irq_pin

    def add_periphery_touch(self, periphery_touch: PeripheryTouch):
        self.peripherys_touch.append(periphery_touch)

    def _init_keyboard(self):
        for iface in self.interfaces:
            # columns
            if iface.electrodes_col:
                for addr_pin in iface.electrodes_col:
                    self.electrodes_map[addr_pin] = iface

            # rows
            if iface.electrodes_row:
                for addr_pin in iface.electrodes_row:
                    self.electrodes_map[addr_pin] = iface

            # flat electrodes (if used)
            if iface.electrodes:
                for addr_pin in iface.electrodes:
                    self.electrodes_map[addr_pin] = iface

        print(f"{Ansi256.MINT}{Ansi.BOLD}electrodes_map:{Ansi.RESET}")
        for address, pin in sorted(self.electrodes_map):
            iface = self.electrodes_map[(address, pin)]
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
                for (address, pin), iface in self.electrodes_map.items():
                    if address == periphery.address:
                        periphery.use2electrodes = bool(
                            iface.electrodes_col and iface.electrodes_row
                        )
                        break
                else:
                    halt_on_error(
                        f"No interface found with this address registered: 0x{address:02X}!\nCheck interfaces electrodes configuration.",
                        status_led=getattr(self.layers_manager, "status_led", None),
                    )

            print(
                f"{Ansi256.MINT}address 0x{periphery.address:02X}: {Ansi.RESET}"
                f"{Ansi256.PEACH}use2electrodes = {periphery.use2electrodes}{Ansi.RESET}"
            )
        print()

        super()._init_keyboard()

    def _get_interface(self, address, ele):
        addr_ele = (address, ele)
        iface = self.electrodes_map.get(addr_ele)

        if iface is None:
            halt_on_error(
                f"No registered electrode: 0x{address:02X}, {ele}!\nCheck interfaces electrodes configuration.",
                status_led=getattr(self.layers_manager, "status_led", None),
            )

        return iface

    def _add_logical_event(self, logical_index: int, is_pressed: bool, events: list):
        if logical_index is None:
            halt_on_error(
                f"Couldn't determin logical_index for the keymap!\nCheck keymap and interfaces configuration.",
                status_led=getattr(self.layers_manager, "status_led", None),
            )

        events.append((logical_index, is_pressed))
        state_str = "pressed" if is_pressed else "released"
        print(
            f"{Ansi256.SKY}Logical key {Ansi256.PEACH}{logical_index} {state_str}{Ansi.RESET}"
        )

    def _handle_electrode_event(
        self,
        periphery,
        electrode_set,
        is_pressed: bool,
        events: list,
        pair_mode: bool = False,
    ):
        if not electrode_set:
            return

        if pair_mode:
            if len(electrode_set) != 2:
                return
            ele1, ele2 = tuple(electrode_set)
            iface = self._get_interface(periphery.address, ele1)
            logical_index = iface.get_logical_index_for_electrode_pair(
                periphery.address, ele1, ele2
            )
            self._add_logical_event(logical_index, is_pressed, events)
        else:
            for ele in electrode_set:
                iface = self._get_interface(periphery.address, ele)
                logical_index = iface.get_logical_index_for_electrode(
                    periphery.address, ele
                )
                self._add_logical_event(logical_index, is_pressed, events)

    def _collect_electrode_events(self):
        if not self.peripherys_touch:
            halt_on_error(
                "No periphery touch registered!",
                status_led=getattr(self.layers_manager, "status_led", None),
            )

        events = []

        for periphery in self.peripherys_touch:
            result = periphery.touched_electrodes()

            current_pins = set(result[1]) if result else set()

            # Get previous state for this device
            previous_pins = self.last_touch_state.get(periphery.address, set())

            # If nothing changed, skip this periphery
            if current_pins == previous_pins:
                continue

            # Save new state
            self.last_touch_state[periphery.address] = current_pins

            # Detect changes
            pressed = current_pins - previous_pins
            released = previous_pins - current_pins

            self._handle_electrode_event(
                periphery, pressed, True, events, pair_mode=periphery.use2electrodes
            )
            self._handle_electrode_event(
                periphery, released, False, events, pair_mode=periphery.use2electrodes
            )

        return events

    def run_once(self):
        # print(f"{Ansi.YELLOW}{Ansi.BOLD}=== run_once ==={Ansi.RESET}")
        if not self._ensure_ble():
            return

        now = time.monotonic_ns() // 1_000_000

        self.timed_keys_manager.update(self.layers_manager, self.keyboard, now)

        for event in self._collect_electrode_events():
            logical_index, pressed = event

            process_key_event(self, "periphery_touch", logical_index, pressed, now)

        if self.backlight:
            self.backlight.shine()

        time.sleep(0.01)  # Keep CPU usage low
        # time.sleep(1.001)  # Keep CPU usage low

    def run_forever(self):
        self._init_keyboard()

        while True:
            self.run_once()
