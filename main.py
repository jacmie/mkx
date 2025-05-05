from mkx.mkx import MKX
from mkx.input.ble_slave import BLESlaveTransport
from mkx.input.uart_slave import UARTSlaveTransport
from mkx.output.usb_hid import USBHIDOutput

# Optional: add only the transports the user wants
inputs = [
    BLESlaveTransport(),
    UARTSlaveTransport(),
]

output = USBHIDOutput()

keyboard = MKX(inputs, output)
keyboard.run_forever()
