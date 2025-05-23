from cptkip.pin.pwm_pin import PwmPin


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
