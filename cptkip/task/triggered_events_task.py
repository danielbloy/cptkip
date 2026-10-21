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
        events: list[
            Tuple[float] | Tuple[float, Any] | Tuple[float, Any, Callable[[Any], None] | None]],
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

        if trigger() and not running:
            debug("Start running trigger events")

            remaining = events.copy()

            start_time = monotonic()
            running = True
            if begin:
                begin()

        if running and not remaining:
            debug("Stop running trigger events")
            running = False
            if end:
                end()

        if running:
            now = monotonic()
            diff = now - start_time
            # We are tolerant of the number of values in an event but the first
            # value must be a time.
            events_to_fire = [event for event in remaining if diff >= event[0]]

            for event in events_to_fire:

                obj = None
                callback = None

                if len(event) > 1:
                    obj = event[1]

                if len(event) > 2:
                    callback = event[2]

                if not callback:
                    callback = func

                if not callback:
                    raise ValueError("No callback provided")

                callback(obj)

            for event in events_to_fire:
                remaining.remove(event)

        return True

    return handler
