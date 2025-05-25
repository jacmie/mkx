from adafruit_hid.keyboard import Keyboard

from mkx.keys_abstract import KeysAbstract
from mkx.timed_keys import TimedKeys


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


class KeysLayer(KeysAbstract):
    def __init__(self, layer):
        super().__init__()
        self.key_name = "LAY"
        self.layer = layer

    def on_press(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        pass

    def on_release(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        pass


class DF(KeysLayer):
    """
    Default Layer - sets the default layer to the given active_layer and optionally jumps to it immediately.

    Example:
    active_layers = [0] # default
    MO(1)               # active_layers = [0, 1]
    MO(2)               # active_layers = [0, 1, 2]
    DF(3, jump=True)    # default layer set to 3 and (if jump=True) active_layers = [3]

    If jump=True (default behavior):
    layers = [3]        # default changed and active layers cleared to only new default

    If jump=False:
    active_layers = [3, 1, 2]   # default changed but active active_layers stack remains (3 inserted at bottom)
    """

    def __init__(self, layer, jump=True):
        super().__init__(layer)
        self.jump = jump
        self.key_name = f"DF({layer})"

    def on_press(self, layer_manager: LayersManager, _, __):
        layer_manager.set_default_layer(self.layer)
        if self.jump:
            layer_manager.set_active_layer(self.layer)


class RL(KeysLayer):
    """
    Replace Layer - replaces the top layer (active layer) with a given layer, without changing the default layer.

    Example:
    active_layers = [0] # default
    MO(1)               # active_layers = [0, 1]
    MO(2)               # active_layers = [0, 1, 2]
    RL(3)               # active_layers = [0, 1, 3]    # replaced layer 2 with 3
    """

    def __init__(self, layer):
        super().__init__(layer)
        self.key_name = f"RL({layer})"

    def on_press(self, layer_manager: LayersManager, _, __):
        layer_manager.set_active_layer(self.layer)


class MO(KeysLayer):
    """
    Momentary Layer - temporarily activates the specified layer while the key is held.
    Optionally holds a modifier key (e.g., Shift) during the layer activation.

    Example:
    active_layers = [0] # default
    MO(1)               # press -> active_layers = [0, 1], release -> active_layers = [0]
    MO(2, SHIFT)        # press -> active_layers = [0, 2], Shift held
                        # release -> active_layers = [0], Shift released
    """

    def __init__(self, layer, mod=None):
        super().__init__(layer)
        self.mod = mod
        self.key_name = f"MO({layer})"

    def on_press(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        layer_manager.activate_layer(self.layer, prioritize=True)
        if self.mod:
            keyboard.press(self.mod)

    def on_release(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        layer_manager.deactivate_layer(self.layer)
        if self.mod:
            keyboard.release(self.mod)


class TG(KeysLayer):
    """
    Toggle Layer - activates the layer if it's inactive, deactivates it if it's active.
    Useful for toggling layers like symbols, macros, or gaming layouts.

    Example:
    layers = [0]         # default layer
    TG(1) press          # layers = [0, 1]
    TG(1) press again    # layers = [0]       # layer 1 toggled off
    TG(2)                # layers = [0, 2]
    TG(3)                # layers = [0, 2, 3]
    TG(2)                # layers = [0, 3]     # layer 2 toggled off
    """

    def __init__(self, layer):
        super().__init__(layer)
        self.key_name = f"TG({layer})"

    def on_press(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        layer_manager.toggle_layer(self.layer)


class LayerSet(KeysAbstract):
    def __init__(self, layer):
        super().__init__()
        self.layer = layer

    def on_press(self, keyboard):
        keyboard.set_active_layer(self.layer)

    def on_release(self, keyboard):
        pass  # One-shot, no release handling


class LayerTapKey(KeysAbstract):
    def __init__(self, layer, tap_key):
        super().__init__()
        self.layer = layer
        self.tap_key = tap_key
        self._pressed_time = None
        self._threshold = 200  # ms to distinguish tap vs hold

    def on_press(self, keyboard, timestamp):
        self._pressed_time = timestamp
        self.tap_key._is_pressed = True  # Suppress auto .press()
        keyboard.activate_layer(self.layer)  # Preemptively activate

    def on_release(self, keyboard, timestamp):
        held_duration = timestamp - self._pressed_time
        if held_duration < self._threshold:
            self.tap_key.on_press(keyboard, timestamp)
            self.tap_key.on_release(keyboard, timestamp)
        keyboard.deactivate_layer(self.layer)


class LayerTapToggle(KeysAbstract):
    def __init__(self, layer):
        super().__init__()
        self.layer = layer
        self._press_time = None
        self._tap_count = 0
        self._threshold = 200  # ms
        self._toggle_window = 500  # ms to register rapid taps

    def on_press(self, keyboard, timestamp):
        self._press_time = timestamp
        keyboard.activate_layer(self.layer)

    def on_release(self, keyboard, timestamp):
        held = timestamp - self._press_time
        if held < self._threshold:
            self._tap_count += 1
            if self._tap_count >= 2:
                keyboard.toggle_layer(self.layer)
                self._tap_count = 0
        else:
            keyboard.deactivate_layer(self.layer)


class LayerTap(KeysAbstract, TimedKeys):
    def __init__(self, layer, tap_key, timeout=200):
        KeysAbstract.__init__(self)
        TimedKeys.__init__(self)
        self.layer = layer
        self.tap_key = tap_key
        self.timeout = timeout
        self._hold_activated = False

    def on_press(self, keyboard, timestamp):
        self._hold_activated = False
        self.tap_key.on_press(keyboard, timestamp)
        self.start_timer(timestamp)

    def on_release(self, keyboard, timestamp):
        if not self._hold_activated and (timestamp - self._pressed_time < self.timeout):
            self.tap_key.on_release(keyboard, timestamp)
        else:
            keyboard.layers.deactivate_layer(self.layer)
        self.stop_timer()

    def check_time(self, keyboard, timestamp):
        if not self._hold_activated and (
            timestamp - self._pressed_time >= self.timeout
        ):
            self.tap_key.on_release(keyboard, timestamp)  # cancel tap
            keyboard.layers.activate_layer(self.layer)
            self._hold_activated = True


# LT_NAV_ESC = LayerTap(layer=1, tap_key=KC.ESCAPE)
