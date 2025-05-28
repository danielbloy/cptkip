import pytest

from cptkip.device.led import Led
from cptkip.pin.pwm_pin import PwmPin


class MockPwmPin(PwmPin):
    def __init__(self):
        self.value_count = 0
        super().__init__(None)
        self.value_count = 0

    @property
    def value(self):
        return super().value

    @value.setter
    def value(self, value: float):
        self.value_count += 1
        super(MockPwmPin, self.__class__).value.__set__(self, value)


class TestLed:

    def test_constructor(self) -> None:
        """
        Validates that a Led is constructed with the correct parameters
        """
        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Led(None)

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Led(2)

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Led("None")

        # Now make one with auto write on
        pin = MockPwmPin()
        led = Led(pin)
        assert led.brightness == 1.0
        assert led.auto_write
        assert led.n == 1
        assert len(led) == 1
        assert pin.value_count == 1  # Validate it writes
        assert pin.value == 1.0

        # Now make one with auto write off
        pin = MockPwmPin()
        led = Led(pin, auto_write=False)
        assert led.brightness == 1.0
        assert not led.auto_write
        assert led.n == 1
        assert len(led) == 1
        assert pin.value_count == 0  # Validates it does not write
        assert pin.value == 0.0

    def test_deinit_can_be_called_multiple_times(self):
        """
        Validates that deinit() can be called multiple times without issue
        and that it sets the properties correctly.
        """
        # Now make one with auto write on
        pin = MockPwmPin()
        led = Led(pin)
        assert led.auto_write
        assert led.n == 1
        assert len(led) == 1

        assert led.brightness == 1.0
        assert pin.value_count == 1
        assert pin.value == 1.0

        led.deinit()
        assert led.brightness == 0.0
        assert pin.value_count == 3  # Validate it writes
        assert pin.value == 0.0

        led.deinit()
        assert led.brightness == 0.0
        assert pin.value_count == 4  # Validate it writes
        assert pin.value == 0.0

        led.deinit()
        assert led.brightness == 0.0
        assert pin.value_count == 5  # Validate it writes
        assert pin.value == 0.0

        # Now make one with auto write off
        pin = MockPwmPin()
        led = Led(pin, auto_write=False)
        assert not led.auto_write
        assert led.n == 1
        assert len(led) == 1

        assert led.brightness == 1.0
        assert pin.value == 0.0
        pin.value = 1.0
        assert pin.value_count == 1  # Validate it writes

        led.deinit()
        assert led.brightness == 0.0
        assert pin.value_count == 2  # Validate it writes
        assert pin.value == 0.0

        led.deinit()
        assert led.brightness == 0.0
        assert pin.value_count == 3  # Validate it writes
        assert pin.value == 0.0

        led.deinit()
        assert led.brightness == 0.0
        assert pin.value_count == 4  # Validate it writes
        assert pin.value == 0.0

    def test_brightness(self):
        """
        Validates that the brightness property correctly sets the brightness and
        only writes to the pin when auto_write is True.
        """
        # Now make one with auto write on
        pin = MockPwmPin()
        led = Led(pin)
        assert led.auto_write
        assert led.n == 1
        assert len(led) == 1

        assert led.brightness == 1.0
        assert pin.value_count == 1
        assert pin.value == 1.0

        # Write the same value and there should be no change.
        led.brightness = 1.0
        assert led.brightness == 1.0
        assert pin.value_count == 1
        assert pin.value == 1.0

        # Now make a change
        led.brightness = 0.5
        assert led.brightness == 0.5
        assert pin.value_count == 2
        assert pin.value == 0.5

        # Now make one with auto write off
        pin = MockPwmPin()
        led = Led(pin, auto_write=False)
        assert not led.auto_write
        assert led.n == 1
        assert len(led) == 1

        assert led.brightness == 1.0
        assert pin.value_count == 0
        assert pin.value == 0.0

        # Write the same value and there should be no change.
        led.brightness = 1.0
        assert led.brightness == 1.0
        assert pin.value_count == 0
        assert pin.value == 0.0

        # Now make a change; should not write.
        led.brightness = 0.5
        assert led.brightness == 0.5
        assert pin.value_count == 0
        assert pin.value == 0.0

    def test_on_and_off(self):
        """
        Validates that the on() and off() functions correctly sets the brightness and
        only writes to the pin when auto_write is True.
        """
        # Now make one with auto write on
        pin = MockPwmPin()
        led = Led(pin)
        assert led.auto_write
        assert led.n == 1
        assert len(led) == 1

        assert led.brightness == 1.0
        assert pin.value_count == 1
        assert pin.value == 1.0

        led.on()
        assert led.brightness == 1.0
        assert pin.value_count == 1
        assert pin.value == 1.0

        led.off()
        assert led.brightness == 0.0
        assert pin.value_count == 2
        assert pin.value == 0.0

        led.on()
        assert led.brightness == 1.0
        assert pin.value_count == 3
        assert pin.value == 1.0

        # Now make one with auto write off
        pin = MockPwmPin()
        led = Led(pin, auto_write=False)
        assert not led.auto_write
        assert led.n == 1
        assert len(led) == 1

        assert led.brightness == 1.0
        assert pin.value_count == 0
        assert pin.value == 0.0

        led.on()
        assert led.brightness == 1.0
        assert pin.value_count == 0
        assert pin.value == 0.0

        led.off()
        assert led.brightness == 0.0
        assert pin.value_count == 0
        assert pin.value == 0.0

        led.on()
        assert led.brightness == 1.0
        assert pin.value_count == 0
        assert pin.value == 0.0

    def test_show(self):
        """
        Validates that show write to the pin regardless of auto_write.
        """
        # Now make one with auto write on
        pin = MockPwmPin()
        led = Led(pin)
        assert led.auto_write
        assert led.n == 1
        assert len(led) == 1

        assert led.brightness == 1.0
        assert pin.value_count == 1
        assert pin.value == 1.0

        led.show()
        assert led.brightness == 1.0
        assert pin.value_count == 2
        assert pin.value == 1.0

        led.show()
        assert led.brightness == 1.0
        assert pin.value_count == 3
        assert pin.value == 1.0

        # Now make one with auto write off
        pin = MockPwmPin()
        led = Led(pin, auto_write=False)
        assert not led.auto_write
        assert led.n == 1
        assert len(led) == 1

        assert led.brightness == 1.0
        assert pin.value_count == 0
        assert pin.value == 0.0

        led.show()
        assert led.brightness == 1.0
        assert pin.value_count == 1
        assert pin.value == 1.0

        led.show()
        assert led.brightness == 1.0
        assert pin.value_count == 2
        assert pin.value == 1.0

    def test_fill_auto_write(self):
        """
        Validates that fill changes the brightness and writes to the pin with auto_write.
        """
        # Now make one with auto write on
        pin = MockPwmPin()
        led = Led(pin)
        assert led.auto_write
        assert led.n == 1
        assert len(led) == 1

        assert led.brightness == 1.0
        assert pin.value_count == 1
        assert pin.value == 1.0

        # Use the 4-digit colours for simplicity.
        led.fill((0, 0, 0, 0x80))
        assert led.brightness >= 0.495
        assert led.brightness <= 0.505
        assert pin.value_count == 2
        assert pin.value >= 0.495
        assert pin.value <= 0.505

        led.fill((0, 0, 0, 0xFF))
        assert led.brightness == 1.0
        assert pin.value_count == 3
        assert pin.value == 1.0

        # Now make one with auto write off
        pin = MockPwmPin()
        led = Led(pin, auto_write=False)
        assert not led.auto_write
        assert led.n == 1
        assert len(led) == 1

        assert led.brightness == 1.0
        assert pin.value_count == 0
        assert pin.value == 0.0

        led.fill((0, 0, 0, 0x80))
        assert led.brightness >= 0.495
        assert led.brightness <= 0.505
        assert pin.value_count == 0
        assert pin.value == 0.0

        led.fill((0, 0, 0, 0xFF))
        assert led.brightness == 1.0
        assert pin.value_count == 0
        assert pin.value == 0.0

    def test_fill_colours(self):
        """
        Validates fill will accept a colour correctly, there are three methods
        to provide a colour: RGB packed into a 24-bit integer, 3 value triplet and
        4 value triplet. The calculated
        """
        pin = MockPwmPin()
        led = Led(pin)

        # Go for full brightness in the various forms
        led.brightness = 0.0
        led.fill(0xFFFFFF)
        assert led.brightness == 1.0
        assert pin.value == 1.0

        led.brightness = 0.0
        led.fill((0xFF, 0xFF, 0xFF))
        assert led.brightness == 1.0
        assert pin.value == 1.0

        led.brightness = 0.0
        led.fill((0, 0, 0, 0xFF))
        assert led.brightness == 1.0
        assert pin.value == 1.0

        # Go for zero brightness in the various forms.
        led.brightness = 1.0
        led.fill(0)
        assert led.brightness == 0.0
        assert pin.value == 0.0

        led.brightness = 1.0
        led.fill((0, 0, 0))
        assert led.brightness == 0.0
        assert pin.value == 0.0

        led.brightness = 1.0
        led.fill((0, 0, 0, 0))
        assert led.brightness == 0.0
        assert pin.value == 0.0

        # Try something in the middle
        led.brightness = 1.0
        led.fill(0x409050)
        assert led.brightness == 0x60 / 0xFF
        assert pin.value == 0x60 / 0xFF

        led.brightness = 1.0
        led.fill((0x50, 0x40, 0x90))
        assert led.brightness == 0x60 / 0xFF
        assert pin.value == 0x60 / 0xFF

        led.brightness = 1.0
        led.fill((0, 0, 0, 0x60))
        assert led.brightness == 0x60 / 0xFF
        assert pin.value == 0x60 / 0xFF

    def test_parse_colour_errors_with_wrong_types(self):
        """Validates that _parse_colour errors with wrong types."""

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Led._parse_color(None)

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Led._parse_color("None")

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Led._parse_color([1, 2, 3])

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Led._parse_color((1,))

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Led._parse_color((1, 2))

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Led._parse_color((1, 2, 3, 4, 5))

        # This fails with a TypeError because we do maths with a triplet
        with pytest.raises(TypeError):
            # noinspection PyTypeChecker
            Led._parse_color(("1", "2", "3"))

        # Because no maths is done with a quadlet, there is no error.
        r, g, b, w = Led._parse_color(("1", "2", "3", "4"))
        assert r == "1"
        assert g == "2"
        assert b == "3"
        assert w == "4"

    def test_parse_colour_single_integer(self):
        """
        Validates parse_colour works as expected with a sinngle integer.
        """
        r, g, b, w = Led._parse_color(0)
        assert r == 0
        assert g == 0
        assert b == 0
        assert w == 0

        r, g, b, w = Led._parse_color(0xFFFFFF)
        assert r == 0xFF
        assert g == 0xFF
        assert b == 0xFF
        assert w == 0xFF

        r, g, b, w = Led._parse_color(0x102030)
        assert r == 0x10
        assert g == 0x20
        assert b == 0x30
        assert w == 0x20

        r, g, b, w = Led._parse_color(0x409050)
        assert r == 0x40
        assert g == 0x90
        assert b == 0x50
        assert w == 0x60

    def test_parse_colour_rgb_tuple(self):
        """
        Validates parse_colour works as expected with an RGB tuple.
        All this does is average out the values of the RGB value to the
        whiteness.
        """
        r, g, b, w = Led._parse_color((0, 0, 0))
        assert r == 0
        assert g == 0
        assert b == 0
        assert w == 0

        r, g, b, w = Led._parse_color((99, 0, 0))
        assert r == 99
        assert g == 0
        assert b == 0
        assert w == 33

        r, g, b, w = Led._parse_color((0, 99, 0))
        assert r == 0
        assert g == 99
        assert b == 0
        assert w == 33

        r, g, b, w = Led._parse_color((0, 0, 999))
        assert r == 0
        assert g == 0
        assert b == 999
        assert w == 333

        r, g, b, w = Led._parse_color((10, 20, 30))
        assert r == 10
        assert g == 20
        assert b == 30
        assert w == 20

        # Try outside of ranges
        r, g, b, w = Led._parse_color((-10, 10, 999))
        assert r == -10
        assert g == 10
        assert b == 999
        assert w == 333

    def test_parse_colour_rgbw_tuple(self):
        """
        Validates parse_colour works as expected with an RGBW tuple.
        """
        r, g, b, w = Led._parse_color((0x00, 0x10, 0xA0, 0xFF))
        assert r == 0x00
        assert g == 0x10
        assert b == 0xA0
        assert w == 0xFF

        # Try outside of ranges
        r, g, b, w = Led._parse_color((-10, 3.3, 9999, -0.3))
        assert r == -10
        assert g == 3.3
        assert b == 9999
        assert w == -0.3

    def test_get_and_set_item(self):
        """
        Validates the getter and setters work as expected.
        """
        pin = MockPwmPin()
        led = Led(pin)

        # Start with the get()
        led.brightness = 1.0
        assert led[0] == (0xFF, 0xFF, 0xFF)
        assert led[1] == (0xFF, 0xFF, 0xFF)
        assert led[2] == (0xFF, 0xFF, 0xFF)
        assert led[3] == (0xFF, 0xFF, 0xFF)

        led.brightness = 0.0
        assert led[0] == (0, 0, 0)
        assert led[1] == (0, 0, 0)
        assert led[2] == (0, 0, 0)
        assert led[3] == (0, 0, 0)

        led.brightness = 0x80 / 0xFF
        assert led[0] == (0x80, 0x80, 0x80)
        assert led[1] == (0x80, 0x80, 0x80)
        assert led[2] == (0x80, 0x80, 0x80)
        assert led[3] == (0x80, 0x80, 0x80)
