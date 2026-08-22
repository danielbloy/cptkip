import time

import cptkip.core.control as control
from cptkip.pin.buzzer_pin import BuzzerPin


class Buzzer:
    """
    Buzzer provides a trivial method to play tones through a simple buzzer; such
    as a little piezo buzzer. Buzzer works well with simply melodies that can be
    provided with the Melody and MelodySequence classes.
    """

    def __init__(self, buzzer: BuzzerPin):
        if buzzer is None:
            raise ValueError("buzzer cannot be None")

        if not isinstance(buzzer, BuzzerPin):
            raise ValueError("buzzer must be of type BuzzerPin")

        self._buzzer = buzzer
        self._playing = False
        self._stop_time_ns = 0
        self._beeps = 0

    def __enter__(self):
        return self

    # TODO: Test
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deinit()

    def deinit(self) -> None:
        """
        Releases the underlying pin.
        """
        self._off()
        self._buzzer.deinit()

    @property
    def volume(self):
        """The volume of the buzzer"""
        return self._buzzer.volume

    @volume.setter
    def volume(self, value: float):
        """Set the volume of the buzzer"""
        value = min(max(value, 0.0), 1.0)
        self._buzzer.volume = value

    @property
    def playing(self):
        """Is the buzzer playing or not"""
        return self._playing

    def beep(self) -> None:
        """Makes a beep."""
        if self.playing:
            self._beeps += 1
        else:
            self._beeps = max(self._beeps - 1, 0)
            self.play(262, 0.3)

    def beeps(self, count: int) -> None:
        """
        Plays a series of beeps.

        :param count: The number of beeps to play.
        """
        if count <= 0:
            return

        self.beep()
        self._beeps += max(count - 1, 0)

    def play(self, frequency: int, duration: float) -> None:
        """
        Plays a tone at the given frequency for the specified number of seconds.
        This will interrupt any existing tone or beeps that are playing
        (outstanding beeps will play once the tone completes).

        :param frequency: The frequency to play the tone at.
        :param duration: The duration in seconds to play the tone for.
        """
        # Calculate the stop time.
        self._stop_time_ns = time.monotonic_ns() + int(duration * control.NS_PER_SECOND)
        self._playing = True
        self._buzzer.play(frequency)

    def off(self) -> None:
        """
        Turns off the buzzer; cancelling and additional beeps.
        """
        self._beeps = 0
        self._off()

    def _off(self) -> None:
        self._playing = False
        self._buzzer.off()

    def update(self) -> None:
        """
        Call to turn the buzzer off at the desired time interval.
        """
        now = time.monotonic_ns()
        if self._playing and now >= self._stop_time_ns:
            self._off()

            # Allow for a delay between beeps. It won't be playing but will have a stop time.
            if self._beeps > 0:
                self._stop_time_ns += int(0.1 * control.NS_PER_SECOND)

        if self._beeps > 0 and now >= self._stop_time_ns:
            self.beep()
