from mkx.layer_status_led_abstract import LayerStatusLedAbstract


class LayerStatusLedArray(LayerStatusLedAbstract):
    def __init__(self, pins):
        self.pins = pins

    def update_status_led(self, layer: int):
        for i, pin in enumerate(self.pins):
            pin.value = i == layer
