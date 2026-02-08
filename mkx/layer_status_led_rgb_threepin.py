import adafruit_rgbled

from mkx.layer_status_led_abstract import LayerStatusLedAbstract


class LayerStatusLedRgbThreePin(LayerStatusLedAbstract):
    """
    RGB status LED driver using adafruit_rgbled.RGBLED.

    Args:
        red_pin, green_pin, blue_pin: microcontroller.Pin (or PWM-capable pins)
        brightness: float 0.0 - 1.0
        common_anode: True if common-anode LED, False (default) if common-cathode
    """

    def __init__(
        self, red_pin, green_pin, blue_pin, brightness=1.0, common_anode=False
    ):
        # invert_pwm = True for common anode, False for common cathode
        self.led = adafruit_rgbled.RGBLED(
            red_pin, green_pin, blue_pin, invert_pwm=bool(common_anode)
        )

        # Clamp brightness between 0.0 and 1.0
        self.brightness = max(0.0, min(1.0, brightness))

        # layers - raw RGB colors (0–255)
        self.layer_colors = {}

    def add_layer(self, layer: int, color):
        """
        Add a layer color.
        color: (R, G, B) tuple with 0–255 values.
        """
        # Clamp values and store
        r, g, b = color
        r = max(0, min(255, r))
        g = max(0, min(255, g))
        b = max(0, min(255, b))
        self.layer_colors[layer] = (r, g, b)

    def update_status_led(self, layer: int):
        """
        Set the RGBLED to show the color for the given layer,
        applying brightness scaling.
        """
        # Get RGB tuple or black if not found
        r, g, b = self.layer_colors.get(layer, (0, 0, 0))

        # Scale by brightness (0–1.0) then assign to the LED
        self.led.color = (
            int(r * self.brightness),
            int(g * self.brightness),
            int(b * self.brightness),
        )
