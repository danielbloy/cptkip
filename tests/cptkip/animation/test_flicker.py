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

    def test_draw_clamps_instead_of_wrapping_when_base_plus_flame_exceeds_255(self, monkeypatch) -> None:
        pixels = MockPixels(1)
        flicker = Flicker(pixels, speed=0.1, color=(255, 255, 255), base=200, flame=100)

        # Force the random flame contribution to its maximum so base + brightness (300)
        # deterministically exceeds 255.
        monkeypatch.setattr(flicker_module.random, "randint", lambda a, b: b)

        flicker.draw()

        assert pixels[0] == (255, 255, 255)
