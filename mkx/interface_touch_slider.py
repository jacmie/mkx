from mkx.interface_abstract import InterfaceAbstract
from mkx.ansi_colors import Ansi, Ansi256


class InterfaceTouchSlider(InterfaceAbstract):
    def __init__(self, electrodes, value_min=0.0, value_max=1.0):
        """
        electrodes: tuple/list of (address, pin)
        """
        super().__init__("touch_slider", 0, 0, 0, 0)

        self.electrodes = tuple(electrodes)
        self.value_min = value_min
        self.value_max = value_max

        self._last_value = None
        self._last_active = {}  # Track previous state per address

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

    def process(self, address, values: dict):
        if values:
            value = self.resolve_absolute(address, values)

            if value is not None:
                # Update internal state for delta calculation
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
        else:
            print(f"{Ansi256.SKY}[Slider] all electrodes released{Ansi.RESET}")
            self._last_value = None

        return []


# Electrode strengths
#         ↓
# Interpolated position (float)
#         ↓
# Delta (movement)
#         ↓
# Accumulator
#         ↓
# Threshold crossed?
#         ↓
# Send HID key(s)

# Production-Grade Wheel → HID Example

# This assumes:
# 8 electrodes
# Circular layout
# You already compute angle using interpolation

# Step 1 — Global State

# import math
# from adafruit_hid.keycode import Keycode

# last_angle = None
# motion_accumulator = 0.0

# STEP_SIZE = 0.04        # Smaller = more sensitive
# MAX_STEPS_PER_LOOP = 5  # Prevent runaway

# Step 2 — Convert Angle to Motion

# def process_wheel(angle, keyboard):
#     global last_angle, motion_accumulator

#     if last_angle is None:
#         last_angle = angle
#         return

#     delta = angle - last_angle

#     # Wraparound correction
#     if delta > math.pi:
#         delta -= 2 * math.pi
#     elif delta < -math.pi:
#         delta += 2 * math.pi

#     last_angle = angle

#     # Add to accumulator
#     motion_accumulator += delta

#     # Convert motion into frame steps
#     steps = int(motion_accumulator / STEP_SIZE)

#     if steps != 0:
#         # Limit burst size
#         steps = max(-MAX_STEPS_PER_LOOP,
#                     min(MAX_STEPS_PER_LOOP, steps))

#         motion_accumulator -= steps * STEP_SIZE

#         send_steps(steps, keyboard)

# Step 3 — Send HID Keys

# def send_steps(steps, keyboard):
#     if steps > 0:
#         for _ in range(steps):
#             keyboard.send(Keycode.RIGHT_ARROW)
#     else:
#         for _ in range(-steps):
#             keyboard.send(Keycode.LEFT_ARROW)

# What This Achieves
# Slow finger movement → 1 frame at a time
# Faster spin → multiple frames
# No jitter
# No sudden jumps
# Natural acceleration feel
# This feels very close to a hardware jog wheel.

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

# Important
# Use:
# time.sleep(0.01–0.02)
# Not faster — or you’ll overwhelm the host with HID events.`
