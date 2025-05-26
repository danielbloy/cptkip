import time

import cptkip.core.control as control
import cptkip.core.environment as environment

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable


def create(
        func: Callable[[], None],
        frequency: int = 0,
        continue_func: Callable[[], bool] = None,
        begin: Callable[[], None] = None,
        end: Callable[[], None] = None,
        initial_delay: float = 0.0) -> Callable[[], bool]:
    """
    Creates a function that will execute the given function at the
    specified frequency for as long as the continue_func returns true. The initial
    invocation of func can be delayed by setting an initial_delay. If a frequency
    of zero is provided then func will be executed as fast as possible. A frequency
    of less than zero is ignored.

    :param func: The function to call.
    :param frequency: The frequency to execute the function at. Zero indicates as
        fast as possible.
    :param continue_func: If specified, this will be periodically called to confirm
        the func should continue to be called.
    :param begin: If specified, this will be executed once at the beginning
        and before any initial delay.
    :param end: If specified, this will be executed once at the end.
    :param initial_delay: If specified, this will delay the first invocation of
        func by the specified number of seconds. A value of less than zero is ignored.
    """

    interval = 0
    if frequency > 0:
        interval = 1 / frequency
    interval_ns: int = int(interval * control.NS_PER_SECOND)
    next_callback_ns: int = 0
    begin_called: bool = False

    def handler() -> bool:
        nonlocal begin_called, next_callback_ns
        if not begin_called:
            if begin:
                begin()
            begin_called = True
            next_callback_ns = time.monotonic_ns() + int(max(initial_delay, 0.0) * control.NS_PER_SECOND)
            return True

        carry_on_looping = not continue_func or continue_func()
        if carry_on_looping:
            now = time.monotonic_ns()
            if now >= next_callback_ns:
                if frequency > 0:
                    while now >= next_callback_ns:
                        next_callback_ns += interval_ns
                func()
            return True

        if end:
            end()

        return False

    return handler
