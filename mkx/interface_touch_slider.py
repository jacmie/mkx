from mkx.interface_abstract import InterfaceAbstract
from mkx.slider_event import SliderEvent
from mkx.ansi_colors import Ansi, Ansi256
from mkx.error import halt_on_error


class InterfaceTouchSlider(InterfaceAbstract):
    def __init__(
        self,
        electrodes,
        slider_keymap,
        step_size=0.05,
        dynamic_step=False,
        max_steps_per_loop=5,
        value_min=0.0,
        value_max=1.0,
    ):
        super().__init__("touch_slider", 0, 0, 0, 0)

        self.electrodes = tuple(electrodes)
        self.slider_keymap = slider_keymap
        self.step_size = step_size
        self.max_steps_per_loop = max_steps_per_loop
        self.value_min = value_min
        self.value_max = value_max
        self.dynamic_step = dynamic_step

        self._last_value = None
        self.motion_accumulator = 0.0

        print(f"{Ansi256.MINT}electrodes:{Ansi.RESET}")
        self.electrodes = self._flatten_electrodes(electrodes)
        print(self.electrodes)

    def _flatten_electrodes(self, electrodes_dict):
        result = []

        for addr, electrodes in electrodes_dict.items():
            for ele in electrodes:
                result.append((addr, ele))  # tuple instead of dict
                print(f"{Ansi256.SKY}(0x{addr:02X}, {ele}){Ansi.RESET}")
        print()

        return tuple(result)

    def _get_slider_keys(self, current_layer):
        """
        Get slider keys for the given layer with safe fallback.

        Returns: (key_increase, key_decrease)
        Raises: halt_on_error if keys not defined or invalid
        """
        if not self.slider_keymap:
            halt_on_error("No slider keymap defined!")

        # Use the specified layer, fall back to layer 0 if it doesn't exist
        if current_layer < len(self.slider_keymap):
            key_increase, key_decrease = self.slider_keymap[current_layer]
        else:
            key_increase, key_decrease = self.slider_keymap[0]

        if key_increase is None or key_decrease is None:
            halt_on_error(f"No keys defined for layer {current_layer}!")

        return key_increase, key_decrease

    def _get_dynamic_step_size(self, delta):
        """
        Calculate dynamic step size based on movement speed.

        Fast movements → smaller steps for faster scrubbing
        Slow movements → larger steps for precise control

        Returns: dynamic step size clamped between min and max bounds
        """
        speed = abs(delta)

        # Ensure base step_size is valid
        base_step = max(self.step_size, 0.01)

        # Speed thresholds and resulting step sizes as fractions of base step
        threshold_fast = 4.0 * base_step
        threshold_medium = 1.5 * base_step

        if speed > threshold_fast:
            dynamic_step = 0.5 * base_step
        elif speed > threshold_medium:
            dynamic_step = 0.8 * base_step
        else:
            dynamic_step = 1.0 * base_step

        # Clamp to reasonable bounds
        min_step = 0.004
        max_step = 1.0
        return max(min_step, min(max_step, dynamic_step))

    def _resolve_absolute(self, values: dict):
        total_weight = sum(values.values())
        weighted_sum = sum(index * value for index, value in values.items())
        weighted_avg_index = weighted_sum / total_weight

        # Normalize to 0-1 range
        norm = weighted_avg_index / (len(self.electrodes) - 1)

        # Map to slider range
        value = self.value_min + norm * (self.value_max - self.value_min)

        print(
            f"{Ansi256.SKY}[Slider] normalized: {Ansi256.PEACH}{norm:.2f}{Ansi.RESET}"
        )
        print(
            f"{Ansi256.SKY}[Slider] absolute value: {Ansi256.PEACH}{value:.3f}{Ansi.RESET}"
        )

        return value

    def _resolve_delta(self, value, current_layer):
        events = []

        delta = value - self._last_value
        self._last_value = value
        print(f"{Ansi256.SKY}[Slider] delta: {Ansi256.PEACH}{delta:.3f}{Ansi.RESET}")

        if self.dynamic_step:
            step_size_to_use = self._get_dynamic_step_size(delta)
        else:
            step_size_to_use = self.step_size

        # Accumulate motion
        self.motion_accumulator += delta
        print(
            f"{Ansi256.SKY}[Slider] accumulated: {Ansi256.PEACH}{self.motion_accumulator:.3f}{Ansi.RESET}"
        )

        # Convert accumulated motion to discrete steps
        steps = int(self.motion_accumulator / step_size_to_use)

        if steps != 0:
            # Limit burst size
            steps = max(
                -self.max_steps_per_loop,
                min(self.max_steps_per_loop, steps),
            )
            self.motion_accumulator -= steps * step_size_to_use

            print(f"{Ansi256.SKY}[Slider] steps: {Ansi256.PEACH}{steps}{Ansi.RESET}")

            # Generate press-release events
            key_increase, key_decrease = self._get_slider_keys(current_layer)

            if steps > 0:
                for _ in range(steps):
                    events.append(SliderEvent(key_increase, True))
                    events.append(SliderEvent(key_increase, False))
            else:
                for _ in range(-steps):
                    events.append(SliderEvent(key_decrease, True))
                    events.append(SliderEvent(key_decrease, False))

        return events

    def process(self, values: dict, current_layer=0):
        events = []

        if values:
            value = self._resolve_absolute(values)

            if value is not None:
                if self._last_value is None:
                    self._last_value = value
                    print(
                        f"{Ansi256.SKY}[Slider] initial position set to {Ansi256.PEACH}{value:.3f}{Ansi.RESET}"
                    )
                else:
                    events = self._resolve_delta(value, current_layer)
        else:
            self._last_value = None
            self.motion_accumulator = 0.0  # Reset accumulator on release

        return events
