from mkx.keys_layers import KeysLayer, LT, TT
from mkx.timed_keys import TimedKeys
from mkx.keys_sticky import SK


def process_key_event(
    self, device_id: str, logical_index: int, pressed: bool, timestamp: int
):
    """
    Pure key handling logic.
    """

    key_pos = (device_id, logical_index)

    if pressed:
        active_layer = self.layers_manager.get_top_layer()

        try:
            key = self.keymap[active_layer][logical_index]
        except IndexError:
            print(f"Key index {logical_index} out of bounds for layer {active_layer}")
            return

        if key is None:
            return

        # Store keys for tracking release and avoid keys lock: key press -> layer changed -> key release
        self.pressed_keys[key_pos] = key

        if isinstance(key, KeysLayer):
            key.on_press(self.layers_manager, self.keyboard, timestamp)
            if not isinstance(key, LT) and not isinstance(key, TT):
                return

        # Call on_press for all types of keys (except KeysLayer, which you already handled above)
        key.on_press(self.layers_manager, self.keyboard, timestamp)

        # If the key is time-based, register it *after* on_press so it's active
        if isinstance(key, TimedKeys):
            self.timed_keys_manager.register(key)

        print("key:", key.key_name, "pressed")

        if isinstance(key, SK):
            self.sticky_key_manager.register(key)

    else:
        # Retrieve previously stored KeysLayer key (if any)
        key = self.pressed_keys.pop(key_pos, None)

        if key is None:
            # Fallback: look up from top layer if not tracked
            active_layer = self.layers_manager.get_top_layer()
            try:
                key = self.keymap[active_layer][logical_index]
            except IndexError:
                print(
                    f"Key index {logical_index} out of bounds for layer {active_layer}"
                )
                return

            if key is None:
                return

        if isinstance(key, KeysLayer):
            key.on_release(self.layers_manager, self.keyboard, timestamp)
            return

        print("key:", key.key_name, "released")

        key.on_release(self.layers_manager, self.keyboard, timestamp)

        if not isinstance(key, SK):
            self.sticky_key_manager.clear_stickies(self.keyboard, timestamp)
