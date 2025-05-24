import time

import pytest

from cptkip.device.buzzer import Buzzer
from cptkip.pin.buzzer_pin import BuzzerPin


class MockBuzzerPin(BuzzerPin):
    def __init__(self):
        self.play_count = 0
        self.last_frequency = 0
        self.off_count = 0
        super().__init__(None)

    def play(self, frequency: int) -> None:
        self.play_count += 1
        super().play(frequency)

    def off(self) -> None:
        self.off_count += 1


class TestBuzzer:

    def test_constructor(self) -> None:
        """
        Validates that a Buzzer is constructed with the correct parameters
        """
        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Buzzer(None)

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Buzzer(2)

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Buzzer("None")

        # This should work
        buzzer = Buzzer(BuzzerPin(1))
        assert not buzzer.playing

    def test_play_once(self):
        """
        Validates that play() plays the tone in the buzzer for the required duration.
        This also tests update() which controls the duration.
        """
        pin = MockBuzzerPin()
        buzzer = Buzzer(pin)
        assert pin.frequency == 0
        assert pin.play_count == 0
        assert pin.off_count == 0
        assert not buzzer.playing

        # call update() when nothing is playing and it should change anything
        buzzer.update()
        assert not buzzer.playing
        assert pin.frequency == 0
        assert pin.play_count == 0
        assert pin.off_count == 0

        # Play a frequency
        buzzer.play(123, 0.1)
        assert buzzer.playing
        assert pin.frequency == 123
        assert pin.play_count == 1
        assert pin.off_count == 1  # Calling play() first calls off()

        # Wait and it should still be playing
        time.sleep(0.07)
        buzzer.update()
        assert buzzer.playing
        assert pin.frequency == 123
        assert pin.play_count == 1
        assert pin.off_count == 1

        # Wait until the timer expired and it should clear.
        time.sleep(0.04)
        buzzer.update()
        assert not buzzer.playing
        assert pin.frequency == 123
        assert pin.play_count == 1
        assert pin.off_count == 2

    def test_play_twice(self):
        """
        Validates that play() plays the tone in the buzzer for the required duration
        and then a second tone once finished.
        """
        pin = MockBuzzerPin()
        buzzer = Buzzer(pin)
        assert pin.frequency == 0
        assert pin.play_count == 0
        assert pin.off_count == 0
        assert not buzzer.playing

        # Play a frequency
        buzzer.play(123, 0.1)
        assert buzzer.playing
        assert pin.frequency == 123
        assert pin.play_count == 1
        assert pin.off_count == 1  # Calling play() first calls off()

        # Wait and it should stop playing
        time.sleep(0.15)
        buzzer.update()
        assert not buzzer.playing
        assert pin.frequency == 123
        assert pin.play_count == 1
        assert pin.off_count == 2

        # Play the second frequency
        buzzer.play(456, 0.1)
        assert buzzer.playing
        assert pin.frequency == 456
        assert pin.play_count == 2
        assert pin.off_count == 3

        # Wait and it should stop playing
        time.sleep(0.15)
        buzzer.update()
        assert not buzzer.playing
        assert pin.frequency == 456
        assert pin.play_count == 2
        assert pin.off_count == 4

    def test_play_overlapping(self):
        """
        Validates that play() plays the tone in the buzzer but can be overridden
        if called again before it has finished.
        """
        pin = MockBuzzerPin()
        buzzer = Buzzer(pin)
        assert pin.frequency == 0
        assert pin.play_count == 0
        assert pin.off_count == 0
        assert not buzzer.playing

        # Play a frequency
        buzzer.play(123, 0.1)
        assert buzzer.playing
        assert pin.frequency == 123
        assert pin.play_count == 1
        assert pin.off_count == 1  # Calling play() first calls off()

        # Wait and it should still be playing
        time.sleep(0.07)
        buzzer.update()
        assert buzzer.playing
        assert pin.frequency == 123
        assert pin.play_count == 1
        assert pin.off_count == 1

        # Play a frequency
        buzzer.play(456, 0.1)
        assert pin.play_count == 2
        assert pin.off_count == 2

        # Wait and it should still be playing
        time.sleep(0.09)
        buzzer.update()
        buzzer.update()
        buzzer.update()
        assert buzzer.playing
        assert pin.frequency == 456
        assert pin.play_count == 2
        assert pin.off_count == 2

        # Wait a tiny bit longer and it should stop
        time.sleep(0.02)
        buzzer.update()
        assert not buzzer.playing
        assert pin.frequency == 456
        assert pin.play_count == 2
        assert pin.off_count == 3

    def test_off(self):
        """
        Validates that off stops the buzzer when playing.
        """
        pin = MockBuzzerPin()
        buzzer = Buzzer(pin)
        assert pin.frequency == 0
        assert pin.play_count == 0
        assert pin.off_count == 0
        assert not buzzer.playing

        # Play a frequency
        buzzer.play(123, 0.1)
        assert buzzer.playing
        assert pin.play_count == 1
        assert pin.off_count == 1

        time.sleep(0.05)
        buzzer.update()
        assert buzzer.playing
        assert pin.play_count == 1
        assert pin.off_count == 1

        buzzer.off()
        assert not buzzer.playing
        assert pin.play_count == 1
        assert pin.off_count == 2

        # Now try a beep
        buzzer.beep()
        assert buzzer.playing
        assert pin.play_count == 2
        assert pin.off_count == 3

        buzzer.off()
        assert not buzzer.playing
        assert pin.play_count == 2
        assert pin.off_count == 4

    def test_beep_once(self):
        """
        Validates that beep() plays a beep.
        """
        pin = MockBuzzerPin()
        buzzer = Buzzer(pin)
        assert pin.frequency == 0
        assert pin.play_count == 0
        assert pin.off_count == 0
        assert not buzzer.playing

        # Play a beep and make sure it lasts for the expected duration.
        buzzer.beep()
        assert pin.play_count == 1
        assert pin.off_count == 1
        assert buzzer.playing
        buzzer.update()
        assert pin.play_count == 1
        assert pin.off_count == 1
        assert buzzer.playing
        time.sleep(0.25)
        buzzer.update()
        assert pin.play_count == 1
        assert pin.off_count == 1
        assert buzzer.playing
        time.sleep(0.1)
        buzzer.update()
        assert pin.play_count == 1
        assert pin.off_count == 2
        assert not buzzer.playing

    def test_beep_twice_not_overlapping(self):
        """
        Validates that beep() can play one beep after another
        """
        pin = MockBuzzerPin()
        buzzer = Buzzer(pin)

        # Play the first beep
        buzzer.beep()
        buzzer.update()
        assert pin.play_count == 1
        assert pin.off_count == 1
        assert buzzer.playing
        time.sleep(0.25)
        buzzer.update()
        assert pin.play_count == 1
        assert pin.off_count == 1
        assert buzzer.playing
        time.sleep(0.1)
        buzzer.update()
        assert pin.play_count == 1
        assert pin.off_count == 2
        assert not buzzer.playing

        # Now play a second beep and it should behave as before
        buzzer.beep()
        buzzer.update()
        assert pin.play_count == 2
        assert pin.off_count == 3
        assert buzzer.playing
        time.sleep(0.25)
        buzzer.update()
        assert pin.play_count == 2
        assert pin.off_count == 3
        assert buzzer.playing
        time.sleep(0.1)
        buzzer.update()
        assert pin.play_count == 2
        assert pin.off_count == 4
        assert not buzzer.playing

    def test_calling_beep_multiple_times(self):
        """
        Calling beep multiple times should queue up multiple beeps.
        """
        pin = MockBuzzerPin()
        buzzer = Buzzer(pin)

        # Now play two beeps together, this is the same as queueing the beeps
        buzzer.beep()
        buzzer.beep()
        buzzer.update()
        assert pin.play_count == 1
        assert pin.off_count == 1
        assert buzzer.playing

        time.sleep(0.2)
        buzzer.update()
        assert pin.play_count == 1
        assert pin.off_count == 1
        assert buzzer.playing

        # This will finish the first beep and go into the off time.
        time.sleep(0.15)
        buzzer.update()
        assert pin.play_count == 1
        assert pin.off_count == 2
        assert not buzzer.playing

        # Transition back into playing the second beep
        time.sleep(0.2)
        buzzer.update()
        assert pin.play_count == 2
        assert pin.off_count == 3
        assert buzzer.playing

        # Transition through the final beep
        time.sleep(0.4)
        buzzer.update()
        assert pin.play_count == 2
        assert pin.off_count == 4
        assert not buzzer.playing

    def test_beeps(self):
        """
        This will be the same as calling beep() multiple times.
        """
        pin = MockBuzzerPin()
        buzzer = Buzzer(pin)

        # Now play two beeps together, this is the same as queueing the beeps
        buzzer.beeps(2)
        buzzer.update()
        assert pin.play_count == 1
        assert pin.off_count == 1
        assert buzzer.playing

        time.sleep(0.2)
        buzzer.update()
        assert pin.play_count == 1
        assert pin.off_count == 1
        assert buzzer.playing

        # This will finish the first beep and go into the off time.
        time.sleep(0.15)
        buzzer.update()
        assert pin.play_count == 1
        assert pin.off_count == 2
        assert not buzzer.playing

        # Transition back into playing the second beep
        time.sleep(0.2)
        buzzer.update()
        assert pin.play_count == 2
        assert pin.off_count == 3
        assert buzzer.playing

        # Transition through the final beep
        time.sleep(0.4)
        buzzer.update()
        assert pin.play_count == 2
        assert pin.off_count == 4
        assert not buzzer.playing
