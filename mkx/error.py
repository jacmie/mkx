import time
import math

from mkx.layer_status_led_abstract import LayerStatusLedAbstract
from mkx.layer_status_led_rgb_neopixel import LayerStatusLedRgbNeoPixel
from mkx.layer_status_led_rgb_threepin import LayerStatusLedRgbThreePin
from mkx.layer_status_led_array import LayerStatusLedArray
from mkx.ansi_colors import Ansi, Ansi256

# NOTE:
# In CircuitPython, uncaught exceptions or sys.exit() at top level cause Safe Mode.
# Safe Mode makes the filesystem read-only, preventing users from fixing config
# files without a hard reset.
#
# For configuration errors, we therefore halt execution using an infinite loop
# instead of crashing or resetting. This keeps the device usable and recoverable.


def halt_on_error(
    message: str,
    status_led: LayerStatusLedAbstract | None = None,
    fade_speed: float = 0.02,  # smaller = slower fade
):
    """
    Halt program due to fatal configuration error.

    LED patterns:
    - RGB NeoPixel: red smoothly fades in/out
    - RGB three-pin: red smoothly fades in/out
    - LED Array: red-like fade effect per LED in wave
    - Fallback: built-in LED hard blink

    Infinite loop keeps USB/filesystem alive.
    """

    print()
    print(
        f"{Ansi.BOLD}{Ansi.BG_RED}{Ansi.WHITE}ERROR >>>{Ansi.RESET} "
        f"{Ansi256.LIGHT_ORANGE}{message}{Ansi.RESET}"
    )
    print()
    print(
        f"{Ansi256.PEACH}Fix the configuration and press "
        f"{Ansi.BOLD}{Ansi.YELLOW}Ctrl+D{Ansi.RESET}{Ansi256.PEACH} to reload.{Ansi.RESET}"
    )
    print()

    t = 0  # time counter for smooth fade

    while True:
        if isinstance(status_led, LayerStatusLedRgbNeoPixel):
            brightness = int((math.sin(t / 10) * 0.5 + 0.5) * 255)
            status_led.pixel[0] = (brightness, 0, 0)
            status_led.pixel.show()

        elif isinstance(status_led, LayerStatusLedRgbThreePin):
            brightness = int((math.sin(t / 10) * 0.5 + 0.5) * 255)
            status_led.led.color = (
                brightness,
                0,
                0,
            )

        # UNTESTED
        # elif isinstance(status_led, LayerStatusLedArray):
        #     n = len(status_led.pins)
        #     for i, pin in enumerate(status_led.pins):
        #         # Each LED gets a sine wave offset by its index
        #         val = math.sin(t / 10 + i * math.pi / n) * 0.5 + 0.5
        #         pin.value = int(val > 0.5)  # simple approximation (on/off)

        t += 1
        time.sleep(fade_speed)
