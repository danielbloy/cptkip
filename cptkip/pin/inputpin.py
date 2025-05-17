import cptkip.core.environment as environment

if environment.are_pins_available():
    import digitalio


class InputPin:
    """
    Simple Pin using a boolean value for input logic level on a Pin.

    :param pin:    The pin to use as an input pin.
    :param pullup: Whether the pin should be pulled up or not.
    """

    def __init__(self, pin, pullup: bool = True):
        self.pin = pin
        self._pin = None
        self.pullup = pullup
        if environment.are_pins_available():
            self._pin = digitalio.DigitalInOut(pin)
            self._pin.direction = digitalio.Direction.INPUT

            if pullup:
                self._pin.pull = digitalio.Pull.UP
            else:
                self._pin.pull = digitalio.Pull.DOWN

    def deinit(self) -> None:
        if environment.are_pins_available():
            self._pin.deinit()

        self._pin = None

    @property
    def value(self):
        return self._pin.value if self._pin else self.pullup

    @value.setter
    def value(self, value: bool):
        if self._pin:
            self._pin.value = value
