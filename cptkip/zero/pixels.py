import cptkip.config.configuration as config
import cptkip.core.environment as environment
from cptkip.device.pixels import create, Pixels

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    pass


def create_pixels(brightness: float = 1.0) -> Pixels:
    """
    Simple wrapper to create Pixels based on the config values.
    """
    return create(config.PIXELS_PIN, config.PIXELS_COUNT, brightness=brightness)
