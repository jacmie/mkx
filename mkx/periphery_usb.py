# usb_periphery.py

import usb_cdc
import json
from periphery_base import PeripheryBase


class USBPeriphery(PeripheryBase):
    def __init__(self, device_id="usb"):
        super().__init__(device_id)
        self.serial = usb_cdc.data
        self.buffer = b""

    def get_events(self):
        events = []
        if self.serial.in_waiting:
            data = self.serial.read(self.serial.in_waiting)
            self.buffer += data
            while b"\n" in self.buffer:
                line, self.buffer = self.buffer.split(b"\n", 1)
                try:
                    msg = json.loads(line.decode().strip())
                    if msg.get("type") == "key":
                        events.append((msg["row"], msg["col"], bool(msg["pressed"])))
                except Exception as e:
                    print("USB parse error:", e)
        return events

    def send_status(self, msg_type, data):
        msg = {"type": msg_type, **data}
        try:
            self.serial.write((json.dumps(msg) + "\n").encode())
        except Exception as e:
            print("USB send error:", e)


# Host-Side Example (Python)
# If you're using a board connected to a host PC as a periphery:

# import serial

# with serial.Serial('/dev/ttyACM1', 115200) as ser:
#     while True:
#         row, col, val = scan_some_keys()
#         line = f"{row},{col},{int(val)}\n"
#         ser.write(line.encode())


# Notes
# Make sure usb_cdc.data is enabled in boot.py:

# python
# Copy
# Edit
# import usb_cdc
# usb_cdc.enable(console=True, data=True)  # Enable secondary CDC port

# Integration
# python
# Copy
# Edit
# from usb_periphery import USBPeriphery

# usb = USBPeriphery(device_id="usb_left")
# central = CentralAggregator(peripheries=[usb])
