import cptkip.core.environment as environment

if environment.is_running_on_desktop():
    from typing import Callable


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


def duration_limiter(seconds: float) -> Callable[[], bool]:
    """
    Returns a function that returns true for the specified number of seconds
    after the first time it is called.

    Uses time.monotonic() rather than time.time(): the wall clock can jump (e.g. NTP
    or RTC updates) and on CircuitPython time.time() only has whole-second resolution.
    """
    from time import monotonic
    first = None

    def func() -> bool:
        nonlocal first
        now = monotonic()
        if first is None:
            first = now
        return (now - first) <= seconds

    return func
