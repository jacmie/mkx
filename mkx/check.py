def check(total_cols, total_rows, keymap, interfaces):
    print(f"\n=== KEYMAP-CHECK (layer 0) ===")

    errors = False

    for iface in interfaces:
        name = getattr(iface, "device_id", "unknown")
        iface.generate_rect_map(total_cols)

        # --- Bounds check ---
        for dim, val, limit in [
            ("row_min", iface.row_min, total_rows),
            ("row_max", iface.row_max, total_rows),
            ("col_min", iface.col_min, total_cols),
            ("col_max", iface.col_max, total_cols),
        ]:
            if not (0 <= val < limit):
                print(f"[ERROR] {name}: {dim}={val} out of bounds 0-{limit-1}")
                errors = True

            # coordinate map presence
            coord_map = getattr(iface, "_coord_map", None)
            if coord_map is None:
                print(f"[ERROR] {name}: no coordinate map set")
                errors = True
                continue

        # --- Coordinate‑map index range check ---
        keymap_size = total_rows * total_cols
        for i, idx in enumerate(coord_map):
            if not (0 <= idx < keymap_size):
                print(
                    f"[ERROR] {name}: coord_map[{i}]={idx} out of range 0-{keymap_size-1}"
                )
                errors = True

        # --- Build a shadow matrix for visualisation ---
        shadow = [["·" for _ in range(total_cols)] for _ in range(total_rows)]

        for local_i, flat_idx in enumerate(coord_map):
            r, c = divmod(flat_idx, total_cols)
            try:
                key_obj = keymap[0][flat_idx]
            except IndexError:
                key_obj = None

            char = str(key_obj.key_name) if key_obj is not None else "None"
            # shorten long names so grid stays narrow
            char = char[:8]
            shadow[r][c] = char

        # --- Print results ---
        print(
            "\n[{}] covers rows {}-{}, cols {}-{}".format(
                name, iface.row_min, iface.row_max, iface.col_min, iface.col_max
            )
        )

        # pretty‑print shadow
        for r in range(total_rows):
            row_str = "  ".join(f"{cell:>8}" for cell in shadow[r])
            print(row_str)

    return errors
