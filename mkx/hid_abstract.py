class HID_abstract:
    def send_key(self, keycode: int, pressed: bool):
        """
        Send a key event to the output device.
        pressed: True = keydown, False = keyup
        """
        raise NotImplementedError(
            "Subclass of the HID_abstract must implement send_key()"
        )
