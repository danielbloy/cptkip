import time
from collections.abc import Callable


def stop() -> bool:
    return False


def count_limiter(total: int) -> Callable[[], bool]:
    count: int = 0

    def func() -> bool:
        nonlocal count
        count += 1
        return count <= total

    return func


def time_limiter(seconds: float) -> Callable[[], bool]:
    first = None

    def func() -> bool:
        nonlocal first
        now = time.time()
        if first is None:
            first = now
        return (now - first) <= seconds

    return func
