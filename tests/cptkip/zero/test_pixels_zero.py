from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.sequence import AnimationSequence

import cptkip.config.configuration as config
from cptkip.animation.flicker import Flicker
from cptkip.zero.pixels import create_pixels, stop_animation, stop_pixels


class TestPixelsZero:
    """
    The tests in here are trivial. They are not intended to test the functionality
    of the underlying pins or devices, just that the `cptkip.zero.pixels` module
    constructs them correctly.
    """

    def test_create_pixels(self):
        """
        Validates that a pixels object is created "properly".
        """
        # No brightness
        pixels = create_pixels()
        assert pixels
        assert pixels.pin == config.PIXELS_PIN == "pixels_pin"
        assert pixels.n == config.PIXELS_COUNT == 37
        assert pixels.brightness == 1.0

        # with brightness
        pixels = create_pixels(0.1)
        assert pixels
        assert pixels.pin == config.PIXELS_PIN == "pixels_pin"
        assert pixels.n == config.PIXELS_COUNT == 37
        assert pixels.brightness == 0.1

        # No brightness
        pixels = create_pixels(pin="pin", count=3)
        assert pixels
        assert pixels.pin == "pin"
        assert pixels.n == 3
        assert pixels.brightness == 1.0

        # with brightness
        pixels = create_pixels(0.1, pin="pin", count=3)
        assert pixels
        assert pixels.pin == "pin"
        assert pixels.n == 3
        assert pixels.brightness == 0.1

    def test_stop_pixels(self):
        """
        Validates that a Pixel object gets stopped (turned off) correctly.
        """
        pixels = create_pixels()
        assert pixels.brightness == 1.0

        stop_pixels(pixels)
        assert pixels.brightness == 0.0

    def test_stop_animation_works(self):
        """
        Validates that stop_animation() works properly.
        """
        pixels = create_pixels()
        animation = Flicker(pixels, speed=0.5, color=(255, 0, 128), base=100, flame=155)

        stop_animation(animation)
        assert animation._paused
        assert pixels.brightness == 0.0

    def test_stop_animation_works_with_sequence(self):
        """
        Validates that stop_animation() works properly.
        """
        pixels = create_pixels()

        animations = [
            Flicker(pixels, speed=0.5, color=(255, 0, 128), base=100, flame=155),
            Blink(pixels, speed=0.5, color=(0, 32, 64)),

        ]
        animation = AnimationSequence(*animations, advance_interval=5)

        stop_animation(animation)
        assert animation._paused
        assert pixels.brightness == 0.0

    def test_module_does_not_load_animation_library(self, monkeypatch):
        """
        Importing cptkip.zero.pixels must not import adafruit_led_animation (it is only
        needed by stop_animation), to save memory when only the create_* helpers are used.
        """
        import importlib
        import sys
        for name in list(sys.modules):
            if name.startswith("adafruit_led_animation") or name == "cptkip.zero.pixels":
                monkeypatch.delitem(sys.modules, name)

        importlib.import_module("cptkip.zero.pixels")
        assert not any(name.startswith("adafruit_led_animation") for name in sys.modules)
