import asyncio
import time

import cptkip.core.environment as environment

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable, Awaitable

# TODO: move to control.py
NS_PER_SECOND = 1_000_000_000
SCHEDULER_INTERNAL_LOOP_RATIO = 32


def new_periodic_task(
        func: Callable[[], Awaitable[None]],
        frequency: int,
        run_func: Callable[[], bool] = None,
        initial_delay: float = 0.0) -> Callable[[], Awaitable[None]]:
    interval = 1 / frequency
    interval_ns: int = int(interval * NS_PER_SECOND)
    next_callback_ns = time.monotonic_ns()

    sleep_interval = interval / SCHEDULER_INTERNAL_LOOP_RATIO

    # TODO: initial delay

    async def handler() -> None:
        nonlocal next_callback_ns
        while not run_func or run_func():
            if time.monotonic_ns() >= next_callback_ns:
                next_callback_ns += interval_ns
                await func()

            await asyncio.sleep(sleep_interval)

    return handler
