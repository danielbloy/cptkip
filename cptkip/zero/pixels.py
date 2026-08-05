from adafruit_led_animation.animation import Animation
from adafruit_led_animation.sequence import AnimationSequence

import cptkip.config.configuration as config
import cptkip.core.environment as environment
from cptkip.device.pixels import OFF
from cptkip.device.pixels import create, Pixels

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    pass


def create_pixels(brightness: float = 1.0) -> Pixels:
    """
    Simple wrapper to create Pixels based on the configuration values.
    """
    return create(config.PIXELS_PIN, config.PIXELS_COUNT, brightness=brightness)


# TODO: Comment and test
def stop_animation(animation: Animation | AnimationSequence):
    animation.freeze()
    if isinstance(animation, AnimationSequence):
        animation = animation.current_animation
        
    stop_pixels(animation.pixel_object)


# TODO: Comment and test
def stop_pixels(pixels: Pixels):
    pixels.fill(OFF)
    pixels.write()
