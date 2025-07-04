from mkx.layer_status_led_abstract import LayerStatusLedAbstract


class LayerStatusLedRgbThreePin(LayerStatusLedAbstract):
    def __init__(self, red_pin, green_pin, blue_pin):
        self.red_pin = red_pin
        self.green_pin = green_pin
        self.blue_pin = blue_pin

        self.layer_colors = {}

    def update_status_led(self, layer: int):
        r, g, b = self.layer_colors.get(layer, (0, 0, 0))
        self.red_pin.value = r
        self.green_pin.value = g
        self.blue_pin.value = b

    def add_layer(self, layer: int, color):
        self.layer_colors[layer] = color
