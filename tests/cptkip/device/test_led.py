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
        Validates fill will accept a colour correctly
        """
        pass

    def test_parse_colour(self):
        """
        Validates parse_colour works as expected.
        """
        pass

    def test_get_and_set_item(self):
        """
        Validates the getter and setters work as expected.
        """
        pass
