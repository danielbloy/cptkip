import cptkip.config.configuration as config
import cptkip.core.environment as environment
from cptkip.device.led import Led
from cptkip.pin.pwm_pin import PwmPin

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    pass


def create_led_pin() -> PwmPin:
    """
    Simple utility function to make it easy to create the LED Pin object.
    """
    return PwmPin(config.LED_PIN, invert=config.LED_INVERT)


def create_led() -> Led:
    """
    Simple utility function to make it easy to create a LED based on configuration.
    """
    return Led(create_led_pin())
