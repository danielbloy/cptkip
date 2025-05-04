import asyncio
import time

import cptkip.core.environment as environment
import cptkip.task.control as control

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable, Awaitable


def create(
        func: Callable[[], Awaitable[None]],
        frequency: int = 0,
        continue_func: Callable[[], bool] = None,
        begin_func: Callable[[], Awaitable[None]] = None,
        end_func: Callable[[], Awaitable[None]] = None,
        initial_delay: float = 0.0) -> Callable[[], Awaitable[None]]:
    """
    Creates an asynchronous function that will execute the given function at the
    specified frequency for as long as the continue_func returns true. The initial
    invocation of func can be delayed by setting an initial_delay. If a frequency
    of zero is provided then func will be executed as fast as possible. A frequency
    of less than zero is ignored.

    :param func: The function to call
    :param frequency: The frequency to execute the function at. Zero indicates as
        fast as possible.
    :param continue_func: If specified, this will be periodically called to confirm
        the func should continue to be called.
    :param begin_func: If specified, this will be executed once at the beginning
        and before any initial delay.
    :param end_func: If specified, this will be executed once at the end.
    :param initial_delay: If specified, this will delay the first invocation of
        func by the specified number of seconds. A value of less than zero is ignored.
    """

    interval = 0
    if frequency > 0:
        interval = 1 / frequency
    interval_ns: int = int(interval * control.NS_PER_SECOND)

    sleep_interval = interval / control.PERIODIC_LOOP_WAIT_RATIO

    async def handler() -> None:
        if begin_func:
            await begin_func()

        next_callback_ns = time.monotonic_ns() + int(max(initial_delay, 0.0) * control.NS_PER_SECOND)
        while not continue_func or continue_func():
            if time.monotonic_ns() >= next_callback_ns:
                next_callback_ns += interval_ns
                await func()

            await asyncio.sleep(sleep_interval)

        if end_func:
            await end_func()

    return handler
