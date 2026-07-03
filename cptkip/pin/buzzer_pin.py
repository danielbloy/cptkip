import cptkip.core.environment as environment

if environment.are_pins_available():
    import pwmio


class BuzzerPin:
    """
    Buzzer is a very lightweight implementation that uses PWM to play a
    sound at a given frequency by modifying the frequency and the duty
    cycle (for volume). This is different to a PwmPin that uses a fixed
    frequency and changes only the duty cycle
    """

    def __init__(self, pin, volume: float = 1.0):
        if environment.are_pins_available() and pin is None:
            raise ValueError("pin cannot be None")

        self.pin = pin
        self._buzzer = None
        self._volume = max(min(volume, 1.0), 0.0)
        self._frequency = 0

    def deinit(self) -> None:
        if self._buzzer:
            self._buzzer.duty_cycle = 0
            self._buzzer.deinit()

        self._buzzer = None

    @property
    def volume(self) -> float:
        """
        Returns the volume of the buzzer. This will be a value between 0.0 and 1.0.
        """
        return self._volume

    @volume.setter
    def volume(self, volume: float) -> None:
        """
        Allows setting of the volume of the buzzer. This should be a float value in
        the range of 0.0 to 1.0.

        :param volume: The new volume.
        """
        self._volume = max(min(volume, 1.0), 0.0)
        self.play(self.frequency)

    @property
    def frequency(self) -> int:
        """
        Returns the frequency the buzzer is currently set to play at.
        """
        return self._frequency

    @frequency.setter
    def frequency(self, frequency: int) -> None:
        """
        Allows setting of the frequency of the buzzer. This immediately re-applies
        the output at the new frequency, the same way volume does.

        :param frequency: The new frequency.
        """
        self.play(frequency)

    def play(self, frequency: int) -> None:
        """
        Play a tone at the specified frequency. This will continue to play
        until another play() or off() is called.

        :param frequency: The frequency to play.
        """
        # Update the pwm only if the frequency has changed or there is no active buzzer.
        if self._frequency != frequency or not self._buzzer:
            self._frequency = frequency
            self.off()
            if frequency > 0 and environment.are_pins_available():
                self._buzzer = pwmio.PWMOut(self.pin, frequency=frequency)

        if self._buzzer and frequency > 0 and environment.are_pins_available():
            self._buzzer.duty_cycle = int(self.volume * (2 ** 10))

    def off(self):
        """
        Stops the buzzer playing any sound.
        """
        self.deinit()

    def on(self):
        """
        Plays the buzzer at previous frequency and volume.
        """
        self.play(self.frequency)
