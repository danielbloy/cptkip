import cptkip.core.environment as environment

MAX_DUTY = 65535

if environment.are_pins_available():
    import pwmio


class PwmPin:
    """
    Simple Pin using a value between 0.0 (fully off) and 1.0 (fully on) to control PWM on a
    Pin. This can be used to control the brightness in LEDS for example.
    """

    """
    :param value: The initial PWM value between 0.0 and 1.0.
    :param inverse: Set to True for connected devices where they are active on low.
                    An example would be the RGB LEDs on a Pimoroni Tiny 2040.
    :param frequency: The frequency of the PWM value.
    """

    def __init__(self, pin, value: float = 0.0, inverse: bool = False, frequency: int = 1000):
        self.pin = pin
        self._pwm = None
        if environment.are_pins_available():
            self._pwm = pwmio.PWMOut(pin, frequency=frequency)

        self.inverse = inverse
        self.value = value

    def deinit(self) -> None:
        if environment.are_pins_available():
            self._pwm.deinit()

        self._pwm = None

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

        if self._pwm:
            self._pwm.duty_cycle = int(MAX_DUTY * (1.0 - value if self.inverse else value))
