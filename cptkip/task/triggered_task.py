from time import monotonic

import cptkip.core.environment as environment
from cptkip.core.logging import debug

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable


class Trigger:
    """
    A simple trigger that automatically resets once read.
    """
    triggered: bool

    def __init__(self, triggered: bool) -> None:
        self.triggered = triggered

    def __call__(self) -> bool:
        result = self.triggered
        self.triggered = False
        return result


def create(
        trigger: Callable[[], bool],
        duration: float | int,
        begin: Callable[[], None] | None = None,
        func: Callable[[], None] | None = None,
        end: Callable[[], None] | None = None,
        continue_func: Callable[[], bool] | None = None) -> Callable[[], bool]:
    """
    Creates an asynchronous function that will monitor a triggerable function for as long as the
    continue_func returns true. When triggered, and if func specified, func will be repeatedly
    called for the specified duration.

    There is also an optional begin function which will be called once when the trigger
    is activated and an optional end function that  will be called once when the trigger is
    deactivated; which will occurs as the specified number of seconds after the trigger has
    been activated.

    At least one of begin, func and end must be provided, but they need not all be specified.

    Once a trigger is activated, it will not be activated again until after it has expired
    and been deactivated. The trigger function is used to activate the trigger by returning
    True.

    :param trigger: Function that triggers when it returns True.
    :param duration: The duration that trigger lasts (i.e. the time between start and stop calls).
    :param begin: This is called once when the trigger is activated
    :param func: This is called once every cycle when triggered.
    :param end: This is called once when the trigger expires.
    :param continue_func: A function that returns whether to cancel the task or not.
    """

    if begin is None and func is None and end is None:
        raise ValueError("at least one of start, run or stop must be specified")

    running = False
    stop_time = 0

    def handler() -> bool:
        nonlocal running, stop_time

        carry_on = not continue_func or continue_func()
        if not carry_on:
            return False

        now = monotonic()

        if trigger() and not running:
            debug("Start running trigger event")
            stop_time = now + duration
            running = True
            if begin:
                begin()

        if running and now >= stop_time:
            debug("Stop running trigger event")
            running = False
            if end:
                end()

        if running and func is not None:
            func()

        return True

    return handler
