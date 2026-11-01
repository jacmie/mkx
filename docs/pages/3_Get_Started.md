@page p_3 3 Get Started
@tableofcontents

@section p_3_1  3.1 Basic Usage

@subsection p_3_1_1 3.1.1 Files Structure

- *lib/* - contains Adafruit bundle libraries & MKX library  
- *boot.py* - runs **first on boot** - sets up the environment  
- *boot_out.txt* - boot log (useful for debugging when USB monitor is unavailable)  
- *code.py* - main script runs on soft reboot (after saving files)  

@subsection p_3_1_2 3.1.2 Programming

By default **CIRCUITPY** drive appears.  
Edit files directly on the MCU and save. With auto reload enabled (default) there will be soft restart and the saved code reloded.

The **MKX library** provides **extensive logging**
- Useful for debugging keymaps and device behavior
- Helps identify issues quickly

To view logs in real time, use a **serial monitor**
- Recommended editors & tools:  
  https://learn.adafruit.com/welcome-to-circuitpython/recommended-editors  

- Popular options:
  - **Mu Editor** - built-in serial console (easy for beginners)
  - **Thonny** - simple interface with serial output
  - **VS Code** - use extensions like *Serial Monitor*
  - **screen / minicom (Linux/macOS)** - in terminal

In the following sections few use examples of the **MKX** library are presented.

@section p_3_2  3.2 Hardware Keypass

<div style="margin-left: 100px;">
  <img width=800 src="KeyPass_keyboard.jpg">
</div>

This simple setup uses an unmodified *Seeed Xiao nRF52840* connected to a computer via USB.
<br>

To make it more useful and entertaining, we simulate the behavior of a hardware security key.  
⚠️ **Warning:** *This is not intended for real security purposes. Actual hardware keys use encryption and have more advanced mechanisms.*
<br>

By bridging pin D5 (sending pin) and pin D6 (receiving pin) with pliers or any other conductive object like a wire, paper clip, etc. predefined key string is sent to the computer.

This setup uses only one hardware component, which both senses the signal and processes it locally, with no separate central/periphery split.  
For this reason **MKX_Single** is used: **PeripherySingle** is defined and added to the keyboard object, and **InterfaceSingle** is added as its matching interface.

Standard keyboard keys were used, modifier key **M_LSFT** was applied to produce capital letters and special characters.  
All input is grouped under a single key called **HK**, defined as a sequence **SEQ** key.  
The keymap is simple and consists of only one key: **HK**.

The nRF52840 supports Bluetooth Low Energy (BLE).  
To connect the keyboard via Bluetooth, uncomment the line **keyboard.use_ble(True)**.  

In some cases, the BLE connection can be unreliable and keystrokes may not be transmitted correctly.  
If this happens, try turning Bluetooth off and on again and then reconnecting the device—for example, by re-pairing it on your phone.  

``` {.py}
# code.py

import board

from mkx.mkx_single import MKX_Single

from mkx.keys_standard import *
from mkx.keys_modifiers import M_LSFT
from mkx.keys_sequence import SEQ

from mkx.periphery_single import PeripherySingle
from mkx.interface_single import InterfaceSingle

keyboard = MKX_Single()

col_pins = (board.D5,)
row_pins = (board.D6,)
keyboard.add_periphery_single(PeripherySingle(col_pins, row_pins))
keyboard.add_interface(InterfaceSingle(0, 0, 0, 0))

# fmt: off

HK = SEQ([M_LSFT(H), E, L, L, O, SPACE,
          M_LSFT(W), O, R, L, D, SPACE,
          M_LSFT(M), M_LSFT(K), M_LSFT(X), M_LSFT(N1), ENTER])

keymap = [
    [
        HK,
    ],
]

# fmt: on

keyboard.add_keymap(keymap, 1, 1)
# Uncomment to connect via BLE
# keyboard.use_ble(True)
keyboard.run_forever()
```

@section p_3_3  3.3 Booster Keyboard

<div style="margin-left: 100px;">
  <img width=800 src="BOOSTER_keyboard.jpg">
</div>

Here is a more practical example using a split keyboard called **Booster**.

Both halves of the keyboard use the *Pimoroni PGA2040* board, chosen for its small footprint, numerous available GPIO pins, and minimal onboard extras.

In the image, you can see:
- hot swap choc keys sockets
- development wiring on the right half, connecting it to USB for programming.
- loop between the sending and receiving pins used for debugging the UART connection.
- USB magnetic connector soldered to the left half, intended for regular usage.
- status RGB LED glowing green, indicating the currently active layer.

The keyboard runs slightly modified [Workman layout](https://workmanlayout.org/) and supports various types of keys, including **media keys**.

In terms of architecture:
- The left half functions as the **PeripheryCentral**
- The right half functions as the **PeripheryUART**

These peripheries are designed solely to send signals to the central processor using a defined protocol.

The left half also contains the **Interfaces** for both sides, managing communication between the **central** unit and each **periphery**.

The **status LED** indicates the active layer:
- Green for Layer 1
- Blue for Layer 2

Additionally, a few shortcut keys are defined, which are referenced later in the keymap.

**Left Keyboard Part (Central)**
``` {.py}
# code.py

import board

from mkx.mkx_central import MKX_Central

from mkx.periphery_central import PeripheryCentral
from mkx.interface_central import InterfaceCentral
from mkx.interface_uart import InterfaceUART
from mkx.layer_status_led_rgb_neopixel import LayerStatusLedRgbNeoPixel

from mkx.keys_standard import *
from mkx.keys_modifiers import M_LGUI
from mkx.keys_holdtap import HT
from mkx.keys_layers import MO, TO
from mkx.keys_media import VOLU, VOLD

keyboard = MKX_Central()

col_pins = (board.GP9, board.GP7, board.GP5, board.GP4, board.GP3, board.GP2)
row_pins = (board.GP10, board.GP11, board.GP13, board.GP15, board.GP17)

central_peryphery = PeripheryCentral("booster_l", col_pins, row_pins)
keyboard.add_periphery_central(central_peryphery)

interface_central = InterfaceCentral(central_peryphery, 0, 0, 5, 4)
keyboard.add_interface(interface_central)

interface_right = InterfaceUART("booster_r", None, board.GP1, 11, 0, 6, 4)
keyboard.add_interface(interface_right)

status_led = LayerStatusLedRgbNeoPixel(board.GP23, brightness=0.015)
status_led.add_layer(0, (0, 255, 0))  # Green
status_led.add_layer(1, (0, 0, 255))  # Blue
keyboard.add_layer_status_led(status_led)

# Shortcuts
DESKTOP = M_LGUI(D)
LOCK = M_LGUI(L)

# Hold Tap
LAY1 = HT(TO(1), MO(1))
LAY0 = HT(TO(0), MO(0))

LCTL_TAB = HT(TAB, LCTRL)
LSFT_SPC = HT(SPC, LSFT)
RALT_BSPC = HT(BSPC, RALT)
LALT_BSPC = HT(BSPC, LALT)

# fmt: off

keymap = [
    [
        GRV,        N1,         N2,         N3,         N4,         N5,         N6,         N7,         N8,         N9,         N0,         BSLS,
        EQL,        Q,          D,          R,          W,          L,          J,          F,          U,          P,          SCLN,       LBRC,
        MINS,       A,          S,          H,          T,          G,          Y,          N,          E,          O,          I,          QUOT,
        LCTL_TAB,   Z,          X,          C,          V,          B,          K,          M,          COMM,       DOT,        SLSH,       RBRC,
        None,       None,       None,       None,       LSFT_SPC,   ENTER,      LAY1,       RALT_BSPC,  None,       None,       None,       None,
    ],
    [
        ESC,        F1,         F2,         F3,         F4,         F5,         F6,         F7,         F8,         F9,         F10,        F11,
        None,       None,       DESKTOP,    PAGE_UP,    None,       LOCK,       None,       BSPC,       UP,         DEL,        None,       F12,
        None,       None,       HOME,       PAGE_DOWN,  END,        None,       None,       LEFT,       DOWN,       RIGHT,      None,       None,
        LCTL_TAB,   Z,          X,          C,          V,          None,       None,       VOLD,       None,       VOLU,       None,       None,
        None,       None,       None,       None,       LSFT_SPC,   ENTER,      LAY0,       LALT_BSPC,  None,       None,       None,       None,
    ]
]

# fmt: on

keyboard.add_keymap(keymap, 12, 5)
keyboard.run_forever()
```

**Right Keyboard Part**

``` {.py}
# code.py

import board

from mkx.mkx_periphery import MKX_Periphery
from mkx.periphery_uart import PeripheryUART


col_pins = (board.GP9, board.GP7, board.GP5, board.GP4, board.GP3, board.GP2)
row_pins = (board.GP10, board.GP11, board.GP13, board.GP15, board.GP17)

peryphery = PeripheryUART("booster_r", col_pins, row_pins, board.GP0, board.GP1)

keyboard = MKX_Periphery(peryphery, debug=True)
keyboard.run_forever()
```

@section p_3_4  3.4 Square Keyboard

<div style="margin-left: 100px;">
  <img src="SQ_keyboard.jpg">
</div>

Another split keyboard example, called **Sq (Square)**, is equipped with *Feather ESP32-S3* boards on both halves.  
This board provides several advantages, including potential Bluetooth connectivity, battery support, and onboard charging capabilities.

Since many parts of the code are shared with the Booster keyboard, this overview will focus only on the key differences.

The left half, which connects to the computer, includes a new file: **boot.py**.  
This script runs immediately when the board powers on, allowing configuration of USB device properties.

This includes:
- defining the keyboard's USB type and name
- disabling auto-reload on file save or system glitches, improving stability during everyday use
- preventing the board from appearing as a mass storage device, which is important for cybersecurity policies in some workplaces

To re-enable the storage device mode, a specific key (wired to source and sense pins) must be held down while powering on the board.  
⚠️ **Warning:** *Always back up your code before disabling the storage feature. Incorrect pin configuration or other errors can make the board unresponsive.  
In such cases, a hard reset may be required, which erases all data and necessitates re-uploading your code.*

Additional Features:
- **RGB backlighting**: the keyboard has a slowly glowing rainbow effect across its keys
- **VIM emulation**: the keyboard can simulate VIM editor behavior using a custom **keys_vim** configuration

Each keyboard layer corresponds to a different **VIM mode**, indicated by the **status LED**.  
Even if you're not a VIM fan, you may find some picked *vim_keys* useful in your own keymap.  
Theoretically, this behavior can work even in text input fields of a browser 😉

**Left Keyboard Part (Central)**

``` {.py}
# boot.py

import board

from mkx.boot_config import boot_cfg

boot_cfg(
    sense=board.D13,  # column
    source=board.D5,  # row
    autoreload=False,
    storage=False,
    usb_id=("MKX Device", "Sq Keyboard"),
)
```
  
``` {.py}
# code.py

import board

from mkx.mkx_central import MKX_Central
from mkx.layer_status_led_rgb_neopixel import LayerStatusLedRgbNeoPixel
from mkx.backlight_neopixel_rainbow import BacklightNeopixelRainbow

from mkx.keys_standard import *
from mkx.keys_modifiers import M_LCTL, M_LSFT, M_LGUI
from mkx.keys_media import VOLU, VOLD
from mkx.keys_holdtap import HT
from mkx.keys_layers import TO
from mkx.keys_vim import *

from mkx.periphery_central import PeripheryCentral
from mkx.interface_central import InterfaceCentral
from mkx.interface_uart import InterfaceUART

keyboard = MKX_Central()

col_pins = (board.D13, board.D12, board.D11, board.A1, board.A4, board.A3)
row_pins = (board.A2, board.MISO, board.D10, board.D9, board.D6, board.D5)
central_peryphery = PeripheryCentral("sq_l", col_pins, row_pins)
keyboard.add_periphery_central(central_peryphery)

interface_central = InterfaceCentral(central_peryphery, 0, 0, 5, 5)
keyboard.add_interface(interface_central)

interface_right = InterfaceUART("sq_r", board.TX, board.RX, 6, 0, 11, 5)
keyboard.add_interface(interface_right)

status_led = LayerStatusLedRgbNeoPixel(board.SCK)
status_led.add_layer(0, (0, 0, 255))  # Blue
status_led.add_layer(1, (0, 255, 0))  # Green
status_led.add_layer(2, (255, 255, 255))  # White
status_led.add_layer(3, (255, 0, 0))  # Red
keyboard.add_layer_status_led(status_led)

backlight = BacklightNeopixelRainbow(board.A0, num_pixels=72, brightness=0.4)
backlight.slower(2)
backlight.set_swirl(True)
keyboard.add_backlight(backlight)

OPEN = M_LCTL(O)
CLOSE = M_LCTL(W)
SAVE = M_LCTL(S)
TABS = M_LCTL(J)
TOOLS = M_LCTL(B)
DESKTOP = M_LGUI(D)
LOCK = M_LGUI(L)
PTAB = M_LCTL(PGUP)
NTAB = M_LCTL(PGDN)
COMMENT = M_LCTL(SLSH)

RALT_DEL = HT(DEL, RALT)
LALT_DEL = HT(DEL, LALT)
LSFT_SPC = HT(SPC, LSFT)

# fmt: off
keymap = [
    # Normal
    [
        ESC,        F1,             F2,             F3,         F4,             F5,         F6,         F7,         F8,         F9,             F10,        F11,
        GRV,        N1,             N2,             N3,         N4,             N5,         N6,         N7,         N8,         N9,             N0,         F12,
        VI_MVLU,    None,           VI_DEL,         VI_REPL.L(3), SAVE,         LOCK,       TABS,       VI_FIND,    VI_UNDO,    VI_PAST,        None,       VOLU,
        VI_MVLD,    VI_APND.L(1),   VI_SUBS.L(1),   HOME,       TOOLS,          DESKTOP,    VI_YANK,    VI_NXTW,    END,        OPEN,           VI_INS.L(1),VOLD,
        TAB,        None,           VI_CUT,         CLOSE,      TO(2),          VI_PRVW,    None,       None,       PTAB,       NTAB,           COMMENT,    None,
        LCTRL,      LCTRL,          ENT,            ENT,        LSFT_SPC,       LSFT_SPC,   BSPC,       LALT_DEL,   LEFT,       UP,             DOWN,       RIGHT,
    ],
    
    # Edit 
    [
        TO(0),      F1,             F2,             F3,         F4,             F5,         F6,         F7,         F8,         F9,             F10,        F11,
        GRV,        N1,             N2,             N3,         N4,             N5,         N6,         N7,         N8,         N9,             N0,         BSLS,
        EQL,        Q,              D,              R,          W,              L,          J,          F,          U,          P,              SCLN,       LBRC,
        MINS,       A,              S,              H,          T,              G,          Y,          N,          E,          O,              I,          QUOT,
        TAB,        Z,              X,              C,          V,              B,          K,          M,          COMM,       DOT,            SLSH,       RBRC,
        LCTRL,      LCTRL,          ENT,            ENT,        LSFT_SPC,       LSFT_SPC,   BSPC,       RALT_DEL,   LEFT,       UP,             DOWN,       RIGHT,
    ],

    # Visual
    [
        TO(0),              F1,             F2,             F3,             F4,         F5,             F6,         F7,             F8,             F9,         F10,            F11,
        GRV,                N1,             N2,             N3,             N4,         N5,             N6,         N7,             N8,             N9,         N0,             F12,
        M_LSFT(VI_NXTL),    None,           VI_DEL,         VI_REPL.L(3),   SAVE,       LOCK,           TABS,       VI_FIND,        VI_UNDO,        VI_PAST,    None,           None,
        M_LSFT(VI_PRVL),    VI_APND.L(1),   VI_SUBS.L(1),   M_LSFT(HOME),   TOOLS,      DESKTOP,        VI_YANK,    M_LSFT(VI_NXTW),M_LSFT(END),    OPEN,       VI_INS.L(1),    None,
        TAB,                None,           VI_CUT,         CLOSE,          None,       M_LSFT(VI_PRVW),None,       None,           PTAB,           NTAB,       COMMENT,        None,
        LCTRL,              LCTRL,          ENT,            ENT,            LSFT_SPC,   LSFT_SPC,       BSPC,       LALT_DEL,       M_LSFT(LEFT),   M_LSFT(UP), M_LSFT(DOWN),   M_LSFT(RIGHT),
    ],

    # Replace 
    [
        VI_R_ESC.L(0), F1,          F2,             F3,         F4,             F5,         F6,         F7,         F8,         F9,             F10,        F11,
        GRV,        N1,             N2,             N3,         N4,             N5,         N6,         N7,         N8,         N9,             N0,         BSLS,
        EQL,        Q,              D,              R,          W,              L,          J,          F,          U,          P,              SCLN,       LBRC,
        MINS,       A,              S,              H,          T,              G,          Y,          N,          E,          O,              I,          QUOT,
        TAB,        Z,              X,              C,          V,              B,          K,          M,          COMM,       DOT,            SLSH,       RBRC,
        LCTRL,      LCTRL,          ENT,            ENT,        LSFT_SPC,       LSFT_SPC,   BSPC,       RALT_DEL,   LEFT,       UP,             DOWN,       RIGHT,
    ],
]

# fmt: on

keyboard.add_keymap(keymap, 12, 6)
keyboard.run_forever()
```

**Right Keyboard Part**
``` {.py}
# code.py

import board

from mkx.mkx_periphery import MKX_Periphery
from mkx.periphery_uart import PeripheryUART

col_pins = (board.D13, board.D12, board.D11, board.A1, board.A4, board.A3)
row_pins = (board.A2, board.MISO, board.D10, board.D9, board.D6, board.D5)

peryphery = PeripheryUART("sq_r", col_pins, row_pins, board.TX, board.RX)

keyboard = MKX_Periphery(peryphery, debug=True)
keyboard.run_forever()
```

@section p_3_5  3.5 Myk Keyboard

<div style="margin-left: 100px;">
  <img src="MykF_keyboard.jpg">
</div>
  
<div style="margin-left: 100px;">
  <img src="MykR_keyboard.jpg">
</div>

This "split" keyboard uses one MCU and two *MCP23017* pin expanders.  
It was initially driven by a *Seeed Xiao nRF52840* to test Bluetooth functionality, but the BLE stack took up too much memory, preventing the full keyboard firmware from fitting.  
This resource constraint caused severe input latency and an lack of Bluetooth connection, so the MCU was changed to a *Seeed Xiao RP2350*.  
While it lacks Bluetooth capabilities, it offers significantly faster processing speeds and a much larger memory capacity.  

In this architecture, the MCU communicates with the two pin expanders over I2C, each using a unique address.  
While this approach dramatically increases the available pin count, it introduces complications in the keymap layout.  
Moreover, the expanders work only with *digitalio.Pull.UP*, which inverts the key-mapping logic.

Driving the *MCP23017* expanders requires the **adafruit_mcp230xx** library, which is not part of the base Adafruit bundle installed in @ref p_2_3.  
Install it additionally with **circup**:
```
circup install adafruit_mcp230xx
```

To prevent key conflicts, the matrix had to be remapped using custom code into a larger, virtual matrix.  
In this layout, the columns and rows are transposed: the top-left quadrant handles the left half of the keyboard,  
while the bottom-right quadrant handles the right half.  
The remaining two quadrants are populated with null values to avoid overlapping inputs.  
*See the remapper.py*.  

However, even with the faster RP2350 MCU, there was still a noticeable input lag.  
The standard I2C frequency wasn't fast enough, so it had to be increased to fast mode with 400kHz, which resolved the lag.

Unlike the Square keyboard (see @ref p_3_4), where `sense`/`source` are wired to a dedicated matrix key, that approach doesn't work here.  
The *MCP23017* expanders are only initialized later in **code.py**, so none of them are available yet while **boot.py** runs, which rules out using any matrix key (they all live behind the expanders) as the `sense`/`source` pair.  
Instead, `sense` and `source` are wired directly to raw MCU pins (**D9** and **D8**), so entering storage/programming mode requires physically bridging these two pads on the board rather than holding down a key,  
or adding separate key (not present on this keyboard).

Another challenge arose when connecting the keyboard halves to the main MCU board using JST-SH 1.0mm connectors.  
These connectors proved to be highly unreliable.  
After extensive hardware debugging, I had to bypass them by soldering custom wire bridges directly to the specific pads visible in the photo.

The yellow casing also tints the status LED, altering its perceived color.  

While this keyboard design introduced quite a few challenges, it finally works and served as an invaluable learning experience.  
Some variations of this concept may still prove useful to you.

``` {.py}
# boot.py

import board

from mkx.boot_config import boot_cfg

boot_cfg(
    sense=board.D9,  # column
    source=board.D8,  # row
    autoreload=False,
    storage=False,
    usb_id=("MKX Device", "Myk Keyboard"),
)
```
  
``` {.py}
# remapper.py

def remapper(keymap):
    """
    Transforms a list of layers from a 6x12 layout into a 12x12 layout
    where each hand occupies a non-overlapping diagonal 6x6 block.
    This decouples the row selections of mcp1 (Rows 0-5) and mcp2 (Rows 6-11) to avoid physical pin sharing.

              Columns 0-5 (mcp1)     Columns 6-11 (mcp2)
            +---------------------+---------------------+
    Rows    |                     |                     |
    0-5     |   LEFT SIDE (6x6)   |     NULL (None)     |
    (mcp1)  |     Transposed      |                     |
            +---------------------+---------------------+
    Rows    |                     |                     |
    6-11    |     NULL (None)     |  RIGHT SIDE (6x6)   |
    (mcp2)  |                     |     Transposed      |
            +---------------------+---------------------+
    """
    remapped_keymap = []

    for layer in keymap:
        # 1. Break the flat layer into a standard 6 rows x 12 columns layout
        grid_12x6 = [layer[i : i + 12] for i in range(0, len(layer), 12)]
        
        # 2. Extract the left and right 6x6 blocks
        left_6x6 = [row[0:6] for row in grid_12x6]
        right_6x6 = [row[6:12] for row in grid_12x6]
        
        # 3. Transpose both 6x6 matrices independently (swap rows and columns)
        left_transposed = [
            [left_6x6[r][c] for r in range(6)] for c in range(6)
        ]
        right_transposed = [
            [right_6x6[r][c] for r in range(6)] for c in range(6)
        ]
        
        # 4. Construct a 12x12 grid with active maps on the diagonal quarters
        grid_12x12 = []
        
        # Top 6 Rows: mcp1 active on Left (Cols 0-5), Right (Cols 6-11) is None
        for r in range(6):
            row_left_half = left_transposed[r]
            row_right_half = [None] * 6
            grid_12x12.extend(row_left_half + row_right_half)
            
        # Bottom 6 Rows: Left (Cols 0-5) is None, mcp2 active on Right (Cols 6-11)
        for r in range(6):
            row_left_half = [None] * 6
            row_right_half = right_transposed[r]
            grid_12x12.extend(row_left_half + row_right_half)
            
        remapped_keymap.append(grid_12x12)

    return remapped_keymap
```
  
``` {.py}
# code.py

import board
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017

from mkx.mkx_single import MKX_Single
from mkx.periphery_single import PeripherySingle
from mkx.interface_single import InterfaceSingle
from mkx.diode_orientation import DiodeOrientation

from mkx.layer_status_led_rgb_neopixel import LayerStatusLedRgbNeoPixel

from mkx.keys_standard import *
from mkx.keys_media import VOLU, VOLD
from mkx.keys_modifiers import M_LCTL, M_LSFT, M_LGUI
from mkx.keys_sequence import SEQ
from mkx.keys_holdtap import HT
from mkx.keys_layers import TO
from mkx.keys_vim import *

from mkx.i2c import init_i2c

keyboard = MKX_Single()

status_led = LayerStatusLedRgbNeoPixel(board.RX)
status_led.add_layer(0, (255, 0, 0))  # Red
status_led.add_layer(1, (0, 255, 0))  # Green
status_led.add_layer(2, (0, 0, 255))  # Blue
keyboard.add_layer_status_led(status_led)

keyboard.use_interrupt(board.D0)

i2c = init_i2c(board.SCL, board.SDA, frequency=400000, status_led=status_led)

mcp1 = MCP23017(i2c, address=0x20)
mcp2 = MCP23017(i2c, address=0x21)

# Configures the IOCON register on both chips to enable open-drain (bit ODR = 0x04)
# This prevents a hardware short-circuit across your shared INT line
for mcp in (mcp1, mcp2):
    current_iocon = mcp.io_control
    mcp.io_control = current_iocon | 0x04

col_pins = (
    # Left Side (mcp1) - Columns 0 to 5
    mcp1.get_pin(13),  # COL0 -> GPB5
    mcp1.get_pin(12),  # COL1 -> GPB4
    mcp1.get_pin(11),  # COL2 -> GPB3
    mcp1.get_pin(10),  # COL3 -> GPB2
    mcp1.get_pin(9),  # COL4 -> GPB1
    mcp1.get_pin(8),  # COL5 -> GPB0
    # Right Side (mcp2) - Columns 6 to 11
    mcp2.get_pin(13),  # COL6 -> GPB5
    mcp2.get_pin(12),  # COL7 -> GPB4
    mcp2.get_pin(11),  # COL8 -> GPB3
    mcp2.get_pin(10),  # COL9 -> GPB2
    mcp2.get_pin(9),  # COL10 -> GPB1
    mcp2.get_pin(8),  # COL11 -> GPB0
)

row_pins = (
    # Left Side Rows (mcp1) - Rows 0 to 5
    mcp1.get_pin(2),  # ROW0 -> GPA2
    mcp1.get_pin(3),  # ROW1 -> GPA3
    mcp1.get_pin(4),  # ROW2 -> GPA4
    mcp1.get_pin(5),  # ROW3 -> GPA5
    mcp1.get_pin(6),  # ROW4 -> GPA6
    mcp1.get_pin(7),  # ROW5 -> GPA7
    # Right Side Rows (mcp2) - Rows 6 to 11
    mcp2.get_pin(2),  # ROW6 -> GPA2
    mcp2.get_pin(3),  # ROW7 -> GPA3
    mcp2.get_pin(4),  # ROW8 -> GPA4
    mcp2.get_pin(5),  # ROW9 -> GPA5
    mcp2.get_pin(6),  # ROW10 -> GPA6
    mcp2.get_pin(7),  # ROW11 -> GPA7
)

periphery = PeripherySingle(
    col_pins,
    row_pins,
    pull=digitalio.Pull.UP,
    diode_orientation=DiodeOrientation.COL2ROW,
)
keyboard.add_periphery_single(periphery)

interface = InterfaceSingle(0, 0, 11, 11)
keyboard.add_interface(interface)


OPEN = M_LCTL(O)
CLOSE = M_LCTL(W)
SAVE = M_LCTL(S)
TABS = M_LCTL(J)
TOOLS = M_LCTL(B)
DESKTOP = M_LGUI(D)
LOCK = M_LGUI(L)
PTAB = M_LCTL(PGUP)
NTAB = M_LCTL(PGDN)
COMMENT = M_LCTL(SLSH)
ALL = M_LCTL(A)
REPLACE = M_LCTL(H)

RALT_DEL = HT(DEL, RALT)
LALT_DEL = HT(DEL, LALT)
LSFT_SPC = HT(SPC, LSFT)

# fmt: off

keymap = [
    # Normal
    [
        ESC,        F1,             F2,             F3,         F4,             F5,         F6,         F7,         F8,         F9,             F10,        F11,
        COMMENT,    ALL,            PTAB,           NTAB,       SAVE,           CLOSE,      None,       None,       None,       None,           None,       F12,
        VI_MVLU,    HOME,           BSPC,           UP,         DEL,            END,        TABS,       VI_FIND,    REPLACE,    None,           None,       VOLU,
        VI_MVLD,    VI_PRVW,        LEFT,           DOWN,       RIGHT,          VI_NXTW,    TOOLS,      None,       None,       OPEN,           None,       VOLD,
        TAB,        VI_UNDO,        VI_CUT,         VI_YANK,    VI_PAST,        TO(2),      DESKTOP,    None,       PTAB,       NTAB,           LOCK,       None,
        LCTRL,      LCTRL,          VI_APND.L(1),   VI_APND.L(1),LSFT_SPC,      LSFT_SPC,   BSPC,       LALT,       LEFT,       UP,             DOWN,       RIGHT,
    ],
    
    # Edit 
    [
        TO(0),      F1,             F2,             F3,         F4,             F5,         F6,         F7,         F8,         F9,             F10,        F11,
        GRV,        N1,             N2,             N3,         N4,             N5,         N6,         N7,         N8,         N9,             N0,         BSLS,
        EQL,        Q,              D,              R,          W,              L,          J,          F,          U,          P,              SCLN,       LBRC,
        MINS,       A,              S,              H,          T,              G,          Y,          N,          E,          O,              I,          QUOT,
        TAB,        Z,              X,              C,          V,              B,          K,          M,          COMM,       DOT,            SLSH,       RBRC,
        LCTRL,      LCTRL,          ENT,            ENT,        LSFT_SPC,       LSFT_SPC,   BSPC,       RALT,       LEFT,       UP,             DOWN,       RIGHT,
    ],

    # Visual
    [
        TO(0),              F1,             F2,             F3,             F4,             F5,                 F6,         F7,             F8,             F9,         F10,            F11,
        COMMENT,            ALL,            PTAB,           NTAB,           SAVE,           CLOSE,              None,       None,           None,           None,       None,           F12,
        M_LSFT(VI_NXTL),    M_LSFT(HOME),   BSPC,           M_LSFT(UP),     DEL,            M_LSFT(END),        TABS,       VI_FIND,        None,           None,       None,           VOLU,
        M_LSFT(VI_PRVL),    M_LSFT(VI_PRVW),M_LSFT(LEFT),   M_LSFT(DOWN),   M_LSFT(RIGHT),  M_LSFT(VI_NXTW),    TOOLS,      None,           None,           OPEN,       None,           VOLD,
        TAB,                VI_UNDO,        VI_CUT,         VI_YANK,        VI_PAST,        TO(0),              DESKTOP,    None,           PTAB,           NTAB,       LOCK,           None,
        LCTRL,              LCTRL,          VI_APND.L(1),   VI_APND.L(1),   LSFT_SPC,       LSFT_SPC,           BSPC,       LALT,           M_LSFT(LEFT),   M_LSFT(UP), M_LSFT(DOWN),   M_LSFT(RIGHT),
    ],
]

# fmt: on

# Process the keymap into the 12x12 matrix format
from remapper import remapper

keymap = remapper(keymap)

keyboard.add_keymap(keymap, 12, 12)
keyboard.run_forever()
```

@section p_3_6  3.6 Hackpad Keyboard

<div style="margin-left: 100px;">
  <img src="Hackpad_keyboard.jpg">
</div>

Example of using capacitive touch sensing technology - a macro keypad called **Hackpad**.

Runs on *Seeed Xiao RP2040* with the **MPR121** capacitive sensor and **DRV2605** for haptic feedback.  
For these chips, Adafruit provides driver libraries, though independent drivers for other chips also exist.  
Using custom drivers may require small MKX changes (mostly updating includes).  

Hackpad uses a 6×6 key matrix. A keypress is triggered when exactly two electrodes are activated.  
This is not a send/receive type architecture, and multi-touch is not supported.  

Electrode pads are covered with solder mask for protection.  
Key legends can be drawn with a marker and removed using high-percentage alcohol (IPA).  
⚠️ Covering MPR121 electrodes with film significantly degrades sensing (material + air gap effects).  

For storage/programming mode (see boot.py), micro mechanical switch is added on the back of the PCB, connected to pins D9 and D10.  

``` {.py}
# boot.py

import board

from mkx.boot_config import boot_cfg

boot_cfg(
    sense=board.D9,  
    source=board.D10,  
    autoreload=True,  
    storage=True,  
    usb_id=("MKX Device", "Hackpad"),  
)
```
  
``` {.py}
# code.py

import board

from mkx.i2c import init_i2c
from mkx.mkx_touch import MKX_Touch

from mkx.layer_status_led_rgb_threepin import LayerStatusLedRgbThreePin

from mkx.keys_standard import *
from mkx.keys_modifiers import M_LCTL, M_LSFT, M_LGUI
from mkx.keys_vim import *

from mkx.periphery_touch import PeripheryTouch
from mkx.interface_touch import InterfaceTouch

from mkx.haptic import Haptic

keyboard = MKX_Touch()

status_led = LayerStatusLedRgbThreePin(
    board.D1, board.D0, board.D2, brightness=1, common_anode=True
)
status_led.add_layer(0, (0, 0, 255))  # Layer 0: Blue
status_led.add_layer(1, (255, 0, 0))  # Layer 1: Red
keyboard.add_layer_status_led(status_led)

i2c = init_i2c(board.SCL, board.SDA, status_led)

keyboard.add_periphery_touch(PeripheryTouch(i2c, address=0x5B, irq_pin=board.D6))

# Define touch sensor electrode mapping (columns and rows on the 0x5B sensor)
electrodes_col = {
    0x5B: tuple(range(6, 12)),  # Touch pins 6-11 map to Hackpad columns
}
electrodes_row = {
    0x5B: tuple(range(0, 6)),  # Touch pins 0-5 map to Hackpad rows
}

# Create 6x6 grid interface from touch sensor electrodes
keyboard.add_interface(
    InterfaceTouch.from_rows_cols(electrodes_col, electrodes_row, 0, 0, 5, 5)
)

# Configure haptic feedback (vibration motor)
hap = Haptic(i2c, 48, board.D7, play_on_init=True)
hap.set_electrodes(electrodes_col)  # Vibrate on
keyboard.add_haptic(hap)


OPEN = M_LCTL(O)
CLOSE = M_LCTL(W)
SAVE = M_LCTL(S)

DESKTOP = M_LGUI(D)
LOCK = M_LGUI(L)

PANEL = M_LCTL(J)
TOOLS = M_LCTL(B)
PTAB = M_LCTL(PGUP)
NTAB = M_LCTL(PGDN)

ALL = M_LCTL(A)
COMMENT = M_LCTL(SLSH)
FIND = M_LCTL(F)
REPLACE = M_LCTL(H)

BUILD = F7
DEBUG = F5
RUN = F9

# fmt: off

# Keymap: 2 layers -> 6 rows × 6 columns
keymap = [
    # Layer 0: Normal mode (IDE navigation and editing)
    [
        ESC,        F1,             F2,             F3,         F4,             F5,
        TOOLS,      PANEL,          DESKTOP,        BUILD,      DEBUG,          RUN,
        COMMENT,    ALL,            PTAB,           NTAB,       SAVE,           CLOSE,
        VI_MVLU,    HOME,           BSPC,           UP,         DEL,            END,
        VI_MVLD,    VI_PRVW,        LEFT,           DOWN,       RIGHT,          VI_NXTW,
        TAB,        VI_UNDO,        VI_CUT,         VI_YANK,    VI_PAST,        TO(1),
    ],

    # Layer 1: Visual/Selection mode (Vim-style text selection with Shift modifiers)
    [
        TO(0),              F1,             F2,             F3,             F4,             F5,
        TOOLS,              PANEL,          DESKTOP,        BUILD,          DEBUG,          RUN,
        COMMENT,            ALL,            PTAB,           NTAB,           SAVE,           CLOSE,
        M_LSFT(VI_NXTL),    M_LSFT(HOME),   BSPC,           M_LSFT(UP),     DEL,            M_LSFT(END),
        M_LSFT(VI_PRVL),    M_LSFT(VI_PRVW),M_LSFT(LEFT),   M_LSFT(DOWN),   M_LSFT(RIGHT),  M_LSFT(VI_NXTW),
        TAB,                VI_UNDO,        VI_CUT,         VI_YANK,        VI_PAST,        TO(0),
    ],
]

# fmt: on

keyboard.add_keymap(keymap, 6, 6)
keyboard.run_forever()
```