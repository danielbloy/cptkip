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
