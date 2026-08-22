from cptkip.pin.pwm_pin import PwmPin

try:
    # noinspection PyUnresolvedReferences
    from typing import Sequence

    ColorUnion = int | tuple[int, int, int] | tuple[int, int, int, int]
except ImportError:
    pass


class Led:
    def __init__(self, pin: PwmPin, brightness: float = 1.0, auto_write: bool = True):
        """
        Wraps a pin (PwmPin) in such a way that a simple LED can be used with
        animations (in a very basic way).

        :param pin:        A PwmPin instance to use for the LED.
        :param brightness: A value between 0.0 (off) and 1.0 (on).
        :param auto_write: Whether to automatically update the LED pin or not.
        """
        if pin is None:
            raise ValueError("pin cannot be None")

        if not isinstance(pin, PwmPin):
            raise ValueError("pin must be of type PwmPin")

        self.pin = pin
        self.auto_write = auto_write
        self._brightness = -1.0  # Sets up the initial variable and forces a "change".
        self.brightness = brightness

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deinit()

    def deinit(self) -> None:
        """
        Turns the LED off and releases the underlying pin.
        """
        self.fill(0)
        self.show()
        self.pin.deinit()

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value: float):
        value = min(max(value, 0.0), 1.0)
        change = value - self._brightness
        if -0.0001 < change < 0.0001:
            return

        self._brightness = value

        if self.auto_write:
            self.show()

    def on(self):
        """
        Turns the LED fully on.
        """
        self.brightness = 1.0

    def off(self):
        """
        Turns the LED fully off.
        """
        self.brightness = 0.0

    @property
    def n(self) -> int:
        """
        Number of pixels. Always 1 - present for API compatibility with
        multi-pixel devices such as NeoPixel strands.
        """
        return 1

    def __len__(self):
        return 1

    def show(self) -> None:
        """
        Applies the current brightness to the underlying pin. Called
        automatically by brightness/fill/__setitem__ when auto_write is True.
        """
        self.pin.value = self._brightness

    def fill(self, color: ColorUnion):
        """
        Takes a colour value in one of the forms supported by _parse_color() and
        uses the calculated W value from that colour as the value to set the
        brightness on a scale from 0.0 to 1.0.

        The pin is only changed if auto_write is True.
        """
        r, g, b, w = self._parse_color(color)
        self.brightness = w / 0xFF

    @staticmethod
    def _parse_color(value: ColorUnion) -> tuple[int, int, int, int]:
        """
        Converts the passed in value to a 4 digit RGBW tuple. The value can be
        one of the following:
        * A single integer value representing a packed RGB value of 0x000000 to 0xFFFFFF
        * A tuple of 3 integers representing RGB, each with an expected value of 0 to 0xFF
        * A tuple of 4 integers representing RGBW, each with an expected value of 0 to 0xFF

        The input is validated that it is either a single integer or a tuple
        containing 3 or 4 elements though it does not validate the tuple values
        are integers.

        Similarly, even though the colours are expected to have values between
        0x00 and 0xFF, these are not validated or range checked.

        If a single integer value is specified it is assumed to be a 24-bit integer
        with the highest 8 bits representing the R value, the middle 8 bits representing
        the G value and the lowest 8 bits representing the B value. The W value is
        calculated as the average of the extracted RGB values.

        If 3 colours are specified in a tuple, the average of the RGB values are used for
        the returned W value and the RGB values are returned as-is.

        If 4 colours are specified in a tuple, they are returned as-is.
        """
        if isinstance(value, int):
            r = value >> 16
            g = (value >> 8) & 0xFF
            b = value & 0xFF
            # Average out the RBG intensities.
            w = int((r + g + b) / 3)
            return r, g, b, w

        if value is None or not isinstance(value, tuple):
            raise ValueError("Expected an int or tuple of length 3 or 4")

        if len(value) < 3 or len(value) > 4:
            raise ValueError(
                "Expected tuple of length {}, got {}".format(4, len(value))
            )

        if len(value) == 3:
            r, g, b = value
            # Average out the RBG intensities.
            w = int((r + g + b) / 3)
        else:
            r, g, b, w = value

        return r, g, b, w

    def __setitem__(self, index: int | slice, val: ColorUnion | Sequence[ColorUnion]):
        """
        Equivalent to fill(val) - index/slice is accepted but ignored since
        there is only ever a single logical pixel.
        """
        r, g, b, w = self._parse_color(val)
        self.fill((r, g, b, w))

    def __getitem__(self, index: int | slice):
        """
        Returns the current brightness as a grayscale (val, val, val) tuple.
        This is derived purely from brightness, not the original RGB values
        last passed to fill()/__setitem__ - colour information beyond the
        computed brightness is not retained.
        """
        val = self.brightness * 255
        return val, val, val
