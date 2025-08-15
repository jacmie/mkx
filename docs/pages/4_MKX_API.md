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

@section p_4_2 4.2 HID

Type of HID device to use.  
Possible options are **HID_USB** for a standard USB HID device or **HID_BLE** for a Bluetooth Low Energy HID device.  

@subsection p_4_2_1  4.2.1 HID_USB

Set USB HID device.

**Example:**
``` {.py}
from mkx.hid_usb import HID_USB

hid = HID_USB()
keyboard.set_hid(hid) # TO DO
```

@subsection p_4_2_2  4.2.2 HID_BLE

Set BLE HID device.

**Example:**
``` {.py}
from mkx.hid_ble import HID_BLE

hid = HID_BLE()
keyboard.set_hid(hid) # TO DO
```


@section p_4_3 4.3 MKX Central
...

@section p_4_4 4.4 MKX Periphery
...

@section p_4_5 4.5 Interphace
...

@section p_4_6 4.6 Layer Status LED
...

@section p_4_7 4.7 Backlight
...