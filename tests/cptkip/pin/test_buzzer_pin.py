from cptkip.pin.buzzer_pin import BuzzerPin


class TrackingBuzzerPin(BuzzerPin):
    def __init__(self, pin, volume: float = 1.0):
        self.play_count = 0
        super().__init__(pin, volume)

    def play(self, frequency: int):
        self.play_count += 1
        super().play(frequency)


class TestBuzzerPin:

    def test_default_construction(self):
        """
        Construct a new BuzzerPin with default values and validate it has the correct values.
        """
        pin = BuzzerPin(4)

        assert pin.pin == 4
        assert pin.volume == 1.0
        assert pin.playing is False
        assert pin.frequency == 0

    def test_construction(self):
        """
        Construct a new BuzzerPin with specified values and validate it has the correct values.
        """
        pin = BuzzerPin(5, volume=0.7)

        assert pin.pin == 5
        assert pin.volume == 0.7
        assert pin.playing is False
        assert pin.frequency == 0

    def test_multiple_deinit(self):
        """
        Call deinit() multiple times without error.
        """
        pin = BuzzerPin(3)
        assert pin.playing is False
        pin.deinit()
        assert pin.playing is False
        pin.deinit()
        assert pin.playing is False
        pin.deinit()
        assert pin.playing is False

    def test_on_off(self):
        """
        Call on() and off() multiple times, ensuring it does not change volume or frequency.
        """
        pin = BuzzerPin(3)
        pin.play(1234)
        assert pin.volume == 1.0
        assert pin.frequency == 1234
        assert pin.playing is True

        pin.off()
        assert pin.volume == 1.0
        assert pin.frequency == 1234
        assert pin.playing is False

        pin.on()
        assert pin.volume == 1.0
        assert pin.frequency == 1234
        assert pin.playing is True

        pin.volume = 0.5
        pin.frequency = 4321
        assert pin.playing is True

        pin.on()
        assert pin.volume == 0.5
        assert pin.frequency == 4321
        assert pin.playing is True

        pin.off()
        assert pin.volume == 0.5
        assert pin.frequency == 4321
        assert pin.playing is False

    def test_volume(self):
        """
        Call volume multiple times, ensuring it sets the correct value.
        """
        pin = BuzzerPin(3)
        assert pin.volume == 1.0
        assert pin.playing is False

        pin.volume = 0.0
        assert pin.volume == 0.0
        assert pin.playing is False

        pin.volume = 1.0
        assert pin.volume == 1.0
        assert pin.playing is False

        pin.volume = 1.0
        assert pin.volume == 1.0
        assert pin.playing is False

        pin.volume = 0.2
        assert pin.volume == 0.2
        assert pin.playing is False

        pin.volume = 0.0
        assert pin.volume == 0.0
        assert pin.playing is False

    def test_play(self):
        """
        Call play multiple times, ensuring it sets the correct value.
        """
        pin = BuzzerPin(3)
        assert pin.frequency == 0
        assert pin.playing is False

        pin.play(1000)
        assert pin.frequency == 1000
        assert pin.playing is True

        pin.play(500)
        assert pin.frequency == 500
        assert pin.playing is True

        pin.play(1234)
        assert pin.frequency == 1234
        assert pin.playing is True

    def test_setting_frequency_or_volume_calls_play(self) -> None:
        """
        Validates that both volume and frequency re-apply the output immediately when set
        (i.e. it calls play() internally).
        """
        pin = TrackingBuzzerPin(3)
        pin.play(1000)
        assert pin.play_count == 1
        assert pin.playing is True

        pin.volume = 0.5
        assert pin.play_count == 2
        assert pin.playing is True

        pin.frequency = 300
        assert pin.play_count == 3
        assert pin.playing is True

        # Setting a volume of zero will stop playing
        pin.volume = 0
        assert pin.play_count == 4
        assert pin.playing is False

        # Setting a volume above zero will start playing
        pin.volume = 0.5
        assert pin.play_count == 5
        assert pin.playing is True

        # Setting a frequency of zero will stop playing.
        pin.frequency = 0
        assert pin.play_count == 6
        assert pin.playing is False

        # Setting a frequency above zero will start playing
        pin.frequency = 300
        assert pin.play_count == 7
        assert pin.playing is True

        # Set both frequency and volume to zero.
        pin.volume = 0
        pin.frequency = 0
        assert pin.play_count == 9
        assert pin.playing is False

        # Setting a volume above zero will not start playing
        pin.volume = 0.5
        assert pin.play_count == 10
        assert pin.playing is False
        pin.volume = 0

        # Setting a frequency above zero will not start playing
        pin.frequency = 300
        assert pin.play_count == 12
        assert pin.playing is False

        # Set both frequency and volume above zero, it should start playing.
        pin.frequency = 300
        pin.volume = 0.5
        assert pin.play_count == 14
        assert pin.playing is True
