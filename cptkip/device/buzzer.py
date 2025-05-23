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

        self.__buzzer = buzzer
        self.__playing = False
        self.__stop_time_ns = 0
        self.__beeps = 0

    @property
    def playing(self):
        """Is the buzzer playing or not"""
        return self.__playing

    def beep(self) -> None:
        """Makes a beep."""
        if self.playing:
            self.__beeps += 1
        else:
            self.play(262, 0.3)

    def beeps(self, count: int) -> None:
        """
        Plays a series of beeps.

        :param count: The number of beeps to play.
        """
        self.beep()
        self.__beeps += max(count - 1, 0)

    def play(self, frequency: int, duration: float) -> None:
        """
        Plays a tone at the given frequency for the specified number of seconds.

        :param frequency: The frequency to play the tone at.
        :param duration: The duration in seconds to play the tone for.
        """
        # Calculate the stop time.
        self.__stop_time_ns = time.monotonic_ns() + int(duration * control.NS_PER_SECOND)
        self.__playing = True
        self.__buzzer.play(frequency)

    def off(self) -> None:
        """
        Turns off the buzzer; cancelling and additional beeps.
        """
        self.__beeps = 0
        self.__off()

    def __off(self) -> None:
        self.__playing = False
        self.__buzzer.off()

    def update(self):
        """
        Call to turn the buzzer off at the desired time internal.
        """
        if (self.__playing or self.__beeps > 0) and time.monotonic_ns() >= self.__stop_time_ns:
            if self.__playing:
                self.__off()

                # Allow for a delay between beeps.
                if self.__beeps > 0:
                    self.__stop_time_ns += (0.1 * control.NS_PER_SECOND)

            else:

                # If there are more beeps expected in the sequence then play them.
                if self.__beeps > 0:
                    self.beep()
