import cptkip.core.environment as environment

MAX_DUTY = 65535

if environment.are_pins_available():
    import digitalio


class DigitalPin:
    """
    Simple Pin using a boolean value (False - off, True - on) to control output logic level on a Pin.
    """

    """
    :param value: The initial value of True (on), False (off)..
    :param invert: Set to True for connected devices where they are active on low. This essentially
                   reverses the logic level.
    """

    def __init__(self, pin, value: bool = False, invert: bool = False):
        self.pin = pin
        self._pin = None
        if environment.are_pins_available():
            self._pin = digitalio.DigitalInOut(pin)
            self._pin.direction = digitalio.Direction.OUTPUT

        self.invert = invert
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
