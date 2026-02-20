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
        self.peripherys_touch = []
        self.electrodes_map = {}

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

    def _handle_electrode_event(self, periphery, used_electrodes, values, events):
        """
        Polymorphic dispatcher: let interfaces decide how to process values.
        Interfaces implement: process(address, values: dict, now: int) -> list[tuple]
        where each tuple is (logical_index, is_pressed)
        """
        print(used_electrodes)
        print(values)

        # Group electrodes by interface
        interfaces_seen = {}
        for ele in used_electrodes:
            iface = self._get_interface(periphery.address, ele)
            if iface not in interfaces_seen:
                interfaces_seen[iface] = iface

        # Call process() on each unique interface with all its electrode values
        for iface in interfaces_seen.values():
            # Filter values dict to only include electrodes this interface uses
            iface_values = {}
            for ele, value in values.items():
                if (
                    periphery.address,
                    ele,
                ) in self.electrodes_map and self.electrodes_map[
                    (periphery.address, ele)
                ] == iface:
                    iface_values[ele] = value

            if iface_values:
                # Call interface-specific processor
                interface_events = iface.process(periphery.address, iface_values)
                if interface_events:
                    events.extend(interface_events)

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

                interface_events = iface.process(periphery.address, values)
                if interface_events:
                    events.extend(interface_events)

            # values = result
            # self._handle_electrode_event(periphery, used_electrodes, values, events)

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

    def run_forever(self):
        self._init_keyboard()

        while True:
            self.run_once()
