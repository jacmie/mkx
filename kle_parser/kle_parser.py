import json


def parse_kle_json(kle_layout, matrix_cols):
    coord_mapping = [-1] * (matrix_cols * len(kle_layout))
    keymap_flat = []

    row_idx = 0
    key_index = 0
    for row in kle_layout:
        col_idx = 0
        skip = 0
        for item in row:
            if isinstance(item, dict):
                skip += int(item.get("x", 0))
                continue

            logical_col = col_idx + skip
            matrix_index = row_idx * matrix_cols + logical_col

            if matrix_index >= len(coord_mapping):
                continue  # Skip out-of-bounds

            coord_mapping[matrix_index] = key_index
            keymap_flat.append(item)

            col_idx += 1
            key_index += 1
        row_idx += 1

    return keymap_flat, coord_mapping


with open("sample.json") as f:
    kle_data = json.load(f)

keymap_flat, coord_mapping = parse_kle_json(kle_data, matrix_cols=12)
