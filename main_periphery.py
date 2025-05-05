from mkx.periphery import MKXPeriphery
from mkx.core.matrix_scanner import MatrixScanner

# from mkx.output.ble_send import BLESendTransport
from mkx.communication.periphery.periphery_ble import BLEPeriphery

keyboard = MKXPeriphery(
    matrix=MatrixScanner(rows=[...], cols=[...]), output=BLESendTransport()
)
keyboard.run_forever()
