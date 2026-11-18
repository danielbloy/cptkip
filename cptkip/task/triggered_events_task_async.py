from asyncio import sleep
from time import monotonic

import cptkip.core.environment as environment
from cptkip.core.control import ASYNC_LOOP_SLEEP_INTERVAL
from cptkip.core.logging import debug

if environment.is_running_on_desktop():
    from typing import Any, Tuple, Callable, Awaitable


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
        events: list[
            Tuple[float] |
            Tuple[float, Any] |
            Tuple[float, Any, Callable[[Any], Awaitable[None]]]],
        begin: Callable[[], Awaitable[None]] | None = None,
        callback: Callable[[Any], Awaitable[None]] | None = None,
        end: Callable[[], Awaitable[None]] | None = None,
        continue_func: Callable[[], bool] | None = None) -> Callable[[], Awaitable[None]]:
    """
    Creates an asynchronous function that will monitor a triggerable function for as long
    as the continue_func returns true. When triggered, the events will start executing at
    the specified interval after the trigger is activated.

    Each event must specif at least one value and can specify up to three values:
    * The first value is the interval at which the event will be triggered.
    * The second value is the argument that will be passed to the event callback.
    * The third value is the event callback function.

    If any event does not specify an event callback function, then the generic callback
    parameter is used. If no argument is specified for the event, None is passed to the
    callback. If all events have an event callback specified, then callback is optional.
    Otherwise, callback is mandatory.

    There is also an optional begin function which will be called once when the trigger
    is activated and an optional end function that will be called once when the trigger is
    deactivated; which will occur at the specified number of seconds after the trigger has
    been activated.

    Once a trigger is activated, it will not be activated again until after it has expired
    and been deactivated. The trigger function is used to activate the trigger by returning
    True.

    :param trigger: Function that triggers when it returns True.
    :param events: The events to execute when the trigger is activated. Each event is a
        tuple with at least one value and up to three values. The first value is the
        interval, the second value is the value to provide to the event callback and the
        third value is the event callback function.
    :param begin: This is called once when the trigger is activated
    :param callback: If all events have a callback function specified, then callback is
        optional. Otherwise, it is mandatory and used for events with no event callback.
    :param end: This is called once when the trigger ends (or if it finishes early).
    :param continue_func: A function that returns whether to cancel the task or not.
    """

    # Loop through all events and if one of them does not have a function,
    # then error if func is not specific. This also validates that each event
    # contains a tuple.
    for event in events:
        if not isinstance(event, tuple) or len(event) > 3:
            raise ValueError("All events must be tuples with one to three elements")

        # First parameter must be a number
        if not isinstance(event[0], (int, float)):
            raise ValueError("First parameter of event must be a number")

        if len(event) < 3:
            if not callback:
                raise ValueError(
                    "Callback must be provided if any event does not provide a callback")
        else:
            if not callable(event[2]):
                raise ValueError("Event callbacks must be callable functions")

    async def handler() -> None:
        running = False
        remaining = []
        start_time = 0

        while not continue_func or continue_func():
            await sleep(ASYNC_LOOP_SLEEP_INTERVAL)

            if trigger() and not running:
                debug("Start running trigger event")

                remaining = events.copy()
                start_time = monotonic()
                running = True
                if begin:
                    await begin()

            if running and not remaining:
                debug("Stop running trigger event")

                running = False
                if end:
                    await end()

            if running:
                now = monotonic()
                diff = now - start_time
                # We are tolerant of the number of values in an event but the first
                # value must be a time.
                events_to_fire = [event for event in remaining if diff >= event[0]]

                for event in events_to_fire:

                    obj = None
                    func = None

                    if len(event) > 1:
                        obj = event[1]

                    if len(event) > 2:
                        func = event[2]

                    if not func:
                        func = callback

                    await func(obj)

                for event in events_to_fire:
                    remaining.remove(event)

        if end and running:
            await end()

    return handler
