import os
import shutil
import time
from pathlib import Path
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

MOUNTPOINT = f"/media/{os.getenv('USER')}/CIRCUITPY"
SOURCE_DIRS = ["mkx"]  # Add other directories or files as needed

# Dictionary to track modified files
modified_files = set()


class SyncHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.is_directory:
            return
        for source in SOURCE_DIRS:
            src_path = Path(event.src_path).resolve()
            source_path = Path(source).resolve()
            if src_path.is_relative_to(source_path):
                modified_files.add(src_path)


def sync():
    if not os.path.ismount(MOUNTPOINT):
        print("Error: CIRCUITPY drive not found.")
        return

    print(f"==> Syncing to {MOUNTPOINT}")
    for src in list(modified_files):
        try:
            relative_path = src.relative_to(Path.cwd())
            dest = Path(MOUNTPOINT) / "lib" / relative_path
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            print(f"Copied: {src} -> {dest}")
            modified_files.remove(src)
        except Exception as e:
            print(f"Error copying {src}: {e}")
    print("==> Sync complete.")


if __name__ == "__main__":
    event_handler = SyncHandler()
    observer = Observer()
    for source in SOURCE_DIRS:
        observer.schedule(event_handler, path=source, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
            if modified_files:
                sync()
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
