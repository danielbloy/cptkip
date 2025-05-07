import asyncio
import statistics
import time
from collections.abc import Callable

from cptkip.task.control import NS_PER_SECOND
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


def time_limiter(seconds: float) -> Callable[[], bool]:
    first = None

    def func() -> bool:
        nonlocal first
        now = time.time()
        if first is None:
            first = now
        return (now - first) <= seconds

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
        Validates that the frequency is correct (roughly). We check the function is
        called the correct number of times (roughly) and that each time is equidistant
        in time.
        """
        periods = []
        first = None
        last = None

        async def func() -> None:
            now = time.monotonic_ns()
            nonlocal first, last, periods
            if first is None:
                first = now
                last = now
            else:
                periods.append(now - last)
                last = now

        # With a frequency of 50 and a time limit of 1 second, this should result in
        # approximately 50 calls. We can't use a count_limiter with frequency as the
        # continue function will get called multiple times per func call.
        task = create(func, frequency=50, continue_func=time_limiter(1))

        asyncio.run(task())
        print(periods)
        assert len(periods) == 49  # TODO: this needs to be a range
        assert statistics.mean(periods) == (1 / 50) * NS_PER_SECOND  # TODO: this needs to be a range.

        # TODO: What other counts will we need?

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
