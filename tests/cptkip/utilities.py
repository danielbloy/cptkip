import time
from typing import Callable


def value_flip(seconds: float, obj, changes: list[float]) -> Callable[[], bool]:
    """
    Similar to time limiter except at each of the given time points specified
    in the list changes, the value property of obj is inverted. This is useful
    for simulating button presses.
    """
    first = None

    def func() -> bool:
        nonlocal first
        now = time.time()
        if first is None:
            first = now

        elapsed = (now - first)
        if changes and elapsed >= changes[0]:
            obj.value = not obj.value
            del changes[0]

        return elapsed <= seconds

    return func


class FakeDigitalInOut:
    """
    Minimal stand-in for CircuitPython's digitalio.DigitalInOut so the "pins available"
    code paths can be exercised on a desktop. Counts deinit() calls.
    """

    def __init__(self, pin):
        self.pin = pin
        self.direction = None
        self.pull = None
        self.value = False
        self.deinit_count = 0

    def deinit(self) -> None:
        self.deinit_count += 1


class FakeDigitalio:
    """
    Minimal stand-in for the CircuitPython digitalio module.
    """
    DigitalInOut = FakeDigitalInOut

    class Direction:
        INPUT = "input"
        OUTPUT = "output"

    class Pull:
        UP = "up"
        DOWN = "down"


class FakePWMOut:
    """
    Minimal stand-in for CircuitPython's pwmio.PWMOut. Counts deinit() calls.
    """

    def __init__(self, pin, frequency: int = 500, duty_cycle: int = 0, variable_frequency: bool = False):
        self.pin = pin
        self.frequency = frequency
        self.duty_cycle = duty_cycle
        self.variable_frequency = variable_frequency
        self.deinit_count = 0

    def deinit(self) -> None:
        self.deinit_count += 1


class FakePwmio:
    """
    Minimal stand-in for the CircuitPython pwmio module.
    """
    PWMOut = FakePWMOut
