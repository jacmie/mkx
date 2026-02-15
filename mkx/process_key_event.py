from mkx.keys_layers import KeysLayer, LT, TT
from mkx.timed_keys import TimedKeys
from mkx.keys_sticky import SK
from mkx.ansi_colors import Ansi, Ansi256


def _get_key(self, logical_index: int):
    active_layer = self.layers_manager.get_top_layer()

    try:
        key = self.keymap[active_layer][logical_index]
    except IndexError:
        print(
            f"{Ansi.RED}Key index {logical_index} out of bounds for layer {active_layer}{Ansi.RESET}"
        )
        return None

    return key


def process_key_event(
    self, device_id: str, logical_index: int, pressed: bool, timestamp: int
):
    """
    Core key event handling logic.
    Maps a logical key index to a key object and dispatches press/release behavior.
    """

    # Uniquely identify a pressed key across devices and positions
    key_pos = (device_id, logical_index)

    if pressed:
        # Resolve key from the currently active layer
        key = _get_key(self, logical_index)
        if key is None:
            return

        print(f"{Ansi.YELLOW}{Ansi.BOLD}key: {key.key_name} pressed{Ansi.RESET}")

        # Track pressed keys to ensure correct release handling
        # (prevents stuck keys when layers change while a key is held)
        self.pressed_keys[key_pos] = key

        # Layer keys may modify the active layer on press
        if isinstance(key, KeysLayer):
            key.on_press(self.layers_manager, self.keyboard, timestamp)
            # Non-tap layer keys do not generate a normal key press
            if not isinstance(key, LT) and not isinstance(key, TT):
                return

        # Dispatch press event for all regular and tap-enabled keys
        key.on_press(self.layers_manager, self.keyboard, timestamp)

        # Register time-dependent keys after activation
        if isinstance(key, TimedKeys):
            self.timed_keys_manager.register(key)

        # Register sticky keys for deferred release handling
        if isinstance(key, SK):
            self.sticky_key_manager.register(key)

    else:
        # Resolve the key being released:
        # prefer tracked key (layer-safe), fall back to current layer lookup
        key = self.pressed_keys.pop(key_pos, None)

        if key is None:
            key = _get_key(self, logical_index)
            if key is None:
                return

        print(f"{Ansi.YELLOW}{Ansi.BOLD}key: {key.key_name} released{Ansi.RESET}")

        # Dispatch release event
        key.on_release(self.layers_manager, self.keyboard, timestamp)

        # Clear active sticky keys unless the released key itself is sticky
        if not isinstance(key, SK):
            self.sticky_key_manager.clear_stickies(self.keyboard, timestamp)

    print()
