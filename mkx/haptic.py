import time
import digitalio

import adafruit_drv2605
from mkx.ansi_colors import Ansi, Ansi256


class Haptic:
    def __init__(self, i2c, effect_id, enable_pin, duration=None, play_on_init=False):
        # Haptic motor driver, fixed address 0x5A
        self.haptic = adafruit_drv2605.DRV2605(i2c)
        self.haptic.sequence[0] = adafruit_drv2605.Effect(effect_id)

        if enable_pin is not None:
            # EN (Enable) pin - must be HIGH for DRV2605 to work
            en = digitalio.DigitalInOut(enable_pin)
            en.direction = digitalio.Direction.OUTPUT
            en.value = True
        else:
            print(
                f"{Ansi256.PEACH}Warning: No enable pin provided for Haptic. Ensure DRV2605 EN pin is HIGH to make it work!{Ansi.RESET}"
            )

        self.duration = duration

        self.electrodes = None

        if play_on_init:
            self.play_effect(None, None)

    def _flatten_electrodes(self, electrodes_dict):
        result = []

        for addr, electrodes in electrodes_dict.items():
            for ele in electrodes:
                result.append((addr, ele))  # tuple instead of dict
                print(f"{Ansi256.SKY}(0x{addr:02X}, {ele}){Ansi.RESET}")
        print()

        return tuple(result)

    def set_ERM_motor(self):
        self.haptic.use_ERM()

    def set_LRM_motor(self):
        self.haptic.use_LRM()

    def set_electrodes(self, electrodes):
        print(f"{Ansi256.MINT}Haptic electrodes:{Ansi.RESET}")
        self.electrodes = self._flatten_electrodes(electrodes)

    def play_effect(self, address, electrode_numbers):
        if self.electrodes is None:
            # No filter always play
            print(f"Haptic_click")
            self.haptic.play()
            if self.duration:
                time.sleep(self.duration)
                self.haptic.stop()
        else:
            # Check if ANY active electrode is in the filter
            for ele in electrode_numbers:
                if (address, ele) in self.electrodes:
                    print(f"Haptic_click")
                    self.haptic.play()
                    if self.duration:
                        time.sleep(self.duration)
                        self.haptic.stop()
                    break  # Play only once
