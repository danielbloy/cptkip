import time

import pytest

from cptkip.device.buzzer import Buzzer
from cptkip.pin.buzzer_pin import BuzzerPin


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
        pin = BuzzerPin(1)
        buzzer = Buzzer(pin)

        # call update() when nothing is playing and it should change anything
        buzzer.update()
        assert not buzzer.playing
        assert pin.frequency == 0

        # Play a frequency
        buzzer.play(123, 0.1)
        assert buzzer.playing
        assert pin.frequency == 123

        # Wait and it should still be playing
        time.sleep(0.07)
        buzzer.update()
        assert buzzer.playing
        assert pin.frequency == 123

        # Wait until the timer expired and it should clear.
        time.sleep(0.04)
        buzzer.update()
        assert not buzzer.playing
        assert pin.frequency == 123

    def test_play_twice(self):
        """
        Validates that play() plays the tone in the buzzer for the required duration
        and then a second tone once finished.
        """
        pin = BuzzerPin(1)
        buzzer = Buzzer(pin)

        # Play a frequency
        buzzer.play(123, 0.1)
        assert buzzer.playing
        assert pin.frequency == 123

        # Wait and it should still be playing
        time.sleep(0.15)
        buzzer.update()
        assert not buzzer.playing
        assert pin.frequency == 123

        # Play the second frequency
        buzzer.play(456, 0.1)
        assert buzzer.playing
        assert pin.frequency == 456

        # Wait and it should still be playing
        time.sleep(0.15)
        buzzer.update()
        assert not buzzer.playing
        assert pin.frequency == 456

    def test_play_overlapping(self):
        """
        Validates that play() plays the tone in the buzzer but can be overridden
        if called again before it has finished.
        """
        pin = BuzzerPin(1)
        buzzer = Buzzer(pin)

        assert not buzzer.playing

        # Play a frequency
        buzzer.play(123, 0.1)
        assert buzzer.playing
        assert pin.frequency == 123

        # Wait and it should still be playing
        time.sleep(0.07)
        buzzer.update()
        assert buzzer.playing
        assert pin.frequency == 123

        # Play a frequency
        buzzer.play(456, 0.1)

        # Wait and it should still be playing
        time.sleep(0.095)
        buzzer.update()
        buzzer.update()
        buzzer.update()
        assert buzzer.playing
        assert pin.frequency == 456

        # Wait a tiny bit longer and it should stop
        time.sleep(0.015)
        buzzer.update()
        assert not buzzer.playing
        assert pin.frequency == 456

    def test_off(self):
        """
        Validates that off stops the buzzer when playing.
        """
        pin = BuzzerPin(1)
        buzzer = Buzzer(pin)

        assert not buzzer.playing

        # Play a frequency
        buzzer.play(123, 0.1)
        assert buzzer.playing

        time.sleep(0.05)
        buzzer.update()
        assert buzzer.playing

        buzzer.off()
        assert not buzzer.playing

        # Now try a beep
        buzzer.beep()
        assert buzzer.playing

        buzzer.off()
        assert not buzzer.playing

    def test_beep(self):
        """
        Validates that beep() plays a beep.
        """
        pin = BuzzerPin(1)
        buzzer = Buzzer(pin)

        assert not buzzer.playing

        # Play a beep and make sure it lasts for the expected duration.
        buzzer.beep()
        buzzer.update()
        assert buzzer.playing
        time.sleep(0.25)
        buzzer.update()
        assert buzzer.playing
        time.sleep(0.1)
        buzzer.update()
        assert not buzzer.playing

        # Now play a second beep and it should behave as before
        buzzer.beep()
        buzzer.update()
        assert buzzer.playing
        time.sleep(0.25)
        buzzer.update()
        assert buzzer.playing
        time.sleep(0.1)
        buzzer.update()
        assert not buzzer.playing

        # Now play two beeps together, this is the same as a single beep
        buzzer.beep()
        buzzer.beep()
        buzzer.update()
        assert buzzer.playing
        time.sleep(0.25)
        buzzer.update()
        assert buzzer.playing
        time.sleep(0.1)
        buzzer.update()
        assert not buzzer.playing

        # Play a beep, wait and play again
        buzzer.beep()
        buzzer.update()
        assert buzzer.playing
        time.sleep(0.25)
        buzzer.update()
        assert buzzer.playing
        buzzer.beep()  # second beep effectively restarts the entire beep.
        buzzer.update()
        assert buzzer.playing
        time.sleep(0.25)
        buzzer.update()
        assert buzzer.playing
        time.sleep(0.1)
        buzzer.update()
        assert not buzzer.playing

    def test_beeps(self):
        assert False

    def test_beep_in_combination_with_beeps(self):
        assert False
