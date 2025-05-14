import time
from collections.abc import Callable


def stop() -> bool:
    return False


def count_limiter(total: int) -> Callable[[], bool]:
    """
    Returns a function that returns true for the specified number of times
    it is called.
    """
    count: int = 0

    def func() -> bool:
        nonlocal count
        count += 1
        return count <= total

    return func


def time_limiter(seconds: float) -> Callable[[], bool]:
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
