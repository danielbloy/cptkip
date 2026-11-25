import cptkip.config.configuration as config
from cptkip.device.buzzer import Buzzer
from cptkip.pin.buzzer_pin import BuzzerPin


def create_buzzer_pin(pin=None) -> BuzzerPin:
    """
    Simple utility function to make it easy to create a BuzzerPin based on configuration.
    If no pin is specified, it defaults to the config value BUZZER_PIN.
    """
    return BuzzerPin(pin or config.BUZZER_PIN)


def create_buzzer(pin=None) -> Buzzer:
    """
    Simple utility function to make it easy to create a Buzzer based on configuration.
    If no pin is specified, it defaults to the config value BUZZER_PIN.
    """
    return Buzzer(create_buzzer_pin(pin))
