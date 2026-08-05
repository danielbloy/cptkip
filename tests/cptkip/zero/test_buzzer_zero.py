import cptkip.config.configuration as config
from cptkip.zero.buzzer import create_buzzer_pin, create_buzzer


class TestBuzzerZero:
    """
    The tests in here are trivial. They are not intended to test the functionality
    of the underlying pins or devices, just that the `cptkip.zero.buzzer` module
    constructs them correctly.
    """

    def test_create_buzzer_pin(self):
        """
        Validates that a buzzer pin is created "properly".
        """
        pin = create_buzzer_pin()
        assert pin
        assert pin.pin == config.BUZZER_PIN == "buzzer_pin"

    def test_create_buzzer(self):
        """
        Validates that a buzzer is created "properly".
        """
        buzzer = create_buzzer()
        assert buzzer
        assert buzzer._buzzer.pin == config.BUZZER_PIN == "buzzer_pin"
