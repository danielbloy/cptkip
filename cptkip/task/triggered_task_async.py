import asyncio
from time import monotonic

import cptkip.core.environment as environment
from cptkip.core.control import ASYNC_LOOP_SLEEP_INTERVAL
from cptkip.core.logging import debug

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable, Awaitable


class Triggerable:
    """Trivial implementation for a triggerable object."""
    triggered: bool


def create(
        triggerable: Triggerable,
        duration: float | int,
        begin: Callable[[], Awaitable[None]] | None = None,
        func: Callable[[], Awaitable[None]] | None = None,
        end: Callable[[], Awaitable[None]] | None = None,
        continue_func: Callable[[], bool] | None = None) -> Callable[[], Awaitable[None]]:
    """
    Creates an asynchronous function that will monitor a triggerable object for as long as the
    continue_func returns true. When triggered, and if func specified, func will be repeatedly
    called for the specified duration.

    There is also an optional begin function which will be called once when the trigger
    is activated and an optional end function that  will be called once when the trigger is
    deactivated; which will occurs as the specified number of seconds after the trigger has
    been activated.

    At least one of begin, func and end must be provided, but they need not all be specified.

    Once a trigger is activated, it will not be activated again until after it has expired
    and been deactivated. The triggerable object is used to activate the trigger via a
    "triggered" property.

    :param triggerable: Object that has a triggered property which will activate.
    :param duration: The duration that trigger lasts (i.e. the time between start and stop calls).
    :param begin: This is called once when the trigger is activated
    :param func: This is called once every cycle when triggered.
    :param end: This is called once when the trigger expires.
    :param continue_func: A function that returns whether to cancel the task or not.
    """

    if begin is None and func is None and end is None:
        raise ValueError("at least one of start, run or stop must be specified")

    async def handler() -> None:
        running = False
        stop_time = 0

        while not continue_func or continue_func():
            await asyncio.sleep(ASYNC_LOOP_SLEEP_INTERVAL)

            now = monotonic()

            if triggerable.triggered and not running:
                debug("Start running trigger event")
                stop_time = now + duration
                running = True
                if begin:
                    await begin()

            triggerable.triggered = False

            if running and now >= stop_time:
                debug("Stop running trigger event")
                running = False
                if end:
                    await end()

            if running and func is not None:
                debug("Sunning trigger event")
                await func()

    return handler
