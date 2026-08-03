import cptkip.config.configuration as config
import cptkip.core.environment as environment
from cptkip.device.buzzer import Buzzer
from cptkip.pin.buzzer_pin import BuzzerPin

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    pass


def create_buzzer() -> Buzzer:
    """
    Simple utility function to make it easy to create a buzzer based on configuration.
    """
    pin = BuzzerPin(config.BUZZER_PIN)
    return Buzzer(pin)
