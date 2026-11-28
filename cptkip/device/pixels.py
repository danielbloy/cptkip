import cptkip.core.environment as environment

OFF = (0, 0, 0)

if environment.are_pins_available():
    # noinspection PyPackageRequirements
    from neopixel import NeoPixel as Pixels

else:

    class Pixels:
        """
        Desktop stand-in for neopixel.NeoPixel. It keeps the colour of each pixel so
        that animations, examples and tests can be checked without hardware. Colours
        are stored as given (brightness is not applied), as RGB tuples.
        """

        def __init__(self, pin, num_pixels: int, brightness: float,
                     auto_write: bool = True) -> None:
            self.pin = pin
            self.num_pixels = num_pixels
            self.brightness = brightness
            self.auto_write = auto_write
            self._pixels = [OFF] * num_pixels

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.deinit()

        def deinit(self) -> None:
            pass

        def __len__(self):
            return self.num_pixels

        @property
        def n(self) -> int:
            return self.num_pixels

        def write(self) -> None:
            pass

        def show(self):
            pass

        @staticmethod
        def _to_tuple(color) -> tuple:
            if isinstance(color, int):
                return (color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF
            return tuple(color)

        def fill(self, color):
            color = self._to_tuple(color)
            for i in range(self.num_pixels):
                self._pixels[i] = color

        def __setitem__(self, index, val):
            if isinstance(index, slice):
                for i, colour in zip(range(*index.indices(self.num_pixels)), val):
                    self._pixels[i] = self._to_tuple(colour)
            else:
                self._pixels[index] = self._to_tuple(val)

        def __getitem__(self, index):
            return self._pixels[index]


def create(pin, num_pixels: int, brightness: float = 1.0) -> Pixels:
    """
    Returns a new Pixels object that controls a strand of NeoPixels or
    other compatible individually addressable pixel device. This clamps the
    brightness between the values 0.0 and 1.0 as well as setting all pixels
    to off.

    :param pin: The pin connected to the NeoPixels.
    :param num_pixels: The number of pixels in the strand.
    :param brightness: The brightness of the pixels.
    """
    pixels: Pixels = Pixels(pin, num_pixels, brightness=max(min(brightness, 1.0), 0.0),
                            auto_write=False)
    pixels.fill(OFF)
    pixels.write()
    # noinspection PyTypeChecker
    return pixels
