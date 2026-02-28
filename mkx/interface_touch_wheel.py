from mkx.interface_touch_slider import InterfaceTouchSlider
from mkx.slider_event import SliderEvent
from mkx.ansi_colors import Ansi, Ansi256


class InterfaceTouchWheel(InterfaceTouchSlider):
    def __init__(
        self,
        electrodes,
        slider_keymap,
        step_size=0.05,
        max_steps_per_loop=5,
        value_min=0.0,
        value_max=1.0,
    ):
        super().__init__(
            electrodes,
            slider_keymap,
            step_size,
            max_steps_per_loop,
            value_min,
            value_max,
        )

        self._last_norm = None

    def _resolve_absolute(self, values: dict):
        N = len(self.electrodes)

        total_weight = sum(values.values())
        weighted_sum = 0.0

        # First frame - no unwrap
        if self._last_norm is None:
            for index, weight in values.items():
                weighted_sum += index * weight

            avg_index = weighted_sum / total_weight
        else:
            ref_index = self._last_norm * N

            for index, weight in values.items():
                diff = index - ref_index

                if diff > N / 2:
                    index -= N
                elif diff < -N / 2:
                    index += N

                weighted_sum += index * weight

            avg_index = weighted_sum / total_weight

        avg_index %= N
        norm = avg_index / N

        self._last_norm = norm  # store circular position

        value = self.value_min + norm * (self.value_max - self.value_min)

        print(f"{Ansi256.SKY}[Wheel] normalized: {Ansi256.PEACH}{norm:.3f}{Ansi.RESET}")
        print(
            f"{Ansi256.SKY}[Wheel] absolute value: {Ansi256.PEACH}{value:.3f}{Ansi.RESET}"
        )

        return value

    def _resolve_delta(self, value, current_layer):
        events = []

        # Convert value - circular norm
        norm = (value - self.value_min) / (self.value_max - self.value_min)

        # Previous norm derived from last value
        prev_norm = (self._last_value - self.value_min) / (
            self.value_max - self.value_min
        )

        delta = norm - prev_norm

        # Shortest circular path
        if delta > 0.5:
            delta -= 1.0
        elif delta < -0.5:
            delta += 1.0

        print(f"{Ansi256.SKY}[Wheel] delta: {Ansi256.PEACH}{delta:.3f}{Ansi.RESET}")

        self.motion_accumulator += delta

        steps = int(self.motion_accumulator / self.step_size)

        if steps != 0:
            steps = max(
                -self.max_steps_per_loop,
                min(self.max_steps_per_loop, steps),
            )

            self.motion_accumulator -= steps * self.step_size

            print(f"{Ansi256.SKY}[Wheel] steps: {Ansi256.PEACH}{steps}{Ansi.RESET}")

            key_inc, key_dec = self._get_slider_keys(current_layer)

            if steps > 0:
                for _ in range(steps):
                    events.append(SliderEvent(key_inc, True))
                    events.append(SliderEvent(key_inc, False))
            else:
                for _ in range(-steps):
                    events.append(SliderEvent(key_dec, True))
                    events.append(SliderEvent(key_dec, False))

        return events

    def process(self, values: dict, current_layer=0):
        if not values:
            self._last_norm = None
        return super().process(values, current_layer)
