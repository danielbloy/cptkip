import asyncio
import statistics
import time

import tests.cptkip.utilities as utils
from core.control import NS_PER_SECOND
from cptkip.task.periodic_task import create


# noinspection PyTypeChecker,PyUnresolvedReferences
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
        task = create(func, continue_func=utils.stop)

        asyncio.run(task())
        assert count == 0

        # Check that a single call occurs.
        task = create(func, continue_func=utils.count_limiter(1))

        asyncio.run(task())
        assert count == 1

        # Check that it gets called 10 times.
        count = 0
        task = create(func, continue_func=utils.count_limiter(10))

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

        count: int = 0

        async def func() -> None:
            now = time.monotonic_ns()
            nonlocal count, first, last, periods
            count += 1
            if first is None:
                first = now
                last = now
            else:
                periods.append((now - last) / NS_PER_SECOND)
                last = now

        def count_invocations() -> bool:
            nonlocal count
            return count != 11

        # With a frequency of 10 and allow for 11 invocations of fun(). This should span exactly
        # 1 second (with a small error margin). There are 11 invocations not 10 because the first
        # invocation is when the "timer" starts.
        task = create(func, frequency=10, continue_func=count_invocations)
        asyncio.run(task())

        duration = (last - first) / NS_PER_SECOND

        # The duration should be within 2%
        assert duration < 1.02
        assert duration > 0.98
        assert len(periods) == 10

        # The mean period should be within 2%
        assert statistics.mean(periods) < 0.102
        assert statistics.mean(periods) > 0.098

        # Use the smallest and largest periods should be within 30%
        periods.sort()
        assert periods[0] > 0.07
        assert periods[-1] < 0.13

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

        task = create(func, continue_func=utils.count_limiter(10), begin=begin_func)

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

        task = create(func, continue_func=utils.count_limiter(10), end=end_func)

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

        task = create(func, continue_func=utils.count_limiter(10), begin=begin_func, end=end_func)

        asyncio.run(task())
        assert count == 10
        assert begin_count == 1
        assert end_count == 1

    def test_with_initial_delay(self):
        """
        This validates the initial delay of the first call to func is measured.
        """

        async def func() -> None:
            nonlocal func_time
            func_time = time.monotonic_ns()

        async def begin_func() -> None:
            nonlocal begin_time
            begin_time = time.monotonic_ns()

        def continue_until_called() -> bool:
            nonlocal func_time
            return func_time is None

        begin_time = None
        func_time = None
        task = create(func, continue_func=continue_until_called, begin=begin_func, initial_delay=0.1)
        asyncio.run(task())

        duration = (func_time - begin_time) / NS_PER_SECOND
        assert duration > (0.1 * 0.9)  # within 10%
        assert duration < (0.1 * 1.1)  # within 10%

        begin_time = None
        func_time = None
        task = create(func, continue_func=continue_until_called, begin=begin_func, initial_delay=0.3)
        asyncio.run(task())

        duration = (func_time - begin_time) / NS_PER_SECOND
        assert duration > (0.3 * 0.9)  # within 10%
        assert duration < (0.3 * 1.1)  # within 10%

        begin_time = None
        func_time = None
        task = create(func, continue_func=continue_until_called, begin=begin_func, initial_delay=0.6)
        asyncio.run(task())

        duration = (func_time - begin_time) / NS_PER_SECOND
        assert duration > (0.6 * 0.9)  # within 10%
        assert duration < (0.6 * 1.1)  # within 10%
