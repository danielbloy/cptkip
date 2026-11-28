from time import monotonic_ns

import cptkip.core.environment as environment
from cptkip.core.control import NS_PER_SECOND

if environment.is_running_on_desktop():
    from typing import Callable


def create(
        func: Callable[[], None],
        frequency: int = 0,
        continue_func: Callable[[], bool] | None = None,
        begin: Callable[[], None] | None = None,
        end: Callable[[], None] | None = None,
        initial_delay: float = 0.0) -> Callable[[], bool]:
    """
    Creates a function that will execute the given function at the specified frequency
    for as long as the continue_func returns true. The initial invocation of func can
    be delayed by setting an initial_delay. If a frequency of zero is provided then
    func will be executed as fast as possible. A frequency of less than zero is ignored.

    :param func: The function to call.
    :param frequency: The frequency to execute the function at. Zero indicates as
        fast as possible.
    :param continue_func: If specified, this will be periodically called to confirm
        the func should continue to be called.
    :param begin: If specified, this will be executed once at the beginning
        and before any initial delay. It always runs on the first invocation
        of the returned handler, even if continue_func would immediately
        return False - continue_func is not consulted until the invocation
        after begin has run. In that case end (if specified) will then run
        on the following invocation.
    :param end: If specified, this will be executed once at the end.
    :param initial_delay: If specified, this will delay the first invocation of
        func by the specified number of seconds. A value of less than zero is ignored.
    """

    # Integer division keeps the period exact: on CircuitPython floats are only
    # 30-bit, so (1 / frequency) * NS_PER_SECOND would drift (e.g. 3 Hz gave
    # 333_333_344 ns). A period of at least 1 ns prevents an endless catch-up loop
    # for absurdly high frequencies.
    interval_ns: int = 0
    if frequency > 0:
        interval_ns = max(1, int(NS_PER_SECOND // frequency))
    next_callback_ns: int = 0
    call_begin: bool = True
    call_end: bool = True

    def handler() -> bool:
        nonlocal call_begin, call_end, next_callback_ns

        if call_begin:
            if begin:
                begin()
            call_begin = False
            next_callback_ns = monotonic_ns() + int(max(initial_delay, 0.0) * NS_PER_SECOND)
            return True

        carry_on_looping = not continue_func or continue_func()
        if carry_on_looping:
            now = monotonic_ns()
            if now >= next_callback_ns:
                if frequency > 0:
                    # Skip any missed periods in one step rather than looping.
                    next_callback_ns += ((now - next_callback_ns) // interval_ns + 1) * interval_ns
                func()
            return True

        if end and call_end:
            call_end = False
            end()

        return False

    return handler
