from mkx.interface_abstract import InterfaceAbstract
from mkx.ansi_colors import Ansi, Ansi256


class InterfaceTouch(InterfaceAbstract):
    def __init__(self, col_min, row_min, col_max, row_max):
        print(f"{Ansi256.MINT}{Ansi.BOLD}New Touch Interface:{Ansi.RESET}")
        print()
        self.electrodes = None
        self.electrodes_col = None
        self.electrodes_row = None
        self.use2electrodes = None
        self._last_active = {}  # Track previous state per address
        super().__init__("keyboard_touch", col_min, row_min, col_max, row_max)

    def _flatten_electrodes(electrodes_dict):
        result = []

        for addr, electrodes in electrodes_dict.items():
            for ele in electrodes:
                result.append((addr, ele))  # tuple instead of dict
                print(f"{Ansi256.SKY}(0x{addr:02X}, {ele}){Ansi.RESET}")
        print()

        return tuple(result)

    @classmethod
    def from_electrodes(cls, electrodes, col_min, row_min, col_max, row_max):
        obj = cls(col_min, row_min, col_max, row_max)
        obj.use2electrodes = False
        print(f"{Ansi256.MINT}electrodes:{Ansi.RESET}")
        obj.electrodes = cls._flatten_electrodes(electrodes)
        print(obj.electrodes)
        return obj

    @classmethod
    def from_rows_cols(
        cls, electrodes_col, electrodes_row, col_min, row_min, col_max, row_max
    ):
        obj = cls(col_min, row_min, col_max, row_max)
        obj.use2electrodes = True
        print(f"{Ansi256.MINT}electrodes col:{Ansi.RESET}")
        obj.electrodes_col = cls._flatten_electrodes(electrodes_col)
        print(f"{Ansi256.MINT}electrodes row:{Ansi.RESET}")
        obj.electrodes_row = cls._flatten_electrodes(electrodes_row)
        return obj

    def get_logical_index_for_electrode(self, address, ele):
        """
        Return logical index for a given electrode (address, pin).
        Works for electrodes, electrodes_col, electrodes_row.
        """
        idx_inside = None

        if self.electrodes:
            # electrodes is a flat list of tuples (addr, pin)
            try:
                idx_inside = self.electrodes.index((address, ele))
            except ValueError:
                return None

            # calculate row/col inside the interface grid
            local_row = idx_inside // self.num_cols
            local_col = idx_inside % self.num_cols

        elif self.electrodes_col:
            # electrodes_col is a list of (addr, pin)
            try:
                idx_inside = self.electrodes_col.index((address, ele))
            except ValueError:
                return None

            # row = 0 (single row per column), col = idx_inside
            local_row = 0
            local_col = idx_inside

        elif self.electrodes_row:
            # electrodes_row is a list of (addr, pin)
            try:
                idx_inside = self.electrodes_row.index((address, ele))
            except ValueError:
                return None

            # row = idx_inside, col = 0
            local_row = idx_inside
            local_col = 0

        else:
            # no electrodes defined
            return None

        # return logical index via parent method
        return self.logical_index(local_col, local_row)

    def get_logical_index_for_electrode_pair(self, address, ele1, ele2):
        """
        Resolve logical index from two active electrodes (matrix mode).
        One must belong to rows, one to columns.
        """

        if not self.electrodes_row or not self.electrodes_col:
            return None

        pair1 = (address, ele1)
        pair2 = (address, ele2)

        # Determine which is row and which is column
        if pair1 in self.electrodes_row and pair2 in self.electrodes_col:
            local_row = self.electrodes_row.index(pair1)
            local_col = self.electrodes_col.index(pair2)

        elif pair2 in self.electrodes_row and pair1 in self.electrodes_col:
            local_row = self.electrodes_row.index(pair2)
            local_col = self.electrodes_col.index(pair1)

        else:
            # Not a valid row/col combination
            return None

        return self.logical_index(local_col, local_row)

    def process(self, address, values: dict):
        """
        Process electrode values and return key events.
        Threshold-based detection: values > 0 are considered active.
        Returns list of (logical_index, is_pressed) tuples.
        """
        THRESHOLD = 10  # Threshold for active electrode

        print(f"values: {values}")

        # Determine active electrodes based on threshold
        current_active = {ele for ele, value in values.items() if value > THRESHOLD}
        print(f"current_active: {current_active}")

        events = []

        if self.use2electrodes:
            prev_key = self._last_active.get(address)
            current_key = None

            if len(current_active) == 2:
                ele1, ele2 = tuple(current_active)
                current_key = self.get_logical_index_for_electrode_pair(
                    address, ele1, ele2
                )

            # Store new key state
            self._last_active[address] = current_key

            # If key changed
            if prev_key != current_key:

                # Release old key
                if prev_key is not None:
                    events.append((prev_key, False))
                    print(
                        f"{Ansi256.SKY}Logical key {Ansi256.PEACH}{prev_key} released{Ansi.RESET}"
                    )

                # Press new key
                if current_key is not None:
                    events.append((current_key, True))
                    print(
                        f"{Ansi256.SKY}Logical key {Ansi256.PEACH}{current_key} pressed{Ansi.RESET}"
                    )
        else:
            for ele in pressed:
                logical_index = self.get_logical_index_for_electrode(address, ele)
                if logical_index is not None:
                    events.append((logical_index, True))
                    print(
                        f"{Ansi256.SKY}Logical key {Ansi256.PEACH}{logical_index} pressed{Ansi.RESET}"
                    )

            for ele in released:
                logical_index = self.get_logical_index_for_electrode(address, ele)
                if logical_index is not None:
                    events.append((logical_index, False))
                    print(
                        f"{Ansi256.SKY}Logical key {Ansi256.PEACH}{logical_index} released{Ansi.RESET}"
                    )

        return events

    def is_connected(self):
        pass  # Not needed

    def reconnect(self):
        pass  # Not needed

    def receive(self, verbose=False):
        pass  # Not needed

    def send(self, msg_type: str, data: dict, verbose=False):
        pass  # Not needed
