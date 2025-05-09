import os, sys
import difflib
import shutil
import time
import argparse
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

PROJECT_DIR = Path(__file__).parent
SOURCE_DIRS = [PROJECT_DIR / "mkx"]  # Add more if needed

modified_files = set()


class SyncHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        for source in SOURCE_DIRS:
            src_path = Path(event.src_path).resolve()
            source_path = source.resolve()

            # Now comparing relative paths
            if src_path.is_relative_to(source_path):
                modified_files.add(src_path)


def list_py_files(directory):
    return {f for f in os.listdir(directory) if f.endswith(".py")}


def read_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.readlines()


def compare_files(verbose, dir1, dir2):
    files1 = list_py_files(dir1)
    files2 = list_py_files(dir2)

    common = files1 & files2
    only_in_dir1 = files1 - files2
    only_in_dir2 = files2 - files1

    if only_in_dir1:
        print(f"Files only in {dir1}:\n", "\n".join(only_in_dir1))

    if only_in_dir2:
        print(f"Files only in {dir2}:\n", "\n".join(only_in_dir2))

    for file in common:
        file1 = os.path.join(dir1, file)
        file2 = os.path.join(dir2, file)
        lines1 = read_file(file1)
        lines2 = read_file(file2)

        diff = list(difflib.unified_diff(lines1, lines2, fromfile=file1, tofile=file2))
        if diff:
            print(f"Differences in {file}")
            if verbose:
                print("".join(diff))


def copy_if_needed(src_path, mountpoint, dry_run=False):
    # Convert the source path to a relative path from the project directory
    relative_path = src_path.relative_to(PROJECT_DIR)

    dest = Path(mountpoint) / "lib" / relative_path
    dest.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy2(src_path, dest)
        print(f"Copied: {src_path} -> {dest}")
    except Exception as e:
        print(f"Error copying {src_path}: {e}")


def initial_sync(mountpoint):
    if not os.path.ismount(mountpoint):
        print(f"Error: {mountpoint} drive not found.")
        sys.exit(1)

    print(f"==> Performing initial sync to {mountpoint}")
    for source in SOURCE_DIRS:
        for root, _, files in os.walk(source):
            for name in files:
                src_path = Path(root) / name
                copy_if_needed(src_path, mountpoint)
    print("==> Initial sync complete.")


def sync(mountpoint):
    if not os.path.ismount(mountpoint):
        print(f"Error: {mountpoint} drive not found.")
        sys.exit(1)

    print(f"==> Syncing to {mountpoint}")
    for src in list(modified_files):
        copy_if_needed(src, mountpoint)
        modified_files.discard(src)
    print("==> Sync complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sync mkx local files to a CIRCUITPY-like device."
    )
    parser.add_argument(
        "-d",
        "--drive",
        default="CIRCUITPY",
        help="Name of the mounted drive (default: CIRCUITPY)",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Which files are different and should be updated.",
    )
    parser.add_argument(
        "--Vdiff", action="store_true", help="Verbose differences between files."
    )
    args = parser.parse_args()

    mountpoint = f"/media/{os.getenv('USER')}/{args.drive}"

    if args.diff or args.Vdiff:
        compare_files(args.Vdiff, PROJECT_DIR / "mkx", Path(mountpoint) / "lib/mkx")
        sys.exit(0)

    initial_sync(mountpoint)

    event_handler = SyncHandler()
    observer = Observer()
    for source in SOURCE_DIRS:
        observer.schedule(event_handler, path=source, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
            if modified_files:
                sync(mountpoint)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
