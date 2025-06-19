@page p_2 2 Get Started
@tableofcontents


``` {.py}
import board

from mkx.mkx_central import MKX_Central
from mkx.hid_usb import HID_USB

# from mkx.hid_ble import HID_BLE
from mkx.keys_standard import *
from mkx.keys_holdtap import HT
from mkx.keys_sticky import SK
from mkx.keys_tapdance import TD
from mkx.keys_layers import DF, MO, LT, TG, TO, TT

from mkx.periphery_central import PeripheryCentral
from mkx.interphace_central import InterphaceCentral
from mkx.interphace_uart import InterphaceUART
from mkx.switch_hid_mode import SwitchHIDmode

keyboard = MKX_Central()

col_pins = (board.GP9, board.GP7, board.GP5, board.GP4, board.GP3, board.GP2)
row_pins = (board.GP10, board.GP11, board.GP13, board.GP15, board.GP17)
central_peryphery = PeripheryCentral("central", col_pins, row_pins)
keyboard.central_periphery = central_peryphery

interphace_central = InterphaceCentral(central_peryphery, 0, 0, 5, 4)
keyboard.add_interface(interphace_central)

interphace_right = InterphaceUART("booster_r", None, board.GP1, 11, 0, 6, 4)
keyboard.add_interface(interphace_right)

LSFT_SPC = HT(SPC, LSFT)

# Normal sticky
SK_C = SK(LSFT)

# Defer release sticky (hold until all keys released)
SK_S = SK(N2, defer_release=True)

# Sticky that doesn’t cancel on repeat tap
SK_NO = SK(N3, retap_cancel=False)

TD_D = TD(D, DEL)


LT_NAV_ESC = DF(0)

# fmt: off
keymap = [
    [
        SK_C,  N1,      N2,      N3,      N4,      N5,      N6,      N7,      N8,       N9,      N0,      A,
        SK_S,  Q,       TD_D,    R,       W,       DF(1),   J,       F,       U,        P,       A,       A,
        SK_NO, A,       S,       H,       T,       MO(1, SHIFT),   Y,       N,       E,        O,       I,       A,
        LCTL,  Z,       X,       C,       TT(1),   TG(1),       K,       M,       A,        A,       A,       A,
        None,  None,    None,    None,    LSFT_SPC,LT(1, B),       ENTER,   A,       None,     None,    None,    None,
    ],
    [
        A,     N1,      N2,      N3,      N4,      N5,      N6,      N7,      N8,       N9,      N0,      A,
        A,     N1,      D,       R,       W,       DF(0),   J,       F,       U,        P,       A,       A,
        A,     N2,      S,       H,       TO(0),   G,       Y,       N,       E,        O,       I,       A,
        A,     N3,      X,       C,       V,       TG(1),   K,       M,       A,        A,       A,       A,
        None,  None,    None,    None,    SPACE ,  A,       ENTER,   A,       None,     None,    None,    None,
    ]
]
# fmt: on
keyboard.add_keymap(keymap, 12, 5)

usb = HID_USB()
# ble = HID_BLE()
hids = [usb]
keyboard.hids = hids

# hid_mode = SwitchHIDmode(usb_output=usb, ble_output=ble, switch_func="usb")
keyboard.hid_mode = "usb"

# keyboard.run_once()
keyboard.run_forever()
```
