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

    def handle_keypad(self, index, touched):
        key = index
        if touched:
            # haptic_click()
            print(f"[KEYPAD] Key {key} touched")
        else:
            print(f"[KEYPAD] Key {key} released")

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

        print("electrodes_map")
        for address, pin in sorted(self.electrodes_map.keys()):
            print(f"(0x{address:02X}, {pin}): {self.electrodes_map[(address, pin)]}")
        print()

        super()._init_keyboard()

    def _touch_to_logical_index(self, address, ele):
        addr_pin = (address, ele)
        iface = self.electrodes_map.get(addr_pin)

        if iface is None:
            halt_on_error(
                f"No registered electrode: 0x{address:02X}, {ele}!\nCheck interfaces electrodes configuration.",
                status_led=getattr(self.layers_manager, "status_led", None),
            )

        # iface = self.self.electrodes_map[addr_pin]

        # try:
        #     idx_inside = iface.electrodes.index(ele)
        # except ValueError:
        #     print(f"[DEBUG] Electrode {ele} not found in iface.electrodes")
        #     return None

        # local_row = idx_inside // iface.num_cols
        # local_col = idx_inside % iface.num_cols

        # return iface.logical_index(local_col, local_row)

        return iface.get_logical_index_for_electrode(address, ele)

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
                # Optional debug log:
                # print(
                #     f"[DEBUG] No change on periphery 0x{periphery.address:02X}, skipping."
                # )
                continue

            # Save new state
            self.last_touch_state[periphery.address] = current_pins

            # Detect changes
            pressed = current_pins - previous_pins
            released = previous_pins - current_pins
            print(
                f"[DEBUG] Periphery {periphery.address} pressed: {pressed}, released: {released}"
            )

            # Pressed events
            for ele in pressed:
                if periphery.use2electrodes:
                    ele1, ele2 = tuple(pressed)
                    addr_pin = (periphery.address, ele)
                    iface = self.electrodes_map.get(addr_pin)
                    logical_index = iface.get_logical_index_for_electrode_pair(
                        periphery.address, ele1, ele2
                    )
                else:
                    logical_index = self._touch_to_logical_index(periphery.address, ele)
                print("[DEBUG] Mapped to logical index:", logical_index)
                if logical_index is not None:
                    events.append((logical_index, True))
                    print(f"[DEBUG] Logical key {logical_index} pressed")

            # Released events
            for ele in released:
                if periphery.use2electrodes:
                    ele1, ele2 = tuple(released)
                    addr_pin = (periphery.address, ele)
                    iface = self.electrodes_map.get(addr_pin)
                    logical_index = iface.get_logical_index_for_electrode_pair(
                        periphery.address, ele1, ele2
                    )
                else:
                    logical_index = self._touch_to_logical_index(periphery.address, ele)
                print("[DEBUG] Mapped to logical index:", logical_index)
                if logical_index is not None:
                    events.append((logical_index, False))
                    print(f"[DEBUG] Logical key {logical_index} released")

        # if not events:
        #     print("[DEBUG] No key events detected this cycle")

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

        time.sleep(0.001)  # Keep CPU usage low
        # time.sleep(1.001)  # Keep CPU usage low

    def run_forever(self):
        self._init_keyboard()

        while True:
            self.run_once()
