from mkx.periphery_abstract import PeripheryAbstract

import digitalio

import adafruit_mpr121


class PeripheryTouch:
    def __init__(self, i2c, address=0x5B, irq_pin=None):
        self.address = address
        self.mpr121 = adafruit_mpr121.MPR121(i2c, address)
        self.irq_pin = None
        self.use2electrodes = None

        if irq_pin is not None:
            self.irq_pin = digitalio.DigitalInOut(irq_pin)
            self.irq_pin.direction = digitalio.Direction.INPUT
            self.irq_pin.pull = digitalio.Pull.UP

    def fire_only_on_2electrodes(self, enable):
        self.use2electrodes = enable

    def _get_two_active_electrodes(self, touch_bits):
        # Clear the lowest active bit
        x = touch_bits & (touch_bits - 1)

        # Check if original number had exactly two bits set
        if x and (x & (x - 1)) == 0:
            # Extract first (lowest) active bit
            first = (touch_bits & -touch_bits).bit_length() - 1
            # Extract second active bit
            second = (x & -x).bit_length() - 1

            return first, second

        return None

    def touched_electrodes(self):
        # If irq_pin==None pin is used then always read,
        # otherwise only read when irq pin value is LOW (active)
        if self.irq_pin is None or not self.irq_pin.value:
            touch_bits = self.mpr121.touched()

            if self.use2electrodes:
                active = self._get_two_active_electrodes(touch_bits)
                if active is not None:
                    print(f"Two active electrodes: {active}")
                    return (self.address, active)
                return None
            else:
                active = tuple(i for i in range(12) if touch_bits & (1 << i))

                if active:
                    print("Touched electrodes:", active)
                    return (self.address, active)

                return None

        return None

        # if self.irq_pin is None or not self.irq_pin.value:
        #     touch_bits = self.mpr121.touched()

        #     if self.use2electrodes:
        #         active_electrodes = self._get_two_active_electrodes(touch_bits)
        #         if active_electrodes is not None:
        #             print(
        #                 f"Two active electrodes: {active_electrodes[0]}, {active_electrodes[1]}"
        #             )
        #             return active_electrodes
        #         else:
        #             return []
        #     else:
        #         touched = [i for i in range(12) if touch_bits & (1 << i)]
        #         print("Touched electrodes:", touched)
        #         return touched

        # return []
