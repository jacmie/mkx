import board
import neopixel

from mkx.backlight_abstract import BacklightAbstract


class BacklightNeopixelStatic(BacklightAbstract):
    def __init__(self, pin, num_pixels, rgb_color=(0, 0, 255), brightness=1):
        self.pixels = neopixel.NeoPixel(
            pin, num_pixels, brightness=brightness, auto_write=False
        )
        self._rgb_color = rgb_color

    def set_rgb_color(self, rgb_color):
        self._rgb_color = rgb_color

    def shine(self):
        self.pixels.fill(self._rgb_color)
        self.pixels.show()
