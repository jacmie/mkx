from mkx.interface_abstract import InterfaceAbstract


class InterfaceSingle(InterfaceAbstract):
    def __init__(self, col_min, row_min, col_max, row_max):
        # device_id has to match the one used in PeripherySingle
        super().__init__("keyboard_single", col_min, row_min, col_max, row_max)

    def is_connected(self):
        pass  # Not needed

    def reconnect(self):
        pass  # Not needed

    def receive(self, verbose=False):
        pass  # Not needed

    def send(self, msg_type: str, data: dict, verbose=False):
        pass  # Not needed
