from cptkip.pin.buzzer_pin import BuzzerPin


class TestBuzzerPin:

    def test_default_construction(self):
        """
        Construct a new BuzzerPin with default values and validate it has the correct values.
        """
        pin = BuzzerPin(4)

        assert pin.pin == 4
        assert pin.volume == 1.0

    def test_construction(self):
        """
        Construct a new BuzzerPin with specified values and validate it has the correct values.
        """
        pin = BuzzerPin(5, volume=0.7)

        assert pin.pin == 5
        assert pin.volume == 0.7

    def test_multiple_deinit(self):
        """
        Call deinit() multiple times without error.
        """
        pin = BuzzerPin(3)
        pin.deinit()
        pin.deinit()
        pin.deinit()

    def test_on_off(self):
        """
        Call on() and off() multiple times, ensuring it does not change volume or frequency.
        """
        pin = BuzzerPin(3)
        pin.play(1234)
        assert pin.volume == 1.0
        assert pin.frequency == 1234

        pin.off()
        assert pin.volume == 1.0
        assert pin.frequency == 1234

        pin.on()
        assert pin.volume == 1.0
        assert pin.frequency == 1234

        pin.volume = 0.5
        pin.frequency = 4321

        pin.on()
        assert pin.volume == 0.5
        assert pin.frequency == 4321

        pin.off()
        assert pin.volume == 0.5
        assert pin.frequency == 4321

    def test_volume(self):
        """
        Call volume multiple times, ensuring it sets the correct value.
        """
        pin = BuzzerPin(3)
        assert pin.volume == 1.0

        pin.volume = 0.0
        assert pin.volume == 0.0

        pin.volume = 1.0
        assert pin.volume == 1.0

        pin.volume = 1.0
        assert pin.volume == 1.0

        pin.volume = 0.2
        assert pin.volume == 0.2

        pin.volume = 0.0
        assert pin.volume == 0.0

    def test_play(self):
        """
        Call play multiple times, ensuring it sets the correct value.
        """
        pin = BuzzerPin(3)
        assert pin.frequency == 0

        pin.play(1000)
        assert pin.frequency == 1000

        pin.play(500)
        assert pin.frequency == 500

        pin.play(1234)
        assert pin.frequency == 1234
