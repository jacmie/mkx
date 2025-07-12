import neopixel

from mkx.backlight_abstract import BacklightAbstract


class BacklightNeopixelRainbow(BacklightAbstract):
    def __init__(self, pin, num_pixels: int, brightness: float = 1):
        self.pixels = neopixel.NeoPixel(
            pin, num_pixels, brightness=brightness, auto_write=False
        )
        self._num_pixels = num_pixels
        self._wheel_pos = 0
        self._wheel_speed = 1
        self._frame_skip = 0
        self._frame_count = 0
        self._swirl = True

    def _wheel(self, pos):
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)  # Red → Green
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)  # Green → Blue
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)  # Blue → Red

    def faster(self, value):
        self._wheel_speed = min(value, 20.0)
        self._frame_skip = 0

    def slower(self, value):
        self._frame_skip = max(value, 0.0)
        self._wheel_speed = 1

    def set_swirl(self, swirl: bool):
        self._swirl = swirl

    def shine(self):
        if self._frame_count < self._frame_skip:
            self._frame_count += 1
            return
        self._frame_count = 0

        if self._swirl:
            for i in range(self._num_pixels):
                pixel_index = (i * 256 // self._num_pixels) + self._wheel_pos
                self.pixels[i] = self._wheel(pixel_index & 255)
        else:
            color = self._wheel(self._wheel_pos & 255)
            for i in range(self._num_pixels):
                self.pixels[i] = color

        self.pixels.show()

        self._wheel_pos = (self._wheel_pos + self._wheel_speed) % 256
