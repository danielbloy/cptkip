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
