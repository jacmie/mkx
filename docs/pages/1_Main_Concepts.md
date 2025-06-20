@page p_1 1 Main Concepts
@tableofcontents

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
<br>

@section p_1_1 1.1 Central

The **Central** board handles all data processing from the **Peripheries** and transmits HID reports to the host system over USB or BLE.  
<br>

@section p_1_2 1.2 Periphery

The **Periphery** is responsible only for sensing the key matrix (and possibly other elements, such as battery level) and sending messages to the **Central**.  
**Periphery** is designed to be fast and power-efficient.  

The **Central** board can simultaneously act as a **Periphery**, allowing it to listen to itself.  
<br>

@section p_1_3 1.3 MKX Keyboard

All boards capable of running [Circuit Python](https://circuitpython.org/downloads) should be suitable for a keyboard.  
The library has already been tested on boards: Waveshare RP2040-Zero, Seeed XIAO RP2040, PGA2040, Feather ESP32-S3  

The MKX architecture is designed to be flexible and reliable.  
It includes mechanisms for time synchronization, debouncing, matrix scanning warm-up, user configuration checks, and other features that enhance stability.  

The system is theoretically capable of supporting multiple **Peripheries** connected to and communicating bidirectionally with the **Central**, but there are a few limitations:
- Circuit Python can establish only one stable BLE connection
- Currently, only UART is used for communication between the **Peripheries** and the **Central**
- Sending data from the **Central** to the **Peripheries** is possible, but not yet implemented
