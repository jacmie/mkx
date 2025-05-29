from adafruit_hid.keyboard import Keyboard

from mkx.keys_abstract import KeysAbstract
from mkx.manager_layers import LayersManager
from mkx.timed_keys import TimedKeys


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
        if len(layer_manager.active_layers) > 1:
            layer_manager.active_layers[-1] = self.layer  # Replace top layer
        else:  # If only one layer is active (default), just add RL layer
            layer_manager.activate_layer(self.layer)


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

    def __init__(self, layer, mod: KeysAbstract = None):
        super().__init__(layer)
        self.mod = mod
        self.key_name = f"MO({layer})"

    def on_press(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        layer_manager.activate_layer(self.layer, prioritize=True)
        if self.mod:
            self.mod.on_press(layer_manager, keyboard, timestamp)

    def on_release(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        layer_manager.deactivate_layer(self.layer)
        if self.mod:
            self.mod.on_release(layer_manager, keyboard, timestamp)


class LT(KeysLayer, TimedKeys):
    """
    Layer Tap - Momentarily activates a layer if held, sends a key if tapped.

    If the key is quickly tapped (within `timeout` ms), it behaves like `tap_key`.
    If held longer, it activates the `layer` as long as the key is held.

    Example:
        LT(1, KC.ESC)  # tap = Escape, hold = activate layer 1
    """

    def __init__(self, layer, tap_key: KeysAbstract, timeout=200):
        assert tap_key is not None, "tap_key must not be None"
        KeysLayer.__init__(self, layer)
        TimedKeys.__init__(self)
        self.tap_key = tap_key
        self.timeout = timeout
        self._hold = False
        self._pressed_time = None
        self.key_name = f"LT({layer}, {getattr(tap_key, 'key_name', 'UNKNOWN')})"

    def on_press(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        self._hold = False
        self._pressed_time = timestamp
        self.start_timer(timestamp)

    def on_release(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        if self._pressed_time is None:
            return

        duration = timestamp - self._pressed_time

        if self._hold:
            # Held long enough, deactivate layer
            layer_manager.deactivate_layer(self.layer)
        elif duration < self.timeout:
            # Tap: trigger tap key now
            self.tap_key.on_press(layer_manager, keyboard, timestamp)
            self.tap_key.on_release(layer_manager, keyboard, timestamp)
        else:
            # Fallback: activate/deactivate layer quickly (in case check_time didn’t fire)
            layer_manager.activate_layer(self.layer)
            layer_manager.deactivate_layer(self.layer)

        self.stop_timer()
        self._pressed_time = None

    def check_time(self, layers_manager: LayersManager, _, timestamp: int):
        print("_pressed_time", self._pressed_time)
        if self._pressed_time is None:
            return

        print(not self._hold, (timestamp - self._pressed_time >= self.timeout))
        if not self._hold and (timestamp - self._pressed_time >= self.timeout):
            layers_manager.activate_layer(self.layer)
            self._hold = True


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


class TO(KeysLayer):
    """
    To Layer (Toggle One-Shot Layer) - Sets the given layer as the sole active layer.
    Clears any other currently active layers.

    Example:
    layers = [0]
    TO(2) press   => layers = [2]
    TO(1) press   => layers = [1]
    """

    def __init__(self, layer):
        super().__init__(layer)
        self.key_name = f"TO({layer})"

    def on_press(
        self, layer_manager: LayersManager, keyboard: Keyboard, timestamp: int
    ):
        layer_manager.set_active_layer(self.layer)


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


class TT(KeysLayer, TimedKeys):
    """
    Tap-Toggle - Momentarily activates a layer if held, toggles layer if double-tapped.

    - Hold: activates layer while held (like MO)
    - Double-tap: toggles layer on/off
    - Single or >2 taps: no-op

    Example:
        TT(1)  # tap-tap toggles layer 1; hold = momentary
    """

    def __init__(self, layer, timeout=200):
        KeysLayer.__init__(self, layer)
        TimedKeys.__init__(self)
        self.timeout = timeout
        self._pressed_time = None
        self._hold = False
        self._tap_count = 0
        self._last_timestamp = 0
        self.key_name = f"TT({layer})"

    def on_press(self, layer_manager: LayersManager, _, timestamp: int):
        if (timestamp - self._last_timestamp) > self.timeout:
            self._tap_count = 0  # Reset tap count if delay too long

        self._tap_count += 1
        self._last_timestamp = timestamp
        self._pressed_time = timestamp
        self._hold = False
        self.start_timer(timestamp)

    def on_release(self, layer_manager: LayersManager, _, timestamp: int):
        if self._pressed_time is None:
            return

        if self._hold:
            layer_manager.deactivate_layer(self.layer)

        self.stop_timer()
        self._pressed_time = None

    def check_time(self, layer_manager: LayersManager, _, timestamp: int):
        print("_pressed_time", self._pressed_time)
        if self._pressed_time is None:
            return

        print(not self._hold, (timestamp - self._pressed_time >= self.timeout))
        if not self._hold and (timestamp - self._pressed_time >= self.timeout):
            print("elapsed")
            print("self._tap_count", self._tap_count)
            if self._tap_count >= 2:
                print("tap")
                # Toggle layer on double-tap
                layer_manager.toggle_layer(self.layer)
            elif self._tap_count == 1:
                # else:
                print("hold")
                # Hold behavior: activate layer only while held
                layer_manager.activate_layer(self.layer)
                self._hold = True
            # Reset after acting
            self._tap_count = 0
            self.stop_timer()


# class TT(KeysAbstract, TimedKeys):
#     """
#     Tap-Toggle Layer key.

#     - Hold: momentarily activate the layer
#     - Tap x2: toggle layer ON
#     - All other taps: do nothing
#     """

#     def __init__(self, layer: int, timeout=200):
#         KeysAbstract.__init__(self)
#         TimedKeys.__init__(self)
#         self.layer = layer
#         self._timeout = timeout
#         self.key_name = f"TT({layer})"
#         self._tap_count = 0
#         self._last_timestamp = 0
#         self._hold = False

#     def on_press(self, layer_manager: LayersManager, _, timestamp: int):
#         if (timestamp - self._last_timestamp) > self._timeout:
#             self._tap_count = 0  # Reset if timeout exceeded

#         self._tap_count += 1
#         self._last_timestamp = timestamp
#         self._hold = False
#         self.start_timer(timestamp)

#     def on_release(self, layer_manager: LayersManager, _, __):
#         if self._hold:
#             layer_manager.deactivate_layer(self.layer)
#         # self.stop_timer()

#     def check_time(self, layer_manager: LayersManager, _, timestamp: int):
#         if self._pressed_time is None:
#             return

#         if not self._hold:
#             if (timestamp - self._pressed_time) >= self._timeout:
#             #     if self._tap_count >= 2:
#             #         layer_manager.activate_layer(self.layer)
#             #     # Tap once or more than twice: no-op
#             #     self._tap_count = 0
#             #     self.stop_timer()
#             # else:
#                 # Treat as hold if still held past timeout
#                 # if self._tap_count == 1:
#                 layer_manager.activate_layer(self.layer)
#                 self._hold = True
