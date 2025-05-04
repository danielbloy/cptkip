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
    interval = 0
    if frequency > 0:
        interval = 1 / frequency
    interval_ns: int = int(interval * control.NS_PER_SECOND)

    sleep_interval = interval / control.PERIODIC_LOOP_WAIT_RATIO

    async def handler() -> None:
        if begin_func:
            await begin_func()

        next_callback_ns = time.monotonic_ns() + int(initial_delay * control.NS_PER_SECOND)
        while not continue_func or continue_func():
            if time.monotonic_ns() >= next_callback_ns:
                next_callback_ns += interval_ns
                await func()

            await asyncio.sleep(sleep_interval)

        if end_func:
            await end_func()

    return handler
