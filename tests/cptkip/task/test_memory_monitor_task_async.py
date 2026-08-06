import asyncio
from time import monotonic_ns

import cptkip.core.control as control
import cptkip.core.memory as memory
import tests.cptkip.utilities as utils
from cptkip.task.memory_monitor_task_async import create


class TestMemoryMonitorTask:
    """
    The memory monitor task is not easy to test as it is designed to be
    a basic reporting tool, wrapping the existing memory functions. We
    therefore only perform basic testing. This resets the counters in
    memory, runs the task and validates that sample has been called.
    """

    # noinspection PyTypeChecker
    def test_continue_func(self):
        """
        Validates that the continue function is used to restrict the number
        of times the task is run.
        """

        left = 5
        count = 0

        def count_down() -> bool:
            nonlocal left, count
            left -= 1
            count += 1
            return left > 0

        task = create(1, 1, continue_func=count_down)
        asyncio.run(task())
        assert left == 0
        assert count == 5

        left = 20
        count = 0
        asyncio.run(task())
        assert left == 0
        assert count == 20

    # noinspection PyTypeChecker
    def test_always_samples_on_first_call(self):
        """
        Validates that memory monitor always samples on first-call even if it
        immediately terminates.
        """
        memory.reset_memory_usage()

        task = create(1, 1, continue_func=utils.stop)
        asyncio.run(task())

        assert memory.peak_used_ram != 0
        assert memory.used_ram != 0
        assert memory.free_ram != 0
        assert memory.total_ram != 0

    # noinspection PyTypeChecker
    def test_correctly_terminate(self):
        """
        Validates that memory monitor correct uses the continue_func.
        """
        continue_func = utils.count_limiter(1)
        task = create(1, 1, continue_func=continue_func)
        asyncio.run(task())
        assert not continue_func()

        continue_func = utils.count_limiter(3)
        task = create(1, 1, continue_func=continue_func)
        asyncio.run(task())
        assert not continue_func()

        count = 5

        def count_down() -> bool:
            nonlocal count
            count -= 1
            return count > 0

        task = create(1, 1, continue_func=count_down)
        asyncio.run(task())
        assert count == 0

    # noinspection PyTypeChecker
    def test_samples_correctly(self):
        """
        Validates that memory monitor correctly samples at the desired rate.
        """

        count = 0
        end_time = 0
        first_sample = 0
        second_sample = 0
        done = False

        def tracker() -> bool:
            nonlocal count, end_time, first_sample, second_sample, done
            count += 1

            # First call always samples, so reset and immediately call again.
            # We also work out when the next samples should be.
            if count == 1:
                end_time = monotonic_ns() + control.NS_PER_SECOND + 1_000_000
                first_sample = monotonic_ns() + (control.NS_PER_SECOND // 2) + 100_000
                second_sample = monotonic_ns() + control.NS_PER_SECOND + 100_000
                memory.reset_memory_usage()
            elif count == 2:
                # Check we have not sampled
                assert memory.peak_used_ram == 0
                assert memory.used_ram == 0
                assert memory.free_ram == 0
                assert memory.total_ram == 0

            if monotonic_ns() > first_sample:
                first_sample += control.NS_PER_SECOND
                assert memory.peak_used_ram != 0
                assert memory.used_ram != 0
                assert memory.free_ram != 0
                assert memory.total_ram != 0
                memory.reset_memory_usage()

            if monotonic_ns() > second_sample:
                second_sample += control.NS_PER_SECOND
                done = True
                assert memory.peak_used_ram != 0
                assert memory.used_ram != 0
                assert memory.free_ram != 0
                assert memory.total_ram != 0
                memory.reset_memory_usage()

            return monotonic_ns() < end_time

        task = create(2, 1, continue_func=tracker)
        asyncio.run(task())
        assert done

    # noinspection PyTypeChecker
    def test_sample_and_reporting_limits(self):
        """
        Validates that using invalid values for sample and reporting get defaulted to 1.
        """
        # First validate that we do not get errors.
        task = create(0, 0, continue_func=utils.stop)
        task()

        task = create(-1, -1, continue_func=utils.stop)
        task()

        count = 0
        end_time = 0
        first_sample = 0
        done = False

        def tracker() -> bool:
            nonlocal count, end_time, first_sample, done
            count += 1

            # First call always samples, so reset and immediately call again.
            # We also work out when the next samples should be.
            if count == 1:
                end_time = monotonic_ns() + control.NS_PER_SECOND + 1_000_000
                first_sample = monotonic_ns() + control.NS_PER_SECOND + 100_000
                memory.reset_memory_usage()

            if monotonic_ns() > first_sample:
                first_sample += control.NS_PER_SECOND
                done = True
                assert memory.peak_used_ram != 0
                assert memory.used_ram != 0
                assert memory.free_ram != 0
                assert memory.total_ram != 0
                memory.reset_memory_usage()

            return monotonic_ns() < end_time

        # Now validate the timing
        task = create(-1, -1, continue_func=tracker)
        asyncio.run(task())
        assert done
