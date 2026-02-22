from mkx.interface_abstract import InterfaceAbstract
from mkx.keys_abstract import KeysAbstract
from mkx.ansi_colors import Ansi, Ansi256
from mkx.slider_event import SliderEvent


class InterfaceTouchSlider(InterfaceAbstract):
    def __init__(
        self,
        electrodes,
        key_increase: KeysAbstract,
        key_decrease: KeysAbstract,
        value_min=0.0,
        value_max=1.0,
        step_size=0.05,
        max_steps_per_loop=5,
    ):
        """
        electrodes: tuple/list of (address, pin)
        """
        super().__init__("touch_slider", 0, 0, 0, 0)

        self.electrodes = tuple(electrodes)
        self.key_increase = key_increase
        self.key_decrease = key_decrease
        self.value_min = value_min
        self.value_max = value_max
        self.step_size = step_size
        self.max_steps_per_loop = max_steps_per_loop

        self._last_value = None
        self._last_active = {}  # Track previous state per address
        self.motion_accumulator = 0.0  # Accumulate delta for step generation

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

    # ----------------------------------------
    # Absolute value (0.0 - 1.0)
    # ----------------------------------------

    def resolve_absolute(self, address, values: dict):
        total_weight = sum(values.values())
        weighted_sum = sum(index * value for index, value in values.items())
        weighted_avg_index = weighted_sum / total_weight

        # Normalize to 0-1 range
        norm = weighted_avg_index / (len(self.electrodes) - 1)

        # Map to slider range
        value = self.value_min + norm * (self.value_max - self.value_min)

        print(
            f"{Ansi256.SKY}[Slider] total weight: {Ansi256.PEACH}{total_weight}{Ansi.RESET}"
        )
        print(
            f"{Ansi256.SKY}[Slider] weighted avg index: {Ansi256.PEACH}{weighted_avg_index:.2f}{Ansi.RESET}"
        )
        print(
            f"{Ansi256.SKY}[Slider] normalized: {Ansi256.PEACH}{norm:.2f}{Ansi.RESET}"
        )
        print(
            f"{Ansi256.SKY}[Slider] absolute value: {Ansi256.PEACH}{value:.3f}{Ansi.RESET}"
        )

        return value

    # ----------------------------------------
    # Incremental (delta)
    # ----------------------------------------

    def resolve_delta(self, address, active_pins):
        value = self.resolve_absolute(address, active_pins)

        if value is None:
            return None

        if self._last_value is None:
            self._last_value = value
            print(
                f"{Ansi256.SKY}[Slider] initial position set to {Ansi256.PEACH}{value:.3f}{Ansi.RESET}"
            )
            return 0

        delta = value - self._last_value
        self._last_value = value

        print(f"{Ansi256.SKY}[Slider] delta: {Ansi256.PEACH}{delta:.3f}{Ansi.RESET}")

        return delta

    def _accumulate_and_generate_events(self, delta, events):
        """
        Accumulate delta motion and generate slider events when threshold is crossed.

        Returns: updated events list
        """
        # Accumulate motion
        self.motion_accumulator += delta
        print(
            f"{Ansi256.SKY}[Slider] accumulated: {Ansi256.PEACH}{self.motion_accumulator:.3f}{Ansi.RESET}"
        )

        # Convert accumulated motion to discrete steps
        steps = int(self.motion_accumulator / self.step_size)

        if steps != 0:
            # Limit burst size
            steps = max(
                -self.max_steps_per_loop,
                min(self.max_steps_per_loop, steps),
            )
            self.motion_accumulator -= steps * self.step_size

            print(f"{Ansi256.SKY}[Slider] steps: {Ansi256.PEACH}{steps}{Ansi.RESET}")

            # Generate events
            if steps > 0:
                for _ in range(steps):
                    events.append(SliderEvent(self.key_increase, True))
                    events.append(SliderEvent(self.key_increase, False))
                    print(
                        f"{Ansi256.SKY}[Slider] {Ansi256.PEACH}{self.key_increase.key_name}{Ansi.RESET}"
                    )
            else:
                for _ in range(-steps):
                    events.append(SliderEvent(self.key_decrease, True))
                    events.append(SliderEvent(self.key_decrease, False))
                    print(
                        f"{Ansi256.SKY}[Slider] {Ansi256.PEACH}{self.key_decrease.key_name}{Ansi.RESET}"
                    )

        return events

    def process(self, address, values: dict):
        events = []

        if values:
            value = self.resolve_absolute(address, values)

            if value is not None:
                # Calculate delta on first touch or on ongoing motion
                if self._last_value is None:
                    self._last_value = value
                    print(
                        f"{Ansi256.SKY}[Slider] initial position set to {Ansi256.PEACH}{value:.3f}{Ansi.RESET}"
                    )
                else:
                    delta = value - self._last_value
                    self._last_value = value
                    print(
                        f"{Ansi256.SKY}[Slider] delta: {Ansi256.PEACH}{delta:.3f}{Ansi.RESET}"
                    )

                    # Accumulate motion and generate events
                    events = self._accumulate_and_generate_events(delta, events)
        else:
            print(f"{Ansi256.SKY}[Slider] all electrodes released{Ansi.RESET}")
            self._last_value = None
            self.motion_accumulator = 0.0  # Reset accumulator on release

        return events


# Want It Even Smoother?
# Add velocity scaling:

# speed = abs(delta)

# if speed > 0.2:
#     STEP_SIZE = 0.02
# elif speed > 0.05:
#     STEP_SIZE = 0.03
# else:
#     STEP_SIZE = 0.05

# Now:
# Slow move → precise
# Fast spin → scrubs faster
