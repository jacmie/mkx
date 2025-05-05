import time


class KeyboardManager:
    def __init__(self, scanner, layers):
        """
        scanner: hardware scanner that returns currently pressed key positions (e.g., (row, col))
        layers: dict[int -> dict[position -> AbstractKey]]
        """
        self.scanner = scanner
        self.layers = layers  # layer_id: { (row, col): Key instance }
        self.active_layers = [0]  # Layer stack (0 is base)
        self._pressed_keys = {}  # position -> Key

    def get_active_key(self, position):
        for layer_id in reversed(self.active_layers):
            layer = self.layers.get(layer_id, {})
            key = layer.get(position)
            if key:
                return key
        return None

    def toggle_layer(self, layer_id):
        if layer_id in self.active_layers:
            self.active_layers.remove(layer_id)
        else:
            self.active_layers.append(layer_id)

    def activate_layer(self, layer_id):
        if layer_id not in self.active_layers:
            self.active_layers.append(layer_id)

    def deactivate_layer(self, layer_id):
        if layer_id in self.active_layers:
            self.active_layers.remove(layer_id)

    def scan(self):
        now = time.monotonic()
        currently_pressed = set(self.scanner.get_pressed())

        # Handle releases
        for position in list(self._pressed_keys):
            if position not in currently_pressed:
                key = self._pressed_keys.pop(position)
                key.release(self, now)

        # Handle new presses
        for position in currently_pressed:
            if position not in self._pressed_keys:
                key = self.get_active_key(position)
                if key:
                    self._pressed_keys[position] = key
                    key.press(self, now)

    # These are helpers expected by key classes
    def press(self, keycode):
        # You’d hook into adafruit_hid here
        print(f"PRESS: {keycode}")

    def release(self, keycode):
        # You’d hook into adafruit_hid here
        print(f"RELEASE: {keycode}")
