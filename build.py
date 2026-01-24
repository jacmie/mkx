import os
import shutil
import subprocess
import argparse

MPY_CROSS = shutil.which("adafruit-mpy-cross")
MPY_TARGET_DIR = ".compiled"
SOURCE_DIRS = ["mkx"]
# Default mountpoint template; upload() can accept a different drive or full path
DEFAULT_DRIVE_NAME = "CIRCUITPY"
DEFAULT_MOUNTPOINT = "/media/{}/{}".format(os.getenv("USER"), DEFAULT_DRIVE_NAME)

MPY_CROSS_CMD = None
if MPY_CROSS:
    MPY_CROSS_CMD = [MPY_CROSS]
else:
    print(
        "Warning: adafruit circuitpython mpy-cross not found. Install it or add mpy-cross to PATH to enable --compile."
    )


def compile():
    if not MPY_CROSS_CMD:
        print("Error: adafruit circuitpython mpy-cross not found. Install it first.")
        return 1

    print("==> Compiling .py to .mpy")
    os.makedirs(MPY_TARGET_DIR, exist_ok=True)

    # Collect all .py files from SOURCE_DIRS (support files and directories)
    py_files = []
    for entry in SOURCE_DIRS:
        if os.path.isdir(entry):
            for root, _, files in os.walk(entry):
                for f in files:
                    if f.endswith(".py"):
                        py_files.append(os.path.join(root, f))
        elif os.path.isfile(entry) and entry.endswith(".py"):
            py_files.append(entry)

    total = len(py_files)
    if total == 0:
        print("No .py source files found to compile.")
        return 0

    produced_count = 0
    files_to_compile = []
    for src_path in py_files:
        # Preserve directory structure under MPY_TARGET_DIR, but use .mpy extension
        rel = os.path.relpath(src_path)
        dst_path = os.path.join(MPY_TARGET_DIR, rel)
        dst_path_mpy = (
            dst_path[:-3] + ".mpy" if dst_path.endswith(".py") else dst_path + ".mpy"
        )
        os.makedirs(os.path.dirname(dst_path_mpy), exist_ok=True)

        # Only compile if output missing or source is newer than output
        need_compile = True
        if os.path.exists(dst_path_mpy):
            try:
                src_mtime = os.path.getmtime(src_path)
                dst_mtime = os.path.getmtime(dst_path_mpy)
                if src_mtime <= dst_mtime:
                    need_compile = False
            except Exception:
                need_compile = True

        if need_compile:
            files_to_compile.append((src_path, dst_path_mpy))

    if not files_to_compile:
        print("==> All files are up-to-date.")
        return 0

    for idx, (src_path, dst_path_mpy) in enumerate(files_to_compile, 1):
        try:
            proc = subprocess.run(
                MPY_CROSS_CMD + ["-O2", src_path, "-o", dst_path_mpy],
                capture_output=True,
                text=True,
            )
        except Exception as e:
            print(f"Error running mpy-cross for {src_path}: {e}")
            continue

        if proc.stdout:
            print(f"mpy-cross stdout:\n{proc.stdout}")
        if proc.stderr:
            print(f"mpy-cross stderr:\n{proc.stderr}")
        if proc.returncode != 0:
            print(f"mpy-cross failed for {src_path} (exit {proc.returncode})")
            # do not stop compilation for other files
            continue

        if os.path.exists(dst_path_mpy):
            produced_count += 1
            print(
                f"Compiled [{idx:>{len(str(len(files_to_compile)))}}/{len(files_to_compile)}]  {dst_path_mpy}"
            )
        else:
            print(
                f"Warning: expected output not found for [{idx}/{len(files_to_compile)}]: {dst_path_mpy}"
            )

    return 0


def upload(mountpoint=None, compile_before=False):
    """Upload compiled .mpy files to the given mountpoint.

    If compile_before is True, attempt to compile first.
    """
    if compile_before:
        status = compile()
        if status != 0:
            print("Compilation failed or mpy-cross missing; aborting upload.")
            return

    if not mountpoint:
        mountpoint = DEFAULT_MOUNTPOINT

    if os.path.exists(mountpoint):
        target_dir = os.path.join(mountpoint, "lib")
        print(f"==> Uploading to {target_dir}")

        # Collect all files to upload
        files_to_upload = []
        for root, _, files in os.walk(MPY_TARGET_DIR):
            for f in files:
                src_file = os.path.join(root, f)
                rel_path = os.path.relpath(src_file, MPY_TARGET_DIR)
                files_to_upload.append(rel_path)

        # List files being uploaded
        for idx, rel_path in enumerate(files_to_upload, 1):
            print(
                f"Uploading [{idx:>{len(str(len(files_to_upload)))}}/{len(files_to_upload)}]  {rel_path}"
            )

        subprocess.run(["rsync", "-r", MPY_TARGET_DIR + "/", target_dir + "/"])
    else:
        print(f"Error: drive not found at {mountpoint}.")


def clean():
    print("==> Cleaning up compiled files")
    shutil.rmtree(MPY_TARGET_DIR, ignore_errors=True)


def tidy(mountpoint=None):
    """Remove all uploaded content from the MCU mountpoint."""
    if not mountpoint:
        mountpoint = DEFAULT_MOUNTPOINT

    if not os.path.exists(mountpoint):
        print(f"Error: drive not found at {mountpoint}.")
        return

    mpy_dir = os.path.join(mountpoint, "lib", "mkx")
    if os.path.isdir(mpy_dir):
        print(f"==> Removing all content from {mpy_dir}")
        shutil.rmtree(mpy_dir, ignore_errors=True)
        print(f"==> Tidied {mpy_dir}")
    else:
        print(f"No files found at {mpy_dir}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Compile/upload mkx to a CIRCUITPY device."
    )
    parser.add_argument(
        "-d",
        "--drive",
        default=DEFAULT_DRIVE_NAME,
        help="Name of the mounted drive (default: CIRCUITPY) or full mount path",
    )
    parser.add_argument(
        "--compile",
        action="store_true",
        help="Compile .py files to .mpy (use with --upload to compile before upload)",
    )
    parser.add_argument(
        "--upload",
        action="store_true",
        help="Upload compiled .mpy files to the drive (does not compile unless --compile given)",
    )
    parser.add_argument(
        "--clean", action="store_true", help="Remove compiled files (.compiled)"
    )
    parser.add_argument(
        "--tidy",
        action="store_true",
        help="Removing all content from the mkx dir on the MCU mountpoint",
    )

    args = parser.parse_args()

    if args.tidy:
        drive_arg = args.drive
        if drive_arg.startswith("/"):
            target = drive_arg
        else:
            target = f"/media/{os.getenv('USER')}/{drive_arg}"

        tidy(mountpoint=target)

    if args.clean:
        clean()

    if args.compile and not args.upload:
        compile()

    if args.upload:
        drive_arg = args.drive
        if drive_arg.startswith("/"):
            target = drive_arg
        else:
            target = f"/media/{os.getenv('USER')}/{drive_arg}"

        upload(mountpoint=target, compile_before=args.compile)
