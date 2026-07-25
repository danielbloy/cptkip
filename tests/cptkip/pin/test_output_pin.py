import pytest

import cptkip.core.environment as environment
from cptkip.pin.output_pin import OutputPin


class TestOutputPin:

    def test_default_construction(self):
        """
        Construct a new OutputPin with default values and validate it has the correct values.
        """
        pin = OutputPin(3)

        assert pin.pin == 3
        assert not pin.value
        assert not pin.invert

    def test_construction(self):
        """
        Construct a new OutputPin with specified values and validate it has the correct values.
        """
        pin = OutputPin(4, value=True)

        assert pin.pin == 4
        assert pin.value
        assert not pin.invert

    def test_construction2(self):
        """
        Construct a new OutputPin with specified values and validate it has the correct values.
        """
        pin = OutputPin(5, invert=True)

        assert pin.pin == 5
        assert not pin.value
        assert pin.invert

    def test_multiple_deinit(self):
        """
        Call deinit() multiple times without error.
        """
        pin = OutputPin(3)
        pin.deinit()
        pin.deinit()
        pin.deinit()

    def test_on_off(self):
        """
        Call on() and off() multiple times, ensuring it sets the correct value.
        """
        for pin in [OutputPin(3), OutputPin(4, invert=True)]:
            assert not pin.value

            pin.off()
            assert not pin.value

            pin.on()
            assert pin.value

            pin.on()
            assert pin.value

            pin.off()
            assert not pin.value

    def test_value(self):
        """
        Call value multiple times, ensuring it sets the correct value.
        """
        for pin in [OutputPin(3), OutputPin(4, invert=True)]:
            assert not pin.value

            pin.value = False
            assert not pin.value

            pin.value = True
            assert pin.value

            pin.value = True
            assert pin.value

            pin.value = False
            assert not pin.value

    def test_construction_with_none_pin_raises_when_pins_available(self, monkeypatch):
        """
        The pin-cannot-be-None guard can only be exercised when pins are
        available, which is never true in the desktop/CI test environment
        by default - so it must be forced on via monkeypatching to cover it.
        """
        monkeypatch.setattr(environment, "are_pins_available", lambda: True)
        with pytest.raises(ValueError):
            OutputPin(None)
