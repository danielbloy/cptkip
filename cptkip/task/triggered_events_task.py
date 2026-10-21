from time import monotonic

import cptkip.core.environment as environment
from cptkip.core.logging import debug

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable
    from typing import Any, Tuple


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


# TODO: Should this have a reset?

def create(
        trigger: Callable[[], bool],
        events: list[Tuple[float, Any, Callable[[Any], None] | None]],
        begin: Callable[[], None] | None = None,
        func: Callable[[Any], None] | None = None,
        end: Callable[[], None] | None = None,
        continue_func: Callable[[], bool] | None = None) -> Callable[[], bool]:
    # TODO: Validate parameters
    #

    running = False
    remaining = []
    start_time = 0

    def handler() -> bool:
        nonlocal running, remaining, start_time

        carry_on = not continue_func or continue_func()
        if not carry_on:
            return False

        now = monotonic()

        if trigger() and not running:
            debug("Start running trigger events")

            remaining = events.copy()
            # TODO: Sort events based on time.

            start_time = monotonic()
            running = True
            if begin:
                begin()

        if running and not events:
            debug("Stop running trigger events")
            running = False
            if end:
                end()

        if running and func is not None:
            now = monotonic()
            diff = now - start_time
            events_to_fire = [event for event in remaining if diff >= event[0]]

            # TODO: Sort events based on time.

            for time, event, callback in events_to_fire:
                if not callback:
                    callback = func

                # TODO: Check for none.
                callback(event)

            for event in events_to_fire:
                remaining.remove(event)

            func()

        return True

    return handler
