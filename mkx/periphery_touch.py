import digitalio

import adafruit_mpr121

from mkx.error import halt_on_error
from mkx.ansi_colors import Ansi, Ansi256


class PeripheryTouch:
    def __init__(self, i2c, address=0x5B, irq_pin=None):
        self.address = address
        self.mpr121 = adafruit_mpr121.MPR121(i2c, address)
        self.irq_pin = None
        self.use2electrodes = None
        self.previous_touch_state = None

        if irq_pin is not None:
            self.irq_pin = digitalio.DigitalInOut(irq_pin)
            self.irq_pin.direction = digitalio.Direction.INPUT
            self.irq_pin.pull = digitalio.Pull.UP

    def fire_only_on_2electrodes(self, enable):
        self.use2electrodes = enable

    def set_thresholds(self, touch=12, release=6):
        if release >= touch:
            halt_on_error("Release threshold must be lower than touch threshold!")

        for i in range(12):
            self.mpr121[i].threshold = touch

    def get_thresholds(self):
        touch = self.mpr121[0].threshold
        release = self.mpr121[0].release_threshold
        return touch, release

    def _electrodes_plot(self, values_dict, threshold=12):
        lines = []

        # Layout configuration
        total_width = 80
        left_margin = 14  # space for "idx | value | "
        plot_width = total_width - left_margin
        # half_width = plot_width // 2  # space left/right of zero
        half_width = 20  # space left/right of zero

        min_val = min(values_dict.values(), default=0)
        max_val = max(values_dict.values(), default=0)

        max_abs = max(abs(min_val), abs(max_val), threshold)

        # Determine scaling only if needed
        scale = 1
        if max_abs > half_width:
            scale = max_abs / half_width

        for idx in sorted(values_dict.keys()):
            value = values_dict[idx]

            idx_str = f"{idx:2d}"
            val_str = f"{value:4d}"

            # Create empty plot buffer
            plot = [" "] * plot_width

            zero_pos = half_width

            # Draw zero axis
            plot[zero_pos] = "|"

            # Compute scaled blocks
            scaled_value = int(value / scale)
            scaled_threshold = int(threshold / scale)

            if scaled_value < 0:
                # Negative (all red)
                for i in range(abs(scaled_value)):
                    pos = zero_pos - 1 - i
                    if pos >= 0:
                        plot[pos] = "\033[91m█\033[0m"

            elif scaled_value > 0:
                for i in range(scaled_value):
                    pos = zero_pos + 1 + i
                    if pos < plot_width:
                        if i < scaled_threshold:
                            plot[pos] = "\033[91m█\033[0m"
                        else:
                            plot[pos] = "\033[92m█\033[0m"

            line_plot = "".join(plot)

            lines.append(f"{idx_str} | {val_str} | {line_plot}")

        return "\n".join(lines)

    def _get_two_active_electrodes(self, touch_bits):
        # Clear the lowest active bit
        x = touch_bits & (touch_bits - 1)

        # Check if original number had exactly two bits set
        if x and (x & (x - 1)) == 0:
            # Extract first (lowest) active bit
            first = (touch_bits & -touch_bits).bit_length() - 1
            # Extract second active bit
            second = (x & -x).bit_length() - 1

            return first, second

        return None

    def electrode_values(self):
        # If irq_pin is set, only read when irq pin value is LOW (active)
        if self.irq_pin is not None and self.irq_pin.value:
            return None

        if self.use2electrodes:
            # In matrix mode, track two active electrodes and fire on state changes
            touch_bits = self.mpr121.touched()
            active_electrodes = self._get_two_active_electrodes(touch_bits)

            # Only return data if state changed (press or release)
            if active_electrodes != self.previous_touch_state:
                self.previous_touch_state = active_electrodes

                if active_electrodes is not None:
                    ele1, ele2 = active_electrodes
                    press_threshold, release_threshold = self.get_thresholds()
                    values = {ele1: press_threshold + 10, ele2: press_threshold + 10}
                    print(
                        f"{Ansi256.SKY}Two active electrodes: {Ansi256.PEACH}{active_electrodes}{Ansi.RESET}"
                    )
                    return values
                else:
                    # Electrodes were released
                    print(f"{Ansi256.SKY}Electrodes released{Ansi.RESET}")
                    return {}

            return None
        else:
            # In single electrode mode, track state changes and filter by touch threshold
            touch_threshold, _ = self.get_thresholds()

            # Calculate values for all electrodes
            all_values = {}
            for i in range(12):
                value = self.mpr121.baseline_data(i) - self.mpr121.filtered_data(i)
                all_values[i] = value

            # Determine which electrodes are above touch threshold
            active_electrodes = frozenset(
                i for i in range(12) if all_values[i] >= touch_threshold
            )

            # Only return data if state changed (press or release)
            if active_electrodes != self.previous_touch_state:
                self.previous_touch_state = active_electrodes

                if active_electrodes:
                    # Return only values for active electrodes
                    values = {i: all_values[i] for i in active_electrodes}
                    print(
                        f"{Ansi256.SKY}\nActive electrodes: {Ansi256.PEACH}{sorted(active_electrodes)}{Ansi.RESET}"
                    )
                    print(
                        f"{self._electrodes_plot(values, touch_threshold)}{Ansi.RESET}"
                    )
                    return values
                else:
                    # All electrodes released
                    print(f"{Ansi256.SKY}All electrodes released{Ansi.RESET}")
                    return {}

            return None
