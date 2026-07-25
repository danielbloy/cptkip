import pytest

import cptkip.animation.flicker as flicker_module
from cptkip.animation.flicker import Flicker


class MockPixels:
    def __init__(self, num_pixels):
        self.auto_write = True
        self._pixels = [(0, 0, 0)] * num_pixels

    def __len__(self):
        return len(self._pixels)

    def __setitem__(self, index, value):
        self._pixels[index] = value

    def __getitem__(self, index):
        return self._pixels[index]


class TestFlicker:

    def test_constructor(self) -> None:
        """
        Validates that a Flicker is constructed with the correct parameters and
        that every pixel is initialised to the given colour.
        """
        pixels = MockPixels(4)
        flicker = Flicker(pixels, speed=0.1, color=(0x10, 0x20, 0x30))

        assert len(flicker) == 4
        assert flicker[0] == (0x10, 0x20, 0x30)
        assert flicker[1] == (0x10, 0x20, 0x30)
        assert flicker[2] == (0x10, 0x20, 0x30)
        assert flicker[3] == (0x10, 0x20, 0x30)
        assert pixels[0] == (0x10, 0x20, 0x30)
        assert pixels[1] == (0x10, 0x20, 0x30)
        assert pixels[2] == (0x10, 0x20, 0x30)
        assert pixels[3] == (0x10, 0x20, 0x30)

    def test_get_out_of_bounds(self) -> None:
        """
        Validates that get() raises when given an out of bounds index.
        """
        pixels = MockPixels(2)
        flicker = Flicker(pixels, speed=0.1, color=(0, 0, 0))

        with pytest.raises(ValueError):
            flicker.get(-1)

        with pytest.raises(ValueError):
            flicker.get(2)

    def test_set_out_of_bounds(self) -> None:
        """
        Validates that set() raises when given an out of bounds index.
        """
        pixels = MockPixels(2)
        flicker = Flicker(pixels, speed=0.1, color=(0, 0, 0))

        with pytest.raises(ValueError):
            flicker.set(-1, (0, 0, 0))

        with pytest.raises(ValueError):
            flicker.set(2, (0, 0, 0))

    def test_get_and_set(self) -> None:
        """
        Validates that get() and set() work as expected including writing
        through to the underlying pixel_object.
        """
        pixels = MockPixels(3)
        flicker = Flicker(pixels, speed=0.1, color=(0, 0, 0))

        flicker.set(0, (0xFF, 0x00, 0x80))
        assert flicker.get(0) == (0xFF, 0x00, 0x80)
        assert pixels[0] == (0xFF, 0x00, 0x80)

        flicker.set(1, (0x10, 0x20, 0x30))
        assert flicker.get(1) == (0x10, 0x20, 0x30)
        assert pixels[1] == (0x10, 0x20, 0x30)

        # Untouched pixel is unaffected.
        assert flicker.get(2) == (0, 0, 0)
        assert pixels[2] == (0, 0, 0)

    def test_get_and_set_item(self) -> None:
        """
        Validates that __getitem__ and __setitem__ behave the same as get() and set(),
        including writing through to the underlying pixel_object.
        """
        pixels = MockPixels(3)
        flicker = Flicker(pixels, speed=0.1, color=(0, 0, 0))

        flicker[0] = (0xFF, 0x00, 0x80)
        assert flicker[0] == (0xFF, 0x00, 0x80)
        assert pixels[0] == (0xFF, 0x00, 0x80)

        flicker[1] = (0x10, 0x20, 0x30)
        assert flicker[1] == (0x10, 0x20, 0x30)
        assert pixels[1] == (0x10, 0x20, 0x30)

        # Untouched pixel is unaffected.
        assert flicker[2] == (0, 0, 0)
        assert pixels[2] == (0, 0, 0)

    def test_set_masks_to_8_bits(self) -> None:
        """
        Validates that set() masks each colour channel down to 8 bits.
        """
        pixels = MockPixels(1)
        flicker = Flicker(pixels, speed=0.1, color=(0, 0, 0))

        flicker.set(0, (256, 300, 511))
        assert flicker.get(0) == (0, 44, 255)
        assert pixels[0] == (0, 44, 255)

    def test_set_all(self) -> None:
        """
        Validates that set_all() sets every pixel to the given colour.
        """
        pixels = MockPixels(5)
        flicker = Flicker(pixels, speed=0.1, color=(0, 0, 0))

        flicker.set_all((0x11, 0x22, 0x33))
        for i in range(5):
            assert flicker[i] == (0x11, 0x22, 0x33)
            assert pixels[i] == (0x11, 0x22, 0x33)

    def test_zero_flame_holds_base_brightness(self) -> None:
        """
        Validates that with flame=0 (no randomness), draw() scales each pixel by
        base / 255 exactly.
        """
        for base in [128, 37, 45, 255]:
            pixels = MockPixels(1)
            flicker = Flicker(pixels, speed=0.1, color=(255, 255, 255), base=base, flame=0)

            expected = int(255 * base / 255)

            for i in range(10):
                flicker.draw()
                assert pixels[0] == (expected, expected, expected)

    def test_draw_clamps_to_255(self, monkeypatch) -> None:
        """
        Validates that draw() clamps to full brightness rather than wrapping when
        base + flame exceeds 255.
        """
        for base, flame in [(200, 100), (100, 200), (200, 200)]:
            pixels = MockPixels(1)
            flicker = Flicker(pixels, speed=0.1, color=(255, 255, 255), base=base, flame=flame)

            # Force the random flame contribution to its maximum so base + brightness (300)
            # deterministically exceeds 255.
            monkeypatch.setattr(flicker_module.random, "randint", lambda a, b: b)

            flicker.draw()

            assert pixels[0] == (255, 255, 255)

    def test_draw_respects_spacing(self) -> None:
        """
        Validates that draw() only updates pixels that fall on the configured spacing
        interval, leaving the others untouched.
        """
        pixels = MockPixels(4)
        flicker = Flicker(pixels, speed=0.1, color=(255, 255, 255), spacing=2, base=100, flame=0)

        # Give pixels 1 and 3 a distinct colour so we can detect if draw() touches them.
        flicker.set(1, (10, 20, 30))
        flicker.set(3, (10, 20, 30))

        flicker.draw()

        expected = int(255 * 100 / 255)
        assert pixels[0] == (expected, expected, expected)
        assert pixels[1] == (10, 20, 30)  # untouched - not on the spacing interval
        assert pixels[2] == (expected, expected, expected)
        assert pixels[3] == (10, 20, 30)  # untouched - not on the spacing interval

        # Try a different spacing
        pixels = MockPixels(4)
        flicker = Flicker(pixels, speed=0.1, color=(255, 255, 255), spacing=3, base=100, flame=0)

        # Give pixels 1 and 2 a distinct colour so we can detect if draw() touches them.
        flicker.set(1, (10, 20, 30))
        flicker.set(2, (10, 20, 30))

        flicker.draw()

        expected = int(255 * 100 / 255)
        assert pixels[0] == (expected, expected, expected)
        assert pixels[1] == (10, 20, 30)  # untouched - not on the spacing interval
        assert pixels[2] == (10, 20, 30)  # untouched - not on the spacing interval
        assert pixels[3] == (expected, expected, expected)

    def test_construction_with_int_color(self) -> None:
        """
        Regression test: an int/hex colour (a documented, supported form for
        every other Animation subclass) used to crash the constructor because
        it bypassed the base class's int-to-tuple conversion.
        """
        pixels = MockPixels(2)
        flicker = Flicker(pixels, speed=0.1, color=0xFFAA00)

        assert flicker[0] == (0xFF, 0xAA, 0x00)
        assert pixels[0] == (0xFF, 0xAA, 0x00)

    def test_reassigning_color_updates_pixels(self) -> None:
        """
        Regression test: setting .color after construction used to silently
        do nothing, because Flicker never overrode _set_color() so the base
        class's default no-op implementation was used instead.
        """
        pixels = MockPixels(2)
        flicker = Flicker(pixels, speed=0.1, color=(0x10, 0x20, 0x30))

        flicker.color = (0x40, 0x50, 0x60)

        assert flicker[0] == (0x40, 0x50, 0x60)
        assert flicker[1] == (0x40, 0x50, 0x60)
        assert pixels[0] == (0x40, 0x50, 0x60)
        assert pixels[1] == (0x40, 0x50, 0x60)

    def test_construction_with_invalid_spacing_raises(self) -> None:
        """
        Validates that spacing < 1 raises immediately at construction, rather
        than crashing inside draw() (spacing=0) or silently becoming a
        permanent no-op (negative spacing).
        """
        pixels = MockPixels(4)

        with pytest.raises(ValueError):
            Flicker(pixels, speed=0.1, color=(0, 0, 0), spacing=0)

        with pytest.raises(ValueError):
            Flicker(pixels, speed=0.1, color=(0, 0, 0), spacing=-1)

    def test_out_of_bounds_raises_value_error(self) -> None:
        """
        Bounds checks should raise ValueError, consistent with every other
        validation check in the codebase, not a bare Exception.
        """
        pixels = MockPixels(2)
        flicker = Flicker(pixels, speed=0.1, color=(0, 0, 0))

        with pytest.raises(ValueError):
            flicker.get(-1)

        with pytest.raises(ValueError):
            flicker.set(2, (0, 0, 0))

    def test_name_parameter(self) -> None:
        """
        Validates that the name parameter is accepted and stored, as it is
        for every other Animation subclass.
        """
        pixels = MockPixels(2)
        flicker = Flicker(pixels, speed=0.1, color=(0, 0, 0), name="my-flicker")

        assert flicker.name == "my-flicker"

    def test_construction_forces_auto_write_off(self) -> None:
        """
        Validates the base Animation class's behaviour of forcing
        pixel_object.auto_write to False is in effect for Flicker too.
        """
        pixels = MockPixels(2)
        assert pixels.auto_write is True

        Flicker(pixels, speed=0.1, color=(0, 0, 0))

        assert pixels.auto_write is False
