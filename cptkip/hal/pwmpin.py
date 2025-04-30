import cptkip.core.environment as environment

MAX_DUTY = 65535

if environment.are_pins_available():
    import pwmio


class PwmPin:
    """
    Simple Pin using value to control the PWM. This can be used to control
    the brightness in LEDS for example.
    """

    """
    :param value: The initial PWM value between 0.0 and 1.0.
    :param inverse: Set to True for connected devices where they are active on low.
                    An example would be the RGB LEDs on a Pimoroni Tiny 2040.
    :param frequency: The frequency of the PWM value.
    """

    def __init__(self, pin, value: float = 0.0, inverse: bool = False, frequency: int = 1000):
        self._value = value
        self._inverse = inverse
        self.pin = pin
        self.pwm = None
        if environment.are_pins_available():
            self.pwm = pwmio.PWMOut(pin, frequency=frequency)

    def deinit(self) -> None:
        self.pin = None
        if self.pwm:
            self.pin.deinit()

    # Turns the PWM fully on.
    def on(self):
        self.value = 1.0

    # Turns the PWM fully off.
    def off(self):
        self.value = 0.0

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: float):
        value = min(max(value, 0.0), 1.0)

        self._value = value

        if self.pwm:
            self.pwm.duty_cycle = int(MAX_DUTY * (1.0 - value if self._inverse else value))
