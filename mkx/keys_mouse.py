import usb_hid

from adafruit_hid.mouse import Mouse

from mkx.keys_abstract import KeysAbstract


class KeysMouse(KeysAbstract):
    """
    A key that sends a Mouse action using Adafruit HID Mouse.
    """

    def __init__(self, key_name: str, mouse_action: str, *args):
        super().__init__()
        self.key_name = key_name
        self.mouse_action = mouse_action
        self.args = args
        self.mouse = Mouse(usb_hid.devices)

        self._x_move = 1
        self._y_move = 1
        self._scroll = 1

    def X(self, value):
        self._x_move = int(value)
        return self

    def Y(self, value):
        self._y_move = int(value)
        return self

    def S(self, value):
        self._scroll = int(value)
        return self

    def on_press(self, _, __, ___):
        if self.mouse_action == "click":
            self.mouse.click(*self.args)
        elif self.mouse_action == "press":
            self.mouse.press(*self.args)
        elif self.mouse_action == "release":
            self.mouse.release(*self.args)
        elif self.mouse_action == "move":
            x = self.args[0] * self._x_move if len(self.args) > 0 else 0
            y = self.args[1] * self._y_move if len(self.args) > 1 else 0
            scroll = self.args[2] * self._scroll if len(self.args) > 2 else 0
            self.mouse.move(x, y, scroll)

    def on_release(self, _, __, ___):
        if self.mouse_action == "press":
            self.mouse.release(*self.args)


# Mouse key definitions

LMB = KeysMouse("LMB", "click", Mouse.LEFT_BUTTON)
"""``LMB``"""
MB_LC = KeysMouse("MB_LC", "click", Mouse.LEFT_BUTTON)
"""``MB_LC``"""
MB_LEFT_CLICK = KeysMouse("MB_LEFT_CLICK", "click", Mouse.LEFT_BUTTON)
"""``MB_LEFT_CLICK``"""

# Mouse click actions
RMB = KeysMouse("RMB", "click", Mouse.RIGHT_BUTTON)
"""``RMB``"""
MB_RC = KeysMouse("MB_RC", "click", Mouse.RIGHT_BUTTON)
"""``MB_RC``"""
MB_RIGHT_CLICK = KeysMouse("MB_RIGHT_CLICK", "click", Mouse.RIGHT_BUTTON)
"""``MB_RIGHT_CLICK``"""

MMB = KeysMouse("MMB", "click", Mouse.MIDDLE_BUTTON)
"""``MMB``"""
MB_MC = KeysMouse("MB_MC", "click", Mouse.MIDDLE_BUTTON)
"""``MB_MC``"""
MB_MIDDLE_CLICK = KeysMouse("MB_MIDDLE_CLICK", "click", Mouse.MIDDLE_BUTTON)
"""``MB_MIDDLE_CLICK``"""

BMB = KeysMouse("BMB", "click", Mouse.BACK_BUTTON)
"""``BMB``"""
MB_BC = KeysMouse("MB_BC", "click", Mouse.BACK_BUTTON)
"""``MB_BC``"""
MB_BACK_CLICK = KeysMouse("MB_BACK_CLICK", "click", Mouse.BACK_BUTTON)
"""``MB_BACK_CLICK``"""

FMB = KeysMouse("FMB", "click", Mouse.FORWARD_BUTTON)
"""``FMB``"""
MB_FC = KeysMouse("MB_FC", "click", Mouse.FORWARD_BUTTON)
"""``MB_FC``"""
MB_FORWARD_CLICK = KeysMouse("MB_FORWARD_CLICK", "click", Mouse.FORWARD_BUTTON)
"""``MB_FORWARD_CLICK``"""

# Mouse press actions
MB_LP = KeysMouse("MB_LP", "press", Mouse.LEFT_BUTTON)
"""``MB_LP``"""
MB_LEFT_PRESS = KeysMouse("MB_LEFT_PRESS", "press", Mouse.LEFT_BUTTON)
"""``MB_LEFT_PRESS``"""

MB_RP = KeysMouse("MB_RP", "press", Mouse.RIGHT_BUTTON)
"""``MB_RP``"""
MB_RIGHT_PRESS = KeysMouse("MB_RIGHT_PRESS", "press", Mouse.RIGHT_BUTTON)
"""``MB_RIGHT_PRESS``"""

MB_MP = KeysMouse("MB_MP", "press", Mouse.MIDDLE_BUTTON)
"""``MB_MP``"""
MB_MIDDLE_PRESS = KeysMouse("MB_MIDDLE_PRESS", "press", Mouse.MIDDLE_BUTTON)
"""``MB_MIDDLE_PRESS``"""

MB_BP = KeysMouse("MB_BP", "press", Mouse.BACK_BUTTON)
"""``MB_BP``"""
MB_BACK_PRESS = KeysMouse("MB_BACK_PRESS", "press", Mouse.BACK_BUTTON)
"""``MB_BACK_PRESS``"""

MB_FP = KeysMouse("MB_FP", "press", Mouse.FORWARD_BUTTON)
"""``MB_FP``"""
MB_FORWARD_PRESS = KeysMouse("MB_FORWARD_PRESS", "press", Mouse.FORWARD_BUTTON)
"""``MB_FORWARD_PRESS``"""

# Mouse release actions
MB_LR = KeysMouse("MB_LR", "release", Mouse.LEFT_BUTTON)
"""``MB_LR``"""
MB_LEFT_RELEASE = KeysMouse("MB_LEFT_RELEASE", "release", Mouse.LEFT_BUTTON)
"""``MB_LEFT_RELEASE``"""

MB_RR = KeysMouse("MB_RR", "release", Mouse.RIGHT_BUTTON)
"""``MB_RR``"""
MB_RIGHT_RELEASE = KeysMouse("MB_RIGHT_RELEASE", "release", Mouse.RIGHT_BUTTON)
"""``MB_RIGHT_RELEASE``"""

MB_R = KeysMouse("MB_R", "release", Mouse.MIDDLE_BUTTON)
"""``MB_R``"""
MB_MIDDLE_RELEASE = KeysMouse("MB_MIDDLE_RELEASE", "release", Mouse.MIDDLE_BUTTON)
"""``MB_MIDDLE_RELEASE``"""

MB_BR = KeysMouse("MB_BR", "release", Mouse.BACK_BUTTON)
"""``MB_BR``"""
MB_BACK_RELEASE = KeysMouse("MB_BACK_RELEASE", "release", Mouse.BACK_BUTTON)
"""``MB_BACK_RELEASE``"""

MB_FR = KeysMouse("MB_FR", "release", Mouse.FORWARD_BUTTON)
"""``MB_FR``"""
MB_FORWARD_RELEASE = KeysMouse("MB_FORWARD_RELEASE", "release", Mouse.FORWARD_BUTTON)
"""``MB_FORWARD_RELEASE```"""

# Mouse move actions
MB_MR = KeysMouse("MB_MR", "move", 1, 0)
"""``MB_MR```"""
MB_MOVE_RIGHT = KeysMouse("MB_MOVE_RIGHT", "move", 1, 0)
"""``MB_MOVE_RIGHT```"""

MB_ML = KeysMouse("MB_ML", "move", -1, 0)
"""``MB_ML``"""
MB_MOVE_LEFT = KeysMouse("MB_MOVE_LEFT", "move", -1, 0)
"""``MB_MOVE_LEFT``"""

MB_MU = KeysMouse("MB_MU", "move", 0, 1)
"""``MB_MU``"""
MB_MOVE_UP = KeysMouse("MB_MOVE_UP", "move", 0, 1)
"""``MB_MOVE_UP``"""

MB_MD = KeysMouse("MB_MD", "move", 0, -1)
"""``MB_MD``"""
MB_MOVE_DOWN = KeysMouse("MB_MOVE_DOWN", "move", 0, -1)
"""``MB_MOVE_DOWN``"""

# Mouse scroll actions
MB_SU = KeysMouse("MB_SU", "move", 0, 0, 1)
"""``MB_SU``"""
MB_SCROLL_UP = KeysMouse("MB_SCROLL_UP", "move", 0, 0, 1)
"""``MB_SCROLL_UP``"""

MB_SD = KeysMouse("MB_SD", "move", 0, 0, -1)
"""``MB_SD``"""
MB_SCROLL_DOWN = KeysMouse("MB_SCROLL_DOWN", "move", 0, 0, -1)
"""``MB_SCROLL_DOWN```"""


# fmt: off
__all__ = [
    # Clicks
    "LMB", "MB_LC", "MB_LEFT_CLICK",
    "RMB", "MB_RC", "MB_RIGHT_CLICK",
    "MMB", "MB_MC", "MB_MIDDLE_CLICK",
    "BMB", "MB_BC", "MB_BACK_CLICK",
    "FMB", "MB_FC", "MB_FORWARD_CLICK",

    # Press
    "MB_LP", "MB_LEFT_PRESS",
    "MB_RP", "MB_RIGHT_PRESS",
    "MB_MP", "MB_MIDDLE_PRESS",
    "MB_BP", "MB_BACK_PRESS",
    "MB_FP", "MB_FORWARD_PRESS",

    # Release
    "MB_LR", "MB_LEFT_RELEASE",
    "MB_RR", "MB_RIGHT_RELEASE",
    "MB_R",  "MB_MIDDLE_RELEASE",
    "MB_BR", "MB_BACK_RELEASE",
    "MB_FR", "MB_FORWARD_RELEASE",

    # Move
    "MB_MR", "MB_MOVE_RIGHT",
    "MB_ML", "MB_MOVE_LEFT",
    "MB_MU", "MB_MOVE_UP",
    "MB_MD", "MB_MOVE_DOWN",

    # Scroll
    "MB_SU", "MB_SCROLL_UP",
    "MB_SD", "MB_SCROLL_DOWN",
]
# fmt: on
