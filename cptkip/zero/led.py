from adafruit_led_animation.animation import Animation
from adafruit_led_animation.sequence import AnimationSequence

import cptkip.config.configuration as config
from cptkip.device.led import Led
from cptkip.pin.pwm_pin import PwmPin


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


def stop_animation(animation: Animation | AnimationSequence):
    """
    Simple utility function to make it easy to turn off LED animations.
    """
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
