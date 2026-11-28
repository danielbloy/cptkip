import cptkip.config.configuration as config
from cptkip.device.pixels import OFF
from cptkip.device.pixels import create, Pixels


def create_pixels(brightness: float = 1.0, pin=None, count=None) -> Pixels:
    """
    Simple wrapper to create Pixels based on the configuration values.
    If no pin is specified, it defaults to the config value PIXELS_PIN and count to PIXELS_COUNT.
    """
    return create(pin or config.PIXELS_PIN, count or config.PIXELS_COUNT, brightness=brightness)


def stop_animation(animation: "Animation | AnimationSequence"):
    """
    Simple utility function to make it easy to turn off Pixel animations.
    """
    # Imported here rather than at module level so that using only the create_*
    # helpers does not load adafruit_led_animation.
    from adafruit_led_animation.sequence import AnimationSequence

    animation.freeze()
    if isinstance(animation, AnimationSequence):
        animation = animation.current_animation

    stop_pixels(animation.pixel_object)


def stop_pixels(pixels: Pixels):
    """
    Simple utility function to make it easy to turn off Pixels.
    """
    pixels.brightness = 0.0
    pixels.fill(OFF)
    pixels.write()
