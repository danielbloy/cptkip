import time

import cptkip.core.environment as environment

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable, Awaitable


def new_triggered_task(
        triggerable,
        duration: float,
        start: Callable[[], Awaitable[None]] = None,
        run: Callable[[], Awaitable[None]] = None,
        stop: Callable[[], Awaitable[None]] = None,
        cancel_func: Callable[[], bool] = never_terminate) -> Callable[[], Awaitable[None]]:
    """
    Returns an async task that will only invoke the functions start, stop and run if the
    trigger has been activated. The start function will be called once when the trigger
    is activated, run will be called as a normal loop task whilst the trigger is activated
    and stop will be called once when the trigger is deactivated; which will occurs as the
    specified number of seconds after the trigger has been activated.

    At least one of start, stop and run must be provided, but they need not all be specified.

    Once a trigger is activated, it will not be activated again until after it has expired
    and been deactivated. The triggerable object is used to activate the trigger via a
    "triggered" property.

    The returned task can be added to a Runner so it is called when triggered. The returned
    callback is itself wrapped in a loop_task so can be added to the Runner with add_task().

    :param triggerable: Object that has a triggered property which will activate.
    :param duration: The duration that trigger lasts (i.e. the time between start and stop calls).
    :param start: This is called once when the trigger is activated
    :param run: This is called once every cycle when triggered.
    :param stop: This is called once when the trigger expires.
    :param cancel_func: A function that returns whether to cancel the task or not.
    """

    if start is None and run is None and stop is None:
        raise ValueError("at least one of start, run or stop must be specified")

    running = False
    stop_time = 0

    async def handler() -> None:
        nonlocal running, stop_time

        now = time.monotonic()

        if triggerable.triggered and not running:
            debug("Start running trigger event")
            stop_time = now + duration
            running = True
            if start is not None:
                await start()

        triggerable.triggered = False

        if running and now >= stop_time:
            debug("Stop running trigger event")
            running = False
            if stop is not None:
                await stop()

        if running and run is not None:
            debug("Sunning trigger event")
            await run()

    return new_loop_task(handler, cancel_func)
