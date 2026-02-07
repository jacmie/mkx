@page p_4 4 MKX API
@tableofcontents

@section p_4_1 4.1 Boot Config

The **boot_cfg** function can be used in **boot.py**, which should be placed in the root directory of your CircuitPython device, alongside **code.py** or **main.py**.  

**boot.py** runs only once at startup, before any workflows are initialized. This allows you to configure USB and other settings dynamically at startup, rather than relying on fixed defaults.  
Because the serial console is not yet available, output is written to **boot_out.txt**.
For a more detailed explanation, see the [CircuitPython Documentation](https://docs.circuitpython.org/en/latest/README.html).  

If an error occurs during startup, the device should fall back to a mountable and debuggable configuration.  

⚠️️ **Warning:** *Always back up your code before disabling the storage feature. In critical scenarios incorrect pin configuration or other errors can make the board unresponsive.  
In such cases, a hard reset may be required, which erases all data and necessitates re-uploading your code.*

``` {.py}
# boot.py

import board

from mkx.boot_config import boot_cfg

boot_cfg(
    sense,
    source=None,
    autoreload: bool = True,
    boot_device: int = 0,
    cdc: bool = True,
    consumer_control: bool = True,
    keyboard: bool = True,
    midi: bool = True,
    mouse: bool = True,
    nkro: bool = False,
    pan: bool = False,
    storage: bool = True,
    usb_id: tuple[str, str] = None,
    **kwargs,
) -> bool:

```

**sense**  
`sense` accepts either uninitialized `microcontroller.Pin`, or `digitalio.DigitalInOut`.
The boot configuration is only applied if `sense` reads `True` or "high", and
skipped if it reads `False` or "low".
If `sense` is an uninitialized `Pin`, it'll be configured as pulled-up input; it
wont be further configured if it is a `DigitalInOut`.


**source**  
`source` accepts either uninitialized `microcontroller.Pin`, `digitalio.DigitalInOut`, or `None`.
It's the "source" of the test voltage to be read by the sense pin.
If `source` is an uninitialized `Pin`, it'll be configured as a "low" output; it
wont be further configured if it is a `DigitalInOut`.

Common matrix and direct pin configurations (see also the examples below):

|diode_orientation |sense pin  |source pin |
|------------------|-----------|-----------|
|`COL2ROW`         |column     |row        |
|`ROW2COL`         |row        |column     |
|direct pin        |direct pin |`None`     |

**autoreload**  
By default, CircuitPython automatically reloads whenever files are saved (and sometimes unexpectedly due to board glitches).  
This behavior is useful during development, allowing you to see changes immediately.  
For everyday use, it’s recommended to disable autoreload to improve stability.  

**boot_device**  
Boot HID device configuration for `usb_hid`, see the [`usb_hid` documentation](https://docs.circuitpython.org/en/latest/shared-bindings/usb_hid/index.html#usb_hid.enable)
for details.

**cdc**  
Enables or disables the USB endpoint that provides the CircuitPython serial console (REPL), allowing or preventing access to the interactive prompt over USB.

**consumer_control**  
Enable the HID endpoint for consumer control reports. Those are extra keys for
things like multimedia control and browser shortcuts.

**keyboard**  
Enable the keyboard HID endpoint.  

**midi**  
Enable MIDI over USB. Enabled by default in CircuitPython, but most keyboards don't use it.

**mouse**  
Enables the HID USB endpoint for a pointing device. Unlike a keyboard, a mouse provides continuous input along multiple axes, allowing movement in all directions rather than discrete key presses.

**nkro**  
Enables N-key rollover support. When the default keyboard is active, this replaces the standard 6-key rollover endpoint with an N-key rollover endpoint.  
This is not a standard HID feature, so it’s intended for advanced users who understand the implications.

**pan**  
Enables horizontal scrolling (panning) for the HID pointing device (mouse) endpoint.

**storage**  
Disables USB storage to prevent your computer from automatically recognizing the device as a new removable drive when the keyboard is connected.  
Preventing the board from appearing as a mass storage device, may be important for cybersecurity policies in some workplaces.

**usb_id**  
Introduced in CircuitPython 8, this allows you to customize your keyboard’s USB identity instead of using the default “MCU board manufacturer – CircuitPython device.”

**return value**  
*boot_cfg* returns **True** if the boot configuration was applied successfully, and **False** if it was skipped.  
This allows the sense pin mechanism to be reused for other custom boot configurations.  
Any unexpected errors are not caught intentionally, so they are recorded in **boot_out.txt** to facilitate debugging.  

**Example:**
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

@section p_4_2 4.2 MKX Central

Main **MKX** class that manages keyboard operation and handles communication with the computer.  


``` {.py}
from mkx.mkx_central import MKX_Central

MKX_Central(
    keymap=None, 
    coord_mapping=None
)
```

**keymap**  
Add *keymap* object to the **MKX_Central**.
May be also added later with the **add_keymap()** method.

**coord_mapping**  
Add custom *coord_mapping* object to the **MKX_Central**.  
Usualy coord_mapping is defined while **MKX Interpfaces** declaration.  
May be also added later with the **add_coord_mapping()** method. # TO DO

**Example:**
``` {.py}
from mkx.mkx_central import MKX_Central

mkx_central = MKX_Central()
```

@subsection p_4_2_1 4.2.1 add_periphery_central

Add **PeripheryCentral** to the ***MKX_Central**.  

``` {.py}
mkx_central.add_periphery_central(
    central_periphery: PeripheryAbstract
)
```

**central_periphery**  
*PeripheryCentral* object.

**Example:**
``` {.py}
from mkx.mkx_central import MKX_Central
from mkx.periphery_central import PeripheryCentral

mkx_central = MKX_Central()

central_peryphery = PeripheryCentral("central", col_pins, row_pins)
mkx_central.add_periphery_central(central_peryphery)
```

@subsection p_4_2_2 4.2.2 add_interface

Add **Interface** of a **Periphery** to the **MKX_Central**.  

``` {.py}
mkx_central.add_interface(
    interface: InterfahceAbstract
)
```

**interface**  
*Interface* object.

**Example:**
``` {.py}
from mkx.mkx_central import MKX_Central
from mkx.periphery_central import PeripheryCentral
from mkx.interface_central import InterfaceCentral
from mkx.interface_uart import InterfaceUART

mkx_central = MKX_Central()

central_peryphery = PeripheryCentral("central", col_pins, row_pins)

interface_central = InterfaceCentral(central_peryphery, 0, 0, 5, 4)
keyboard.add_interface(interface_central)
 
interface_right = InterfaceUART("right_peryphery", None, board.GP1, 11, 0, 6, 4)
keyboard.add_interface(interface_right)
```

@subsection p_4_2_3 4.2.3 add_layer_status_led

Add **LayerStatusLed** to the **MKX_Central**.  

``` {.py}
mkx_central.add_layer_status_led(
    status_led: LayerStatusLedAbstract
)
```

**status_led**  
*LayerStatusLed* object.

**Example:**  
``` {.py}
import board

from mkx.mkx_central import MKX_Central
from mkx.layer_status_led_rgb_neopixel import LayerStatusLedRgbNeoPixel

mkx_central = MKX_Central()

status_led = LayerStatusLedRgbNeoPixel(board.SCK)
status_led.add_layer(0, (0, 0, 255))  # Blue
status_led.add_layer(1, (0, 255, 0))  # Green
status_led.add_layer(2, (255, 255, 255))  # White
status_led.add_layer(3, (255, 0, 0))  # Red
mkx_central.add_layer_status_led(status_led)
```

@subsection p_4_2_4 4.2.4 add_backlight

Add **Backlight** to the **MKX_Central**.  

``` {.py}
mkx_central.add_backlight(
    backlight: BacklightAbstract
)
```

**backlight**  
*Backlight* object.

**Example:**  
``` {.py}
import board

from mkx.mkx_central import MKX_Central
from mkx.backlight_neopixel_rainbow import BacklightNeopixelRainbow

mkx_central = MKX_Central()

backlight = BacklightNeopixelRainbow(board.A0, num_pixels=72, brightness=0.4)
backlight.slower(2)
backlight.set_swirl(True)
mkx_central.add_backlight(backlight)
```

@subsection p_4_2_5 4.2.5 add_keymap

Add **Keymap** to the **MKX_Central**.  
**Keymap** must have rectangular shape. In custom layouts where certain positions are unused, set them to **None**.

``` {.py}
mkx_central.add_keymap(
    keymap, 
    col_size, 
    row_size
)
```

**keymap**  
*Keymap* object.

**col_size**  
Keymap layer max column number.  
Counting starts from '0'.  

**row_size**  
Keymap layer max row number.  
Counting starts from '0'.  

**Example:**  
``` {.py}
from mkx.mkx_central import MKX_Centrals
 
from mkx.keys_standard import *
 
mkx_central = MKX_Central()
 
# fmt: off

keymap = [
    [
        A,  B,  C,
        N1, N2, None,
    ],
]
 
# fmt: on
 
mkx_central.add_keymap(keymap, 2, 1)
```

@subsection p_4_2_6 4.2.6 use_ble

Enable or disable BLE.  

``` {.py}
mkx_central.use_ble(
    use_ble: bool
)
```

**use_ble**  
Flag to enable or disable BLE connection, default *False*.

**Example:**
``` {.py}
from mkx.mkx_central import MKX_Central

mkx_central = MKX_Central()
mkx_central.use_ble(True)
```

@subsection p_4_2_7 4.2.7 run_forever

Start running keyboard's infinite loop.


``` {.py}
mkx_central.run_forever()

```


@section p_4_3 4.3 MKX Periphery

The general **Periphery** captures keystrokes and transmit messages to the **MKX_Central**.  
The **MKX_Periphery** is a simpler counterpart to the **MKX_Central**,  
operating continuously on hardware separate from the **MKX_Central**.  
Each **MKX_Periphery** is assigned a general **Periphery**.

The general **Periphery** can be implemented as **PeripheryCentral**, which operates on the same hardware module as the Central,  
or as **PeripheryUART**, on a separate hardware module and communicates via UART.  

``` {.py}
from mkx.mkx_periphery import MKX_Periphery

mkx_periphery = MKX_Periphery(
    uart_peryphery: PeripheryAbstract, 
    debug :bool=False
)
```

**uart_peryphery**  
PeripheryUART object (or other derived from the *PeripheryAbstract*).  

**debug**  
Flag enabling verbose output for the Periphery.  

@subsection p_4_3_1 4.3.1 PeripheryCentral

Set the PeripheryCentral.

``` {.py}
from mkx.periphery_central import PeripheryCentral

mkx_periphery = PeripheryCentral(
    device_id: str, 
    col_pins, 
    row_pins, 
    **kwargs
)
```

**device_id**  
Device id/name.  

**col_pins**  
List of column pins.  

**row_pins**  
List of row pins.  

** **kwargs**  
Other optional arguments.  

**Example:**
``` {.py}
import board
 
from mkx.mkx_central import MKX_Central
from mkx.periphery_central import PeripheryCentral
from mkx.interface_central import InterfaceCentral
from mkx.interface_uart import InterfaceUART

mkx_central = MKX_Central()
 
col_pins = (board.GP9, board.GP7, board.GP5, board.GP4, board.GP3, board.GP2)
row_pins = (board.GP10, board.GP11, board.GP13, board.GP15, board.GP17)
 
central_peryphery = PeripheryCentral("central_peryphery", col_pins, row_pins)
mkx_central.add_periphery_central(central_peryphery)

interface_central = InterfaceCentral(central_peryphery, 0, 0, 5, 4)
mkx_central.add_interface(interface_central)
 
interface_right = InterfaceUART("side_periphery", None, board.GP1, 11, 0, 6, 4)
mkx_central.add_interface(interface_right)

# other code ...

mkx_central.run_forever()
```

@subsection p_4_3_2 4.3.2 PeripheryUART

Set the PeripheryUART.

``` {.py}
from mkx.periphery_uart import PeripheryUART

mkx_periphery = PeripheryUART(
    device_id: str, 
    col_pins, 
    row_pins, 
    tx_pin,
    rx_pin,
    *,
    baudrate=9600,
    **kwargs
)
```

**device_id**  
Device id/name.  

**col_pins**  
List of column pins.  

**row_pins**  
List of row pins.  

**tx_pin**  
TX communication pin.  

**rx_pin**  
RX communication pin.  

**baudrate**  
UART communication baudrate.  

** **kwargs**  
Other optional arguments.  

**Example:**
``` {.py}
import board
 
from mkx.mkx_periphery import MKX_Periphery
from mkx.periphery_uart import PeripheryUART
 
 
col_pins = (board.GP9, board.GP7, board.GP5, board.GP4, board.GP3, board.GP2)
row_pins = (board.GP10, board.GP11, board.GP13, board.GP15, board.GP17)
 
peryphery = PeripheryUART("booster_r", col_pins, row_pins, board.GP0, board.GP1)
 
mkx_periphery = MKX_Periphery(peryphery, debug=True)
mkx_periphery.run_forever()
```

@section p_4_4 4.4 Interface

The **Interface** connects the **Peripheries** to the **MKX_Central**.  

Possible options are **InterfaceCentral** matching the **PeripheryCentral** and  
**InterfaceUART** matching the **PeripheryUART**.  

**Example:**
``` {.py}
import board
 
from mkx.mkx_central import MKX_Central
from mkx.periphery_central import PeripheryCentral
from mkx.interface_central import InterfaceCentral
from mkx.interface_uart import InterfaceUART

mkx_central = MKX_Central()
 
col_pins = (board.GP9, board.GP7, board.GP5, board.GP4, board.GP3, board.GP2)
row_pins = (board.GP10, board.GP11, board.GP13, board.GP15, board.GP17)
 
central_peryphery = PeripheryCentral("central_peryphery", col_pins, row_pins)
mkx_central.add_periphery_central(central_peryphery)

interface_central = InterfaceCentral(central_peryphery, 0, 0, 5, 4)
mkx_central.add_interface(interface_central)
 
interface_right = InterfaceUART("side_periphery", None, board.GP1, 11, 0, 6, 4)
mkx_central.add_interface(intefhace_right)

# other code ...

mkx_central.run_forever()
```

@subsection p_4_4_1 4.4.1 InterfaceCentral

Set the InterfaceCentral.  

Min/max column and rows values can be inverted, meaning min value can be bigger than max.  
Inverted min/max column and rows values will change the keys mapping.  

``` {.py}
from mkx.interface_central import InterfaceCentral

interface = InterfaceCentral(
    central_periphery: InterfahceAbstract, 
    col_min :int, 
    row_min :int, 
    col_max :int, 
    row_max :int
)
```

**central_periphery**  
PeripheryCentral object.

**col_min**  
Minimum column number. Counting start from '0'.  

**row_min**  
Minimum row number. Counting start from '0'.  

**col_max**  
Maximum column number. Counting start from '0'.  

**row_max**  
Maximum row number. Counting start from '0'.  


@subsection p_4_4_2 4.4.2 InterfaceUART

Set the InterfaceUART.

``` {.py}
from mkx.interface_uart import InterfaceUART

mkx_periphery = InterfaceUART(
    device_id: str, 
    tx_pin,
    rx_pin,
    col_min :int,
    row_min :int,
    col_max :int,
    row_max :int,
    baudrate=9600
)
```

**device_id**  
Device id/name, must match the device_id of the **Periphery**.  

**tx_pin**  
TX communication pin.  

**rx_pin**  
RX communication pin.  

**col_min**  
Minimum column number. Counting start from '0'.  

**row_min**  
Minimum row number. Counting start from '0'.  

**col_max**  
Maximum column number. Counting start from '0'.  

**row_max**  
Maximum row number. Counting start from '0'.  

**baudrate**  
UART communication baudrate.  


@section p_4_5 4.5 Layer Status LED

Status LED used for the indication of the active layer.  

@subsection p_4_5_1 4.5.1 LayerStatusLedRgbNeoPixel

RGB NeoPixel LED which indicates active layer by color.  

``` {.py}
from mkx.layer_status_led_rgb_neopixel import LayerStatusLedRgbNeoPixel

status_led = LayerStatusLedRgbNeoPixel(
    status_led_pin, 
    brightness :float=0.1, 
    auto_write :bool=True
)
```

**status_led_pin**  
Pin for the RGB NeoPixel LED.  

**brightness**  
Brightness of the LED in the range 0-1.  

**auto_write**  
Flag to update LED color automaticly.  

**Example:**
``` {.py}
import board
 
from mkx.mkx_central import MKX_Central
from mkx.layer_status_led_rgb_neopixel import LayerStatusLedRgbNeoPixel
 
mkx_central = MKX_Central()
 
status_led = LayerStatusLedRgbNeoPixel(board.GP23, brightness=0.015)
status_led.add_layer(0, (0, 255, 0))  # Green
status_led.add_layer(1, (0, 0, 255))  # Blue

mkx_central.add_layer_status_led(status_led)
```

@subsection p_4_5_2 4.5.2 LayerStatusLedRgbThreePin

RGB three pin LED which indicates active layer by color.  
*Untested!* due to lack of proper hardware configuration.

``` {.py}
from mkx.layer_status_led_rgb_threepin import LayerStatusLedRgbThreePin

status_led = LayerStatusLedRgbThreePin(
    red_pin,
    green_pin,
    blue_pin
)
```
**red_pin**  
Red LED pin.

**green_pin**  
Green LED pin.

**blue_pin**  
Blue LED pin.

@subsection p_4_5_3 4.5.3 LayerStatusLedArray

Array of LED which indicates active layer.  
*Untested!* due to lack of proper hardware configuration.

``` {.py}
from mkx.layer_status_led_array import LayerStatusLedArray

status_led = LayerStatusLedArray(
    pins
)
```
**pins**  
List of pins for LED-s.

@section p_4_6 4.6 Backlight

<div style="margin-left: 100px;">
  <img width=800 src="RGB_backlight.jpg">
</div>

RGB NeoPixel backlight.

@subsection p_4_6_1 4.6.1 BacklightNeopixelStatic

Static color backlight.

``` {.py}
from mkx.backlight_neopixel_static import BacklightNeopixelStatic

status_led = BacklightNeopixelStatic(
    pin, 
    num_pixels :int, 
    rgb_color=(0, 0, 255), 
    brightness :float=1
)
```

**pin**  
Pin for the backlight RGB NeoPixel LED-s.  

**num_pixels**  
Number of the RGB NeoPixel LED-s.  

**rgb_color**  
Peaked values of the RGB color.  

**brightness**  
Brightness of the LED in the range 0-1.  

**Example:**
``` {.py}
import board
 
from mkx.mkx_central import MKX_Central
from mkx.backlight_neopixel_static import BacklightNeopixelStatic
 
mkx_central = MKX_Central()
 
backlight = BacklightNeopixelStatic(board.A0, num_pixels=72, rgb_color=(0, 0, 255), brightness=0.4)

mkx_central.add_backlight(backlight)
```

@subsection p_4_6_2 4.6.2 BacklightNeopixelRainbow

Rainbow animated color backlight.

``` {.py}
from mkx.backlight_neopixel_rainbow import BacklightNeopixelRainbow

status_led = BacklightNeopixelRainbow(
    pin, 
    num_pixels :int, 
    rgb_color=(0, 0, 255), 
    brightness :float=1
)
```

**pin**  
Pin for the backlight RGB NeoPixel LED-s.  

**num_pixels**  
Number of the RGB NeoPixel LED-s.  

**brightness**  
Brightness of the LED in the range 0-1.  

@subsection p_4_6_2_1 4.6.2.1 faster()

Hom much faster should be the rainbow animation from the initial one.

``` {.py}
backlight.faster(
    value
)
```

**value**  
Increased animation speed up to 20.

@subsection p_4_6_2_2 4.6.2.2 slower()

Hom much slower should be the rainbow animation from the initial one.

``` {.py}
backlight.slower(
    value
)
```

**value**  
Decreased animation speed up to 20.

@subsection p_4_6_2_3 4.6.2.3 set_swirl()

Should the LED-s change color independently by swirl or not.

``` {.py}
backlight.set_swirl(
    swirl :bool
)
```

**swirl**  
Swirl or not.

**Example:**
``` {.py}
import board
 
from mkx.mkx_central import MKX_Central
from mkx.backlight_neopixel_rainbow import BacklightNeopixelRainbow
 
mkx_central = MKX_Central()
 
backlight = BacklightNeopixelRainbow(board.A0, num_pixels=72, brightness=0.4)
backlight.slower(2)
backlight.set_swirl(True)

mkx_central.add_backlight(backlight)
```