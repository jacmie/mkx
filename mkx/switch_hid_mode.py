class SwitchHIDmode:
    def __init__(self, usb_output, ble_output, switch_func):
        self.usb_output = usb_output
        self.ble_output = ble_output
        self.switch_func = switch_func  # Function returning "usb" or "ble"

    @property
    def active_output(self):
        mode = self.switch_func()
        if mode == "usb":
            return self.usb_output
        elif mode == "ble":
            return self.ble_output
        else:
            raise RuntimeError("Unknown output mode: " + str(mode))

    def send_key(self, key):
        self.active_output.send_key(key)

    def release_key(self, key):
        self.active_output.release_key(key)

    # Add other HID-related methods as needed


# import digitalio
# import board

# mode_pin = digitalio.DigitalInOut(board.D2)
# mode_pin.switch_to_input(pull=digitalio.Pull.UP)

# def get_mode():
#     return "usb" if not mode_pin.value else "ble"
