class InterfahceAbstract:
    def __init__(self, device_id, col_min, row_min, col_max, row_max):
        self.device_id = device_id
        self.buffer = b""

        self.col_min = col_min
        self.row_min = row_min
        self.col_max = col_max
        self.row_max = row_max

        self.num_rows = abs(self.row_max - self.row_min) + 1
        self.num_cols = abs(self.col_max - self.col_min) + 1

        self._coord_map = []

    def set_coord_map(self, coord_list):
        expected = self.num_rows * self.num_cols

        if len(coord_list) != expected:
            raise ValueError(
                "coord_list length {} does not match {}".format(
                    len(coord_list), expected
                )
            )
        self._coord_map = coord_list

    def logical_index(self, local_col, local_row):
        idx_inside = self.num_cols * local_row + local_col
        try:
            return self._coord_map[idx_inside]
        except IndexError:
            raise IndexError(
                "Local coord ({},{}) outside interface bounds".format(
                    local_row, local_col
                )
            )

    # ---------- internal helpers --------------------------------

    def generate_rect_map(self, keymap_col_size):
        row_range = (
            range(self.row_min, self.row_max + 1)
            if self.row_min <= self.row_max
            else range(self.row_min, self.row_max - 1, -1)
        )
        col_range = (
            range(self.col_min, self.col_max + 1)
            if self.col_min <= self.col_max
            else range(self.col_min, self.col_max - 1, -1)
        )

        for r in row_range:
            for c in col_range:
                self._coord_map.append(r * keymap_col_size + c)

    def is_connected(self) -> bool:
        raise NotImplementedError(
            "Subclass of the InterfahceAbstract must implement is_connected()"
        )

    def reconnect(self):
        raise NotImplementedError(
            "Subclass of the InterfahceAbstract must implement reconnect()"
        )

    def receive(self, verbose=False) -> list[dict]:
        raise NotImplementedError(
            "Subclass of the InterfahceAbstract must implement receive()"
        )

    def send(self, msg_type: str, data: dict, verbose=False):
        raise NotImplementedError(
            "Subclass of the InterfahceAbstract must implement send()"
        )

    def ensure_connection(self) -> bool:
        if not self.is_connected():
            # print("Not connected, attempting to reconnect...")
            self.reconnect()
            if not self.is_connected():
                print("Reconnection failed.")
                return False
        return True
