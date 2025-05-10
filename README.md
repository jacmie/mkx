# MKX

Next Generation Mechanical Keyboard Firmware

    ┌──────────────────────────────┐
    │        PC / Host Device      │
    │   (receives USB HID input)   │
    └──────────────────────────────┘
                ▲
            USB HID
                ▲
        ┌───────────────┐
        │   CENTRAL     │
        │ Master Logic  │
        └───────────────┘
          ▲     ▲     ▲
        BLE UART  USB HID
        │           │
    ┌────────────┐ ┌────────────┐
    │ Left Half  │ │ Right Half │
    │  BLE/ UART │ │  BLE/ UART │
    │ (Only Scan)│ │ (Only Scan)│
    └────────────┘ └────────────┘


## Autosync library with board
pip install watchdog

error: externally-managed-environment
...
hint: See PEP 668 for the detailed specification.

python3 -m dev ../dev
source ../dev/bin/activate
pip install watchdog
python auto_sync.py

python auto_sync.py
to stop CTRL + C

## Install adafruit bundle 
In the dev environment:
pip install circup

With the board plugged and Circuit Python installed, dowload the appropriate version of the bundle:
circup list

DO IT BEFORE RENAMING THE DRIVE!!!
circup install adafruit_ble adafruit_hid
circup install adafruit_ble adafruit_hid adafruit_register adafruit_uuid
circup install adafruit_ble adafruit_hid --path /media/jacmie/CIRCUITPY


## Build with mpy
python build.py compile
python build.py upload
python build.py clean

## Code rules
- keep files structure flat
- place the library on board in the default CIRCUITPYTHON/lib



Peripheral board sends key press/release events.

Central board processes input and sends HID reports.

You want to group key events in time windows, to ensure consistent and correct modifier behavior (e.g., Ctrl+Z).

You’re concerned about desync, particularly modifiers and main keys falling into different frames.