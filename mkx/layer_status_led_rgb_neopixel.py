import neopixel

from mkx.layer_status_led_abstract import LayerStatusLedAbstract


class LayerStatusLedRgbNeoPixel(LayerStatusLedAbstract):
    def __init__(self, status_led_pin, brightness=0.3, auto_write=True):
        self.pixel = neopixel.NeoPixel(
            status_led_pin, 1, brightness=brightness, auto_write=auto_write
        )
        self.layer_colors = {}

    def update_status_led(self, layer: int):
        color = self.layer_colors.get(layer, (0, 0, 0))
        self.pixel[0] = color

    def add_layer(self, layer: int, color):
        self.layer_colors[layer] = color
