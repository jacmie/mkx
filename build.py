import os
import shutil
import subprocess

MPY_CROSS = shutil.which("mpy-cross")
MPY_TARGET_DIR = ".compiled"
SOURCE_DIRS = ["mkx", "keymap.py"]
MOUNTPOINT = "/media/{}/CIRCUITPY".format(os.getenv("USER"))

if not MPY_CROSS:
    print("Error: mpy-cross not found. Install it first.")
    exit(1)


def compile():
    print("==> Compiling .py to .mpy")
    os.makedirs(MPY_TARGET_DIR, exist_ok=True)
    for dir in SOURCE_DIRS:
        for root, _, files in os.walk(dir):
            for file in files:
                if file.endswith(".py"):
                    src_path = os.path.join(root, file)
                    dst_path = os.path.join(MPY_TARGET_DIR, src_path)
                    os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                    subprocess.run([MPY_CROSS, "-O2", src_path, "-o", dst_path])


def upload():
    compile()
    if os.path.exists(MOUNTPOINT):
        print(f"==> Uploading to {MOUNTPOINT}")
        subprocess.run(["rsync", "-r", MPY_TARGET_DIR + "/", MOUNTPOINT])
    else:
        print("Error: CIRCUITPY drive not found.")


def clean():
    print("==> Cleaning up compiled files")
    shutil.rmtree(MPY_TARGET_DIR, ignore_errors=True)


if __name__ == "__main__":
    import sys

    actions = {"compile": compile, "upload": upload, "clean": clean}
    if len(sys.argv) < 2 or sys.argv[1] not in actions:
        print("Usage: python build.py {compile|upload|clean}")
    else:
        actions[sys.argv[1]]()
