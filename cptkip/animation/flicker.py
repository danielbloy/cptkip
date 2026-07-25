import array
import random

from adafruit_led_animation.animation import Animation


class Flicker(Animation):
    """
    This flickers each neopixel that is "on" (has a brightness > 0). This function
    by default flickers each pixel but is configurable using spacing. The flicker
    sets the brightness of the pixels to a random value between base and (base + flame).
    """

    def __init__(
            self, pixel_object, speed, color, spacing=1, base=150, flame=105, name=None):
        if spacing < 1:
            raise ValueError("spacing must be at least 1")

        size = len(pixel_object)
        self._size = size
        self._spacing = spacing
        self._base = base
        self._flame = flame
        self._red = array.array("B", bytes(size))
        self._green = array.array("B", bytes(size))
        self._blue = array.array("B", bytes(size))
        super().__init__(pixel_object, speed, color, name=name)

    def _set_color(self, color):
        # Overridden so that setting .color (including at construction, via
        # Animation.__init__) actually updates the stored base colour used by
        # draw(). This also routes int/hex colours through the base class's
        # existing int-to-tuple conversion, so set_all() never sees a raw int.
        super()._set_color(color)
        self.set_all(color)

    def get(self, i):
        if i < 0 or i >= self._size:
            raise ValueError(f"Index {i} is out of bounds!")

        # array.array("B", ...) already yields a plain 0-255 int, so no
        # int()/mask needed here - these are the stored base colour, not dimmed.
        return self._red[i], self._green[i], self._blue[i]

    def set(self, i, colour):
        if i < 0 or i >= self._size:
            raise ValueError(f"Index {i} is out of bounds!")

        self._red[i] = colour[0] & 0xFF
        self._green[i] = colour[1] & 0xFF
        self._blue[i] = colour[2] & 0xFF
        self.pixel_object[i] = (self._red[i], self._green[i], self._blue[i])

    def set_all(self, colour):
        for i in range(self._size):
            self.set(i, colour)  # show all colors

    def draw(self):
        for i in range(0, self._size, self._spacing):
            brightness = random.randint(0, self._flame)
            r = min(int(self._red[i] * (self._base + brightness) / 255), 0xFF)  # 8-bit red dimmed to brightness
            g = min(int(self._green[i] * (self._base + brightness) / 255), 0xFF)  # 8-bit green dimmed to brightness
            b = min(int(self._blue[i] * (self._base + brightness) / 255), 0xFF)  # 8-bit blue dimmed to brightness
            self.pixel_object[i] = (r, g, b)

    def __len__(self):
        """
        Number of pixels.
        """
        return self._size

    def __getitem__(self, index: int):
        return self.get(index)

    def __setitem__(self, index: int, colour):
        self.set(index, colour)
