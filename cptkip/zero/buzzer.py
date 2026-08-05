import cptkip.config.configuration as config
from cptkip.device.buzzer import Buzzer
from cptkip.pin.buzzer_pin import BuzzerPin


def create_buzzer_pin() -> BuzzerPin:
    """
    Simple utility function to make it easy to create a BuzzerPin based on configuration.
    """
    return BuzzerPin(config.BUZZER_PIN)


def create_buzzer() -> Buzzer:
    """
    Simple utility function to make it easy to create a Buzzer based on configuration.
    """
    return Buzzer(create_buzzer_pin())
