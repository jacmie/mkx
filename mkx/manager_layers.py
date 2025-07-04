from mkx.layer_status_led_abstract import LayerStatusLedAbstract


class LayersManager:
    def __init__(self, default_layer=0):
        self.default_layer = default_layer
        self.active_layers = [default_layer]
        self.status_led = None
        self._update_status_led()

    def _update_status_led(self):
        if self.status_led:
            self.status_led.update_status_led(self.get_top_layer())

    def add_layer_status_led(self, status_led: LayerStatusLedAbstract):
        self.status_led = status_led
        self._update_status_led()

    def activate_layer(self, layer, *, prioritize=False):
        if layer in self.active_layers:
            if prioritize:
                self.active_layers.remove(layer)
                self.active_layers.append(layer)
        else:
            self.active_layers.append(layer)
        self._update_status_led()

    def deactivate_layer(self, layer):
        if layer in self.active_layers and layer != self.default_layer:
            self.active_layers.remove(layer)
        self._update_status_led()

    def set_active_layer(self, layer):
        self.active_layers = [layer]
        self._update_status_led()

    def set_default_layer(self, layer):
        self.default_layer = layer
        if layer not in self.active_layers:
            self.active_layers.insert(0, layer)
        self._update_status_led()

    def toggle_layer(self, layer, *, prioritize=False):
        if layer in self.active_layers:
            self.deactivate_layer(layer)
        else:
            self.activate_layer(layer, prioritize=prioritize)

    def get_top_layer(self):
        return self.active_layers[-1] if self.active_layers else self.default_layer
