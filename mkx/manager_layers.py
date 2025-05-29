class LayersManager:
    def __init__(self, default_layer=0):
        self.default_layer = default_layer
        self.active_layers = [default_layer]

    def activate_layer(self, layer, *, prioritize=False):
        if layer in self.active_layers:
            if prioritize:
                self.active_layers.remove(layer)
                self.active_layers.append(layer)
        else:
            self.active_layers.append(layer)

    def deactivate_layer(self, layer):
        if layer in self.active_layers and layer != self.default_layer:
            self.active_layers.remove(layer)

    def set_active_layer(self, layer):
        self.active_layers = [layer]

    def set_default_layer(self, layer):
        self.default_layer = layer
        if layer not in self.active_layers:
            self.active_layers.insert(0, layer)

    def toggle_layer(self, layer, *, prioritize=False):
        if layer in self.active_layers:
            self.deactivate_layer(layer)
        else:
            self.activate_layer(layer, prioritize=prioritize)

    def get_top_layer(self):
        print("active_layers:", self.active_layers)
        return self.active_layers[-1] if self.active_layers else self.default_layer
