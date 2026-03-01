import board
import busio
import time

from mkx.error import halt_on_error
from mkx.ansi_colors import Ansi, Ansi256


def init_i2c(scl_pin=board.SCL, sda_pin=board.SDA, status_led=None):
    print(f"{Ansi256.MINT}=== Initializing I2C ==={Ansi.RESET}")
    try:
        i2c = busio.I2C(scl_pin, sda_pin)
        print(f"{Ansi256.SKY}✓ I2C bus created\n{Ansi.RESET}")
    except Exception as e:
        halt_on_error(
            f"✗ I2C failed: {e}",
            status_led,
        )

    # Try a few times since I2C can be slow to start
    print(f"{Ansi256.MINT}=== Scanning I2C Bus (3 attempts) ==={Ansi.RESET}")
    devices = []
    for attempt in range(3):
        try:
            while not i2c.try_lock():
                pass
            devices = i2c.scan()
            i2c.unlock()
            if devices:
                break
            print(f"  Attempt {attempt + 1}: No devices")
            time.sleep(0.1)
        except Exception as e:
            print(f"  Attempt {attempt + 1}: Error - {e}")
            time.sleep(0.1)

    if devices:
        print(f"{Ansi256.SKY}✓ Found {len(devices)} device(s) address:{Ansi.RESET}")
        for addr in devices:
            print(f"{Ansi256.PEACH}  - 0x{addr:02X}{Ansi.RESET}")
        print()
        return i2c
    else:
        halt_on_error(
            "✗ No I2C devices found after 3 attempts\nCHECK: I2C wiring, pullup resistors, power",
            status_led,
        )
        return None
