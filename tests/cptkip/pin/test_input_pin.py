import pytest

import cptkip.core.environment as environment
from cptkip.pin.input_pin import InputPin


class TestInputPin:
    def test_default_construction(self):
        """
        Construct a new InputPin with default values and validate it has the correct values.
        """
        pin = InputPin(3)

        assert pin.pin == 3
        assert pin.pullup

    def test_construction(self):
        """
        Construct a new InputPin with specified values and validate it has the correct values.
        """
        pin = InputPin(4, pullup=False)

        assert pin.pin == 4
        assert not pin.pullup

    def test_multiple_deinit(self):
        """
        Call deinit() multiple times without error.
        """
        pin = InputPin(3)
        pin.deinit()
        pin.deinit()
        pin.deinit()

    def test_value(self):
        """
        Call value multiple times, ensuring it sets the correct value.
        """
        for pin in [InputPin(3), InputPin(4, pullup=False)]:
            assert pin.value == pin.pullup

    def test_value_is_read_only(self):
        """
        InputPin.value must not be settable: an input pin's value is driven
        by whatever is connected to it, not by this code.
        """
        pin = InputPin(3)
        with pytest.raises(AttributeError):
            # noinspection property-access
            pin.value = True

    def test_construction_with_none_pin_raises_when_pins_available(self, monkeypatch):
        """
        The pin-cannot-be-None guard can only be exercised when pins are
        available, which is never true in the desktop/CI test environment
        by default - so it must be forced on via monkeypatching to cover it.
        """
        monkeypatch.setattr(environment, "are_pins_available", lambda: True)
        with pytest.raises(ValueError):
            InputPin(None)
