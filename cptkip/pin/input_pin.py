import cptkip.core.environment as environment

if environment.are_pins_available():
    import digitalio


class InputPin:
    """
    Simple Pin using a boolean value for input logic level on a Pin. Unlike
    OutputPins which have a capability to invert the value, input pins do not
    as they are typically used with buttons that can already default to working
    with inverted values.

    :param pin:    The pin to use as an input pin.
    :param pullup: Whether to set the pin to pull up or not. If an external
                   resistor is being used to pull the pin up or down, then
                   set this to None.
    """

    def __init__(self, pin, pullup: bool | None = True):
        self.pin = pin
        self._pin = None
        self.pullup = pullup
        if environment.are_pins_available():
            self._pin = digitalio.DigitalInOut(pin)
            self._pin.direction = digitalio.Direction.INPUT

            if pullup is not None:
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
        # Return the value of the pin if we have one.
        if self._pin:
            return self._pin.value

        # No pin so default to the value for pullup if specified
        if self.pullup is not None:
            return self.pullup

        # Default to True
        return True

    @value.setter
    def value(self, value: bool):
        if self._pin:
            self._pin.value = value
