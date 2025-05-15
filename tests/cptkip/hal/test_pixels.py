import cptkip.hal.pixels as pixels


class TestPixels:
    def test_default_construction(self):
        """
        Just tests that dummy Pixels default construction works.
        """
        pix = pixels.Pixels(3, 8, 1.0)

        assert pix.pin == 3
        assert pix.num_pixels == 8
        assert pix.brightness == 1.0
        assert pix.auto_write

    def test_construction(self):
        """
        Just tests that dummy Pixels default construction works when all values specified.
        """
        pix = pixels.Pixels(5, 9, 0.5, auto_write=False)

        assert pix.pin == 5
        assert pix.num_pixels == 9
        assert pix.brightness == 0.5
        assert not pix.auto_write

    def test_construction_via_new(self):
        """
        Validate that the wrapper function caps the brightness to the allowed range
        """
        pix = pixels.create(3, 8, -1.0)

        assert pix.pin == 3
        assert pix.num_pixels == 8
        assert pix.brightness == 0.0
        assert not pix.auto_write

        pix = pixels.create(5, 9, 1.5)

        assert pix.pin == 5
        assert pix.num_pixels == 9
        assert pix.brightness == 1.0
        assert not pix.auto_write
