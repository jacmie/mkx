@page p_3 3 Key Concepts
@tableofcontents

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


Peripheral board sends key press/release events.

Central board processes input and sends HID reports.

You want to group key events in time windows, to ensure consistent and correct modifier behavior (e.g., Ctrl+Z).