import pytest

import cptkip.core.environment as environment
import cptkip.pin.pwm_pin as pwm_pin
from cptkip.pin.pwm_pin import PwmPin
from tests.cptkip.utilities import FakePwmio


class TestPwmPin:

    def test_default_construction(self):
        """
        Construct a new PwmPin with default values and validate it has the correct values.
        """
        pin = PwmPin(4)

        assert pin.pin == 4
        assert pin.value == 0.0
        assert not pin.invert

    def test_construction(self):
        """
        Construct a new PwmPin with specified values and validate it has the correct values.
        """
        pin = PwmPin(5, value=0.7, invert=True)

        assert pin.pin == 5
        assert pin.value == 0.7
        assert pin.invert

    def test_multiple_deinit(self):
        """
        Call deinit() multiple times without error.
        """
        pin = PwmPin(3)
        pin.deinit()
        pin.deinit()
        pin.deinit()

    def test_with_resources(self):
        """
        Validates that a pin can be used in a with statement.
        """

        with PwmPin(4) as pin:
            assert pin.pin == 4
            assert pin.value == 0.0
            assert not pin.invert

    def test_on_off(self):
        """
        Call on() and off() multiple times, ensuring it sets the correct value.
        """
        for pin in [PwmPin(3), PwmPin(4, invert=True)]:
            assert pin.value == 0.0

            pin.off()
            assert pin.value == 0.0

            pin.on()
            assert pin.value == 1.0

            pin.on()
            assert pin.value == 1.0

            pin.off()
            assert pin.value == 0.0

    def test_value(self):
        """
        Call value multiple times, ensuring it sets the correct value.
        """
        for pin in [PwmPin(3), PwmPin(4, invert=True)]:
            assert pin.value == 0.0

            pin.value = 0.0
            assert pin.value == 0.0

            pin.value = 1.0
            assert pin.value == 1.0

            pin.value = 1.0
            assert pin.value == 1.0

            pin.value = 0.2
            assert pin.value == 0.2

            pin.value = 0.0
            assert pin.value == 0.0

    def test_construction_with_none_pin_raises_when_pins_available(self, monkeypatch):
        """
        The pin-cannot-be-None guard can only be exercised when pins are
        available, which is never true in the desktop/CI test environment
        by default - so it must be forced on via monkeypatching to cover it.
        """
        monkeypatch.setattr(environment, "are_pins_available", lambda: True)
        with pytest.raises(ValueError):
            PwmPin(None)

    def test_deinit_twice_with_pins_available(self, monkeypatch):
        """
        deinit() must be safe to call more than once when real pins are in use
        (e.g. an explicit deinit() followed by a context manager exit). The
        hardware module is faked so the "pins available" path runs on a desktop.
        """
        monkeypatch.setattr(environment, "are_pins_available", lambda: True)
        monkeypatch.setattr(pwm_pin, "pwmio", FakePwmio(), raising=False)

        with PwmPin("GP1") as pin:
            hardware = pin._pwm
            pin.deinit()
            pin.deinit()

        assert hardware.deinit_count == 1
        assert pin._pwm is None
