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


# noinspection PyTypeChecker
class TestPeriodicTask:

    def test_using_default_values(self):
        """
        Creates a task using all the defaults (apart from the continue function).
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

    def test_frequency(self):
        """
        TODO
        """
        assert False

    def test_using_begin_func(self):
        """
        Validates the begin function is called once and only once before the function is called.
        """
        count: int = 0

        async def func() -> None:
            assert begin_count == 1
            nonlocal count
            count += 1

        begin_count: int = 0

        async def begin_func() -> None:
            assert count == 0
            nonlocal begin_count
            begin_count += 1

        task = create(func, continue_func=count_limiter(10), begin_func=begin_func)

        asyncio.run(task())
        assert count == 10
        assert begin_count == 1

    def test_using_end_func(self):
        """
        Validates the end function is called once and only once after the function is called.
        """
        count: int = 0

        async def func() -> None:
            assert end_count == 0
            nonlocal count
            count += 1

        end_count: int = 0

        async def end_func() -> None:
            assert count == 10
            nonlocal end_count
            end_count += 1

        task = create(func, continue_func=count_limiter(10), end_func=end_func)

        asyncio.run(task())
        assert count == 10
        assert end_count == 1

    def test_using_begin_and_end_funcs(self):
        """
        Validates the begin and end functions are called once and only once, before and after
        the function is called.
        """
        count: int = 0

        async def func() -> None:
            assert begin_count == 1
            assert end_count == 0
            nonlocal count
            count += 1

        begin_count: int = 0

        async def begin_func() -> None:
            assert count == 0
            assert end_count == 0
            nonlocal begin_count
            begin_count += 1

        end_count: int = 0

        async def end_func() -> None:
            assert begin_count == 1
            assert count == 10
            nonlocal end_count
            end_count += 1

        task = create(func, continue_func=count_limiter(10), begin_func=begin_func, end_func=end_func)

        asyncio.run(task())
        assert count == 10
        assert begin_count == 1
        assert end_count == 1

    def test_with_initial_delay(self):
        """
        TODO
        """
        assert False
