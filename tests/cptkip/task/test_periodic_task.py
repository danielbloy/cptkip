import asyncio
from collections.abc import Callable

from cptkip.task.periodic_task import create


def stop() -> bool:
    return False


def count_limiter(total: int) -> Callable[[], bool]:
    count: int = 0

    def func() -> bool:
        nonlocal count
        count += 1
        return count <= total

    return func


class TestPeriodicTask:

    def test_using_default_values(self):
        """
        Creates a task using all of the defaults (apart from the continue function)
        """
        count: int = 0

        async def func() -> None:
            nonlocal count
            count += 1

        # using a continue function that always returns false will result in fun() never being called.
        task = create(func, continue_func=stop)

        asyncio.run(task())
        assert count == 0

        # Check that a single call occurs.
        task = create(func, continue_func=count_limiter(1))

        asyncio.run(task())
        assert count == 1

        # Check that it gets called 10 times.
        count = 0
        task = create(func, continue_func=count_limiter(10))

        asyncio.run(task())
        assert count == 10
