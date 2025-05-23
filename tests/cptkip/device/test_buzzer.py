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

    def test_play(self):
        assert False

    def test_off(self):
        assert False

    def test_update(self):
        assert False

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
