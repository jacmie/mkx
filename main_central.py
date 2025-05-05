from mkx.mkx_central_hid import MKXCentralHID
from mkx.core.matrix_scanner import MatrixScanner
from mkx.communication.periphery.periphery_ble import BLESlaveTransport
from mkx.communication.central_hid.central_hid_usb import USBHIDOutput

inputs = [MatrixScanner(rows=[...], cols=[...]), BLESlaveTransport()]
output = USBHIDOutput()

keyboard = MKXCentralHID(inputs=inputs, output=output)
keyboard.run_once()
# keyboard.run_forever()
