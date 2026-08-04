import cptkip.config.configuration as config
from cptkip.zero.led import create_led_pin, create_led


class TestLedZero:
    """
    The tests in here are trivial. They are not intended to test the functionality
    of the underlying pins or devices, just that the `cptkip.zero.led` module
    constructs them correctly.
    """

    def test_create_led_pin(self):
        """
        Validates that a led pin is created "properly".
        """
        pin = create_led_pin()
        assert pin
        assert pin.pin == config.LED_PIN
        assert pin.invert == config.LED_INVERT

    def test_create_led(self):
        """
        Validates that a led is created "properly".
        """
        led = create_led()
        assert led
