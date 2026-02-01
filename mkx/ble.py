import time

import adafruit_ble
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.standard.hid import HIDService
from adafruit_ble.services.standard.device_info import DeviceInfoService


class BLE:
    def __init__(
        self,
        name="MKX keyboard",
        manufacturer="MKX",
        model="MKX",
        software_revision="1.0.0",
        appearance=961,
    ):
        self.name = name
        self.appearance = appearance

        self.ble = None
        self.hid = None
        self.device_info = None
        self.advertisement = None

        self.manufacturer = manufacturer
        self.model = model
        self.software_revision = software_revision

    def init(self):
        """Initialize BLE stack and start advertising if needed."""
        self.ble = adafruit_ble.BLERadio()

        # Services auto-register on creation
        self.hid = HIDService()
        self.device_info = DeviceInfoService(
            manufacturer=self.manufacturer,
            model_number=self.model,
            software_revision=self.software_revision,
        )

        self.advertisement = ProvideServicesAdvertisement(self.hid)
        self.advertisement.complete_name = self.name
        self.advertisement.appearance = self.appearance

        if not self.ble.connected:
            time.sleep(0.5)
            self.ble.start_advertising(self.advertisement)

    def ensure_advertising(self):
        """Restart advertising if disconnected."""
        if not self.ble.connected and not self.ble.advertising:
            self.ble.start_advertising(self.advertisement)

    @property
    def connected(self):
        return self.ble and self.ble.connected

    @property
    def devices(self):
        """Return HID devices for Keyboard()"""
        return self.hid.devices if self.hid else None
