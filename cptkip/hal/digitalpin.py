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


class OutputPin:
    """
    Simple Pin using a boolean value (False - off, True - on) to control output logic level on a Pin.

    :param pin:    The pin to use as an output pin.
    :param value:  The initial value of True (on), False (off).
    :param invert: Set to True for connected devices where they are active on low. This essentially
                   reverses the logic level output and is useful for output that are active on low
                   such as the LEDs on a Pimoroni Tiny 2040. The value stored by the pin is the
                   original value.
    """

    def __init__(self, pin, value: bool = False, invert: bool = False):
        self.pin = pin
        self._pin = None
        self.invert = invert
        if environment.are_pins_available():
            self._pin = digitalio.DigitalInOut(pin)
            self._pin.direction = digitalio.Direction.OUTPUT

        self.value = value

    def deinit(self) -> None:
        if environment.are_pins_available():
            self._pin.deinit()

        self._pin = None

    # Turns the pin fully on.
    def on(self):
        self.value = True

    # Turns the pin fully off.
    def off(self):
        self.value = False

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: bool):
        self._value = value

        if self._pin:
            self._pin.value = not value if self.invert else value
