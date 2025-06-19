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


