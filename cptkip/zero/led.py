import cptkip.config.configuration as config
from cptkip.device.led import Led
from cptkip.pin.pwm_pin import PwmPin


def create_led_pin(pin=None, invert=None) -> PwmPin:
    """
    Simple utility function to make it easy to create the LED Pin object.
    If no pin is specified, it defaults to the config value LED_PIN and invert is LED_INVERT.
    """
    return PwmPin(pin or config.LED_PIN, invert=invert or config.LED_INVERT)


def create_led(pin=None, invert=None) -> Led:
    """
    Simple utility function to make it easy to create a LED based on configuration.
    If no pin is specified, it defaults to the config value LED_PIN.
    """
    return Led(create_led_pin(pin, invert))


def stop_animation(animation):
    """
    Simple utility function to make it easy to turn off LED animations.

    :param animation: An Animation or AnimationSequence from adafruit_led_animation.
    """
    # Imported here rather than at module level so that using only the create_*
    # helpers does not load adafruit_led_animation.
    from adafruit_led_animation.sequence import AnimationSequence

    animation.freeze()
    if isinstance(animation, AnimationSequence):
        animation = animation.current_animation

    stop_led(animation.pixel_object)


def stop_led(led: Led):
    """
    Simple utility function to make it easy to turn off an LED.
    """
    led.off()
    led.show()
