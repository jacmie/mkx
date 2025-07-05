import digitalio
import microcontroller
import usb_hid
import supervisor


def boot_cfg(
    sense,
    source=None,
    autoreload: bool = True,
    boot_device: int = 0,
    cdc: bool = True,
    consumer_control: bool = True,
    keyboard: bool = True,
    midi: bool = True,
    mouse: bool = True,
    nkro: bool = False,
    pan: bool = False,
    storage: bool = True,
    usb_id: tuple[str, str] = None,
    **kwargs,
) -> bool:
    """
    sense: microcontroller.Pin or digitalio.DigitalInOut
    source: microcontroller.Pin or digitalio.DigitalInOut or None
    """

    if len(kwargs):
        print("unknown option", kwargs)

    if isinstance(sense, microcontroller.Pin):
        sense = digitalio.DigitalInOut(sense)
        sense.direction = digitalio.Direction.INPUT
        sense.pull = digitalio.Pull.UP

    if isinstance(source, microcontroller.Pin):
        source = digitalio.DigitalInOut(source)
        source.direction = digitalio.Direction.OUTPUT
        source.value = False

    # sense pulled low -> skip boot configuration
    if not sense.value:
        return False

    # configure HID devices
    devices = []

    if keyboard:
        if nkro:
            from mkx.device_nkro_keyboard import nkro_keyboard

            devices.append(nkro_keyboard.NKRO_KEYBOARD)
        else:
            devices.append(usb_hid.Device.KEYBOARD)

    if mouse:
        if pan:
            from mkx.device_pointer import pointer

            devices.append(pointer.POINTER)
        else:
            devices.append(usb_hid.Device.MOUSE)

    if consumer_control:
        devices.append(usb_hid.Device.CONSUMER_CONTROL)

    if devices:
        usb_hid.enable(devices, boot_device)
    else:
        usb_hid.disable()

    # configure midi over usb
    if not midi:
        import usb_midi

        usb_midi.disable()

    # configure usb vendor and product id
    if usb_id is not None:
        if hasattr(supervisor, "set_usb_identification"):
            supervisor.set_usb_identification(*usb_id)

    # Entries for cdc (REPL) and storage are intentionally evaluated last to
    # ensure the board is debuggable, mountable and rescueable, in case any of
    # the previous code throws an exception.
    if not cdc:
        import usb_cdc

        usb_cdc.disable()

    if not storage:
        import storage

        storage.disable_usb_drive()

    if not autoreload:
        supervisor.disable_autoreload()

    return True
