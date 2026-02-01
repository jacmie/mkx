import os, sys
import difflib
import shutil
import time
import argparse
import subprocess
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

PROJECT_DIR = Path(__file__).parent
SOURCE_DIRS = [PROJECT_DIR / "mkx"]  # Add more if needed
IGNORED_DIRS = {"__pycache__", ".pytest_cache", ".git", ".compiled"}
IGNORED_FILES = {".covarage", ".DS_Store"}

modified_files = set()


class SyncHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return

        src_path = Path(event.src_path).resolve()

        if any(part in IGNORED_DIRS for part in src_path.parts):
            return

        if src_path.name in IGNORED_FILES:
            return

        for source in SOURCE_DIRS:
            source_path = source.resolve()
            if src_path.is_relative_to(source_path):
                modified_files.add(src_path)


def list_py_files(directory: Path):
    py_files = set()

    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

        for name in files:
            if name in IGNORED_FILES:
                continue
            if name.endswith((".py", ".mpy")):
                py_files.add(name)

    return py_files


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


def copy_if_needed(src_path, mountpoint, use_compiled=False, dry_run=False):
    # Convert the source path to a relative path from the project directory
    relative_path = src_path.relative_to(PROJECT_DIR)

    # If use_compiled is True and src is a .py file, use the .mpy from .compiled instead
    if use_compiled and str(src_path).endswith(".py"):
        compiled_path = PROJECT_DIR / ".compiled" / relative_path
        compiled_path = compiled_path.with_suffix(".mpy")
        if compiled_path.exists():
            src_path = compiled_path
            relative_path = compiled_path.relative_to(PROJECT_DIR / ".compiled")

    dest = Path(mountpoint) / "lib" / relative_path
    dest.parent.mkdir(parents=True, exist_ok=True)

    try:
        shutil.copy2(src_path, dest)
        print(f"Copied: {src_path} -> {dest}")
    except Exception as e:
        print(f"Error copying {src_path}: {e}")


def initial_sync(mountpoint, use_compiled=False):
    if not os.path.ismount(mountpoint):
        print(f"Error: {mountpoint} drive not found.")
        sys.exit(1)

    print(f"==> Performing initial sync to {mountpoint}")
    for source in SOURCE_DIRS:
        for root, dirs, files in os.walk(source):
            dirs[:] = [d for d in dirs if d not in IGNORED_DIRS]

            for name in files:
                if name in IGNORED_FILES:
                    continue
                src_path = Path(root) / name
                copy_if_needed(src_path, mountpoint, use_compiled=use_compiled)
    print("==> Initial sync complete.")


def sync(mountpoint, use_compiled=False):
    if not os.path.ismount(mountpoint):
        print(f"Error: {mountpoint} drive not found.")
        sys.exit(1)

    print(f"==> Syncing to {mountpoint}")
    for src in list(modified_files):
        copy_if_needed(src, mountpoint, use_compiled=use_compiled)
        modified_files.discard(src)
    print("==> Sync complete.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Sync mkx local files to a CIRCUITPY device."
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
    parser.add_argument(
        "--build",
        action="store_true",
        help="Build .mpy binaries using build.py and upload instead of .py files.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Remove compiled files (.compiled directory).",
    )
    parser.add_argument(
        "--tidy",
        action="store_true",
        help="Remove all uploaded content from the MCU mountpoint.",
    )
    args = parser.parse_args()

    mountpoint = f"/media/{os.getenv('USER')}/{args.drive}"

    if args.tidy:
        subprocess.run(
            [
                sys.executable,
                str(PROJECT_DIR / "build.py"),
                "--tidy",
                "--drive",
                args.drive,
            ]
        )
        sys.exit(0)

    if args.clean:
        subprocess.run(
            [
                sys.executable,
                str(PROJECT_DIR / "build.py"),
                "--clean",
            ]
        )
        sys.exit(0)

    if args.diff or args.Vdiff:
        compare_files(args.Vdiff, PROJECT_DIR / "mkx", Path(mountpoint) / "lib/mkx")
        sys.exit(0)

    # If build mode is requested, call build.py compile first and thereafter
    # on changes we'll re-run the compile and sync .mpy files. Otherwise do initial .py sync.
    build_mode = args.build
    build_script = PROJECT_DIR / "build.py"

    if build_mode:
        print("==> Build mode: compiling .mpy binaries")
        subprocess.run(
            [
                sys.executable,
                str(build_script),
                "--compile",
                "--drive",
                args.drive,
            ]
        )
        initial_sync(mountpoint, use_compiled=True)
    else:
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
                # If build mode, compile and sync .mpy files
                if build_mode:
                    print("==> Detected changes — rebuilding .mpy")
                    subprocess.run(
                        [
                            sys.executable,
                            str(build_script),
                            "--compile",
                            "--drive",
                            args.drive,
                        ]
                    )
                    sync(mountpoint, use_compiled=True)
                else:
                    sync(mountpoint)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
