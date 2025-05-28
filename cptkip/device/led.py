import cptkip.core.environment as environment
from cptkip.pin.pwm_pin import PwmPin

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    pass

try:
    # noinspection PyUnresolvedReferences
    from typing import Optional, Tuple, Union, Sequence

    ColorUnion = Union[int, Tuple[int, int, int], Tuple[int, int, int, int]]
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

    def deinit(self) -> None:
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
        if -0.001 < change < 0.001:
            return

        self._brightness = value

        if self.auto_write:
            self.show()

    # Turns the LED fully on.
    def on(self):
        self.brightness = 1.0

    # Turns the LED fully off.
    def off(self):
        self.brightness = 0.0

    @property
    def n(self) -> int:
        return 1

    def __len__(self):
        return 1

    def show(self) -> None:
        self.pin.value = self._brightness

    def fill(self, color: ColorUnion):
        r, g, b, w = self._parse_color(color)
        self.brightness = w / 0xFF

    @staticmethod
    def _parse_color(value: ColorUnion) -> Tuple[int, int, int, int]:
        """
        Converts the passed in value to a 4 digit RGBW tuple. The value can be
        one of the following:
        * A single integer value of 0 to 0xFF
        * A tuple of 3 integers representing RGB, each with a value of 0 to 0xFF
        * A tuple of 4 integers representing RGBW, each with a value of 0 to 0xFF

        The input is validated that it is either a single integer or a tuple
        containing 3 or 4 elements but it does not validate the tuple values
        are integers.

        Similarly, even though the colours are expected to have values between
        0x00 and 0xFF, these are not validated or range checked.

        If a single integer value is specified...
        If 3 colours are specified, the average of the RGB values is used for the 4th value
        If 4 colours are specified, they are returned as-is
        """
        if isinstance(value, int):
            r = value >> 16
            g = (value >> 8) & 0xFF
            b = value & 0xFF
            # Average out the RBG intensities.
            w = (r + g + b) / 3
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
            w = (r + g + b) / 3
        else:
            r, g, b, w = value

        return r, g, b, w

    def __setitem__(self, index: Union[int, slice], val: Union[ColorUnion, Sequence[ColorUnion]]):
        if isinstance(index, slice):
            val = val[0]

        r, g, b, w = self._parse_color(val)
        self.fill((r, g, b, w))

    def __getitem__(self, index: Union[int, slice]):
        val = self.brightness * 255
        return val, val, val
