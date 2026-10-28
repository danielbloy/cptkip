import time
from typing import Callable


def stop() -> bool:
    return False


def duration_limiter(seconds: float) -> Callable[[], bool]:
    """
    Returns a function that returns true for the specified number of seconds
    after the first time it is called.
    """
    first = None

    def func() -> bool:
        nonlocal first
        now = time.time()
        if first is None:
            first = now
        return (now - first) <= seconds

    return func


def value_flip(seconds: float, obj, changes: list[float]) -> Callable[[], bool]:
    """
    Similar to time limiter except at each of the given time points specified
    in the list changes, the value property of obj is inverted. This is useful
    for simulating button presses.
    """
    first = None

    def func() -> bool:
        nonlocal first
        now = time.time()
        if first is None:
            first = now

        elapsed = (now - first)
        if changes and elapsed >= changes[0]:
            obj.value = not obj.value
            del changes[0]

        return elapsed <= seconds

    return func
