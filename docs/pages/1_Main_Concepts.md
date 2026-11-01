@page p_1 1 Main Concepts
@tableofcontents

@section p_1_1 1.1 MKX Keyboard

All boards capable of running [Circuit Python](https://circuitpython.org/downloads) should be suitable for a keyboard.  
The library has already been tested on boards: Waveshare RP2040-Zero, Seeed XIAO RP2040, Seeed XIAO RP2350, Seeed Xiao nRF52840, PGA2040, Feather ESP32-S3  

The MKX architecture is designed to be flexible and reliable.  
It includes mechanisms for time synchronization, debouncing, matrix scanning warm-up, user configuration checks, and other features that enhance stability.  

There are three top level keyboard classes, each covering a different scenario (see @ref p_4_2, @ref p_4_3 and @ref p_4_5):

**MKX_Single** - one MCU, one local key matrix, no split support.

    ┌──────────────────────────────┐
    │        PC / Host Device      │
    │   (receives USB HID input)   │
    └──────────────────────────────┘
                    ▲
               USB/BLE HID
                    ▲
            ┌───────────────┐
            │   MKX_Single  │
            │  Scan + Logic │
            └───────────────┘
<br>

**MKX_Central** - one MCU acting as **Central**, optionally combined with one or more **Peripheries**, for split keyboards.

    ┌──────────────────────────────┐
    │        PC / Host Device      │
    │   (receives USB HID input)   │
    └──────────────────────────────┘
                    ▲
               USB/BLE HID
                    ▲
            ┌───────────────┐
            │    CENTRAL    │
            │ Master Logic  │
            └───────────────┘
                    ▲
      ┌───────────┐   ┌───────────┐
      │ PERIPHERY │   │ PERIPHERY │
      │  Central  │   │    UART   │
      │(Only Scan)│   │(Only Scan)│
      └───────────┘   └───────────┘

The system is theoretically capable of supporting multiple **Peripheries** connected to and communicating bidirectionally with the **Central**, but there are a few limitations:
- Circuit Python can establish only one stable BLE connection
- Currently, only UART is used for communication between the **Peripheries** and the **Central**
- Sending data from the **Central** to the **Peripheries** is possible, but not yet implemented
<br>

**MKX_Touch** - standalone capacitive touch keyboard built on an MPR121 touch sensor instead of a mechanical matrix (see @ref p_1_8).

    ┌──────────────────────────────┐
    │        PC / Host Device      │
    │   (receives USB HID input)   │
    └──────────────────────────────┘
                    ▲
               USB/BLE HID
                    ▲
            ┌───────────────┐
            │   MKX_Touch   │
            │ Touch + Logic │
            └───────────────┘
                    ▲
                   I2C
                    ▲
            ┌───────────────┐
            │ MPR121 Sensor │
            │  (Electrodes) │
            └───────────────┘
<br>

@section p_1_2 1.2 Central

The **Central** board handles all data processing from the **Peripheries** and transmits HID reports to the host system over USB or BLE.  
<br>

@section p_1_3 1.3 Periphery

The **Periphery** is responsible only for sensing the key matrix (and possibly other elements, such as battery level) and sending messages to the **Central**.  
**Periphery** is designed to be fast and power-efficient.  

The **Central** board can simultaneously act as a **Periphery**, allowing it to listen to itself.  
<br>

@section p_1_4 1.4 Matrix Scanning

Reading the physical key matrix is handled internally by **MatrixScanner**, used by every **Periphery**.  
It automatically picks the fastest scanning backend the hardware allows, trying each in this order:

1. **rp2pio** - on RP2040/RP2350 boards, drives all columns and samples all rows in a single PIO state-machine instruction, the fastest option available.  
   It requires raw `microcontroller.Pin` objects for both columns and rows (not pins wrapped in `digitalio`, nor pins behind an I2C expander), at most 32 column pins and 32 row pins,  
   and - due to a hardware limitation of the PIO "out pins"/"in pins" instructions, which only accept a base pin plus a count - the column pins must form one contiguous, ascending GPIO block (e.g. GP2-GP7)  
   and the row pins a separate contiguous, ascending block (e.g. GP8-GP12).  
   Descending or non-contiguous pin layouts are rejected automatically and fall through to the next backend.
2. **keypad.KeyMatrix** - CircuitPython's built-in background matrix scanner, implemented in optimized interrupt-driven C code.  
   It is very fast, uses virtually no CPU time, and - unlike rp2pio - has no pin-ordering or contiguity restrictions, making it the recommended choice whenever rp2pio's strict layout isn't needed.  
   Like rp2pio, it still requires raw microcontroller pins.
3. **digitalio** (fallback) - a plain, software bit-banged scan driving one column at a time and reading each row through `digitalio`.  
   It is the slowest option, but works on every board and pin type, including pins wired through an I2C GPIO expander (e.g. MCP23017) that the two accelerated backends cannot reach.

Each accelerated backend can be disabled independently through the **Periphery** `use_rp_pio`/`use_keypad_scan` options, forcing a fallback further down the list,  
which is mainly useful for testing or troubleshooting a specific hardware layout.  
Since the fastest available backend is always chosen automatically, the physical pin layout chosen for a keyboard directly affects scanning performance:  
raw, contiguous GPIO pins get the full PIO speed, raw non-contiguous pins still get the fast interrupt-driven keypad scan,  
while pins routed through an I2C expander always fall back to the slower, polled digitalio scan.

@section p_1_5 1.5 Interfaces and Coordinate Mapping

An **Interface** bridges a physical **Periphery** (or touch sensor) to a single, logical keymap address space.  
Every **Interface** declares the rectangular area of the keymap it is responsible for using `col_min`, `row_min`, `col_max` and `row_max` boundaries, and is matched to its **Periphery** by a shared `device_id`.

This indirection is what allows a split keyboard to combine several physically independent matrices (left half, right half, one or more UART **Peripheries**) into one continuous keymap, each **Interface** simply claiming its own region of columns and rows.  
Min/max boundaries can be inverted (min bigger than max), which mirrors the key order without changing any wiring, handy for keyboard halves that are physically rotated or mirrored.

Available interfaces are **InterfaceSingle**, **InterfaceCentral**, **InterfaceUART** and **InterfaceTouch** (with **InterfaceTouchSlider** / **InterfaceTouchWheel** for continuous input), see @ref p_4_6.

@section p_1_6 1.6 Keymap and Layers

The **Keymap** is a list of layers, where each layer is a flat list of keys sized `col_size * row_size` (see @ref p_4_3_5).  
Unused positions in non-rectangular layouts can be set to **None**.

Layers are not simply swapped one for another: the **LayersManager** keeps a stack of currently active layers on top of a persistent default layer.  
Only the top-most active layer is used to resolve key presses (and to drive the Layer Status LED color), while layers lower in the stack remain active until explicitly released, enabling momentary layers, layer toggles and layer taps to be combined freely.  
See the **DF**, **RL**, **MO**, **LT**, **TG**, **TO** and **TT** layer keys at @ref p_5_3.

@section p_1_7 1.7 Keys System

Every key in a keymap derives from **KeysAbstract**, implementing `on_press()` and `on_release()` callbacks that receive the **LayersManager**, the HID **Keyboard** object and a timestamp.  
Keys are grouped by behavior: standard, modifiers, media, mouse, layers, hold-tap, tap dance, sticky keys, key sequences and a hardware VIM mode, see @ref p_5 for the full reference.

Some keys (hold-tap, tap dance) need to act after a timeout even if no further event occurs, independently of matrix scanning.  
These keys implement **TimedKeys**, and the **TimedKeysManager** polls them every loop iteration so delayed actions (like firing a "hold" behavior) still happen on time.

@section p_1_8 1.8 Capacitive Touch Input

**MKX_Touch** is a separate keyboard architecture for capacitive touch keyboards built around the MPR121 touch sensor (**PeripheryTouch**), communicating over I2C (see @ref p_4_9).  
It does not use a mechanical matrix, cannot be combined with classical switches, and does not support split keyboards.

**InterfaceTouch** supports two input modes:
- single electrode mode, a direct one-to-one mapping between electrodes and keys
- 2-electrode matrix mode, pairing column and row electrodes next to each other to multiply the number of keys per sensor, at the cost of multi-touch support (only one key combination can be resolved at a time)

**InterfaceTouchSlider** and **InterfaceTouchWheel** turn a row (or circle) of electrodes into a continuous linear or rotary control, generating repeated key events (for example volume up/down) based on motion, with optional dynamic step sizing for faster scrubbing, see @ref p_4_6_5 and @ref p_4_6_6.

Touch events can optionally trigger the **Haptic** driver (DRV2605) for vibration feedback, restricted to specific electrodes if desired, see @ref p_4_10.

@section p_1_9 1.9 Visual and Haptic Feedback

The **Layer Status LED** indicates the currently active top layer through color or an LED array, useful at a glance without looking at the screen, see @ref p_4_7.  
The **Backlight** illuminates the keyboard itself, either with a static color or an animated rainbow effect, see @ref p_4_8.  
The **Haptic** driver provides vibration feedback, primarily used with **MKX_Touch** (see @ref p_1_8 and @ref p_4_10).

@section p_1_10 1.10 Connectivity and Safety

The keyboard reports to the host as a standard USB HID device, or over Bluetooth Low Energy (BLE) if enabled with `use_ble(True)`. Circuit Python supports only one stable BLE connection at a time.

**boot.py** can call `boot_cfg()` to configure USB endpoints (keyboard, mouse, consumer control, N-key rollover) and disable features like autoreload or USB storage before the main workflow starts.  
A dedicated sense pin lets this configuration be skipped on demand, so the board always has a way to fall back to a mountable, debuggable state if something goes wrong, see @ref p_4_1.
