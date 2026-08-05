import cptkip.config.configuration as config
from cptkip.zero.pixels import create_pixels


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
