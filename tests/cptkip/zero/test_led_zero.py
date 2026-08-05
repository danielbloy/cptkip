from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.sequence import AnimationSequence

import cptkip.config.configuration as config
from cptkip.animation.flicker import Flicker
from cptkip.zero.led import create_led_pin, create_led, stop_led, stop_animation


class TestLedZero:
    """
    The tests in here are trivial. They are not intended to test the functionality
    of the underlying pins or devices, just that the `cptkip.zero.led` module
    constructs them correctly.
    """

    def test_create_led_pin(self):
        """
        Validates that a led pin is created "properly".
        """
        pin = create_led_pin()
        assert pin
        assert pin.pin == config.LED_PIN == "led_pin"
        assert pin.invert == config.LED_INVERT == "led_invert"

    def test_create_led(self):
        """
        Validates that a led is created "properly".
        """
        led = create_led()
        assert led
        assert led.pin.pin == config.LED_PIN == "led_pin"
        assert led.pin.invert == config.LED_INVERT == "led_invert"

    def test_stop_pixels(self):
        """
        Validates that a LED object gets stopped (turned off) correctly.
        """
        led = create_led()
        assert led.brightness == 1.0
        assert led.pin.value == 1.0

        stop_led(led)
        assert led.brightness == 0.0
        assert led.pin.value == 0.0

    def test_stop_animation_works(self):
        """
        Validates that stop_animation() works properly.
        """
        led = create_led()
        animation = Flicker(led, speed=0.5, color=(255, 0, 128), base=100, flame=155)

        stop_animation(animation)
        assert animation._paused
        assert led.brightness == 0.0
        assert led.pin.value == 0.0

    def test_stop_animation_works_with_sequence(self):
        """
        Validates that stop_animation() works properly.
        """
        led = create_led()

        animations = [
            Flicker(led, speed=0.5, color=(255, 0, 128), base=100, flame=155),
            Blink(led, speed=0.5, color=(0, 32, 64)),

        ]
        animation = AnimationSequence(*animations, advance_interval=5)

        stop_animation(animation)
        assert animation._paused
        assert led.brightness == 0.0
        assert led.pin.value == 0.0
