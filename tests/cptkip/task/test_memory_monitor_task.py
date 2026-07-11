import time

import cptkip.core.memory as memory
import tests.cptkip.utilities as utils
from cptkip.task.memory_monitor_task import create


class TestMemoryMonitorTask:
    """
    The memory monitor task is not easy to test as it is designed to be
    a basic reporting tool, wrapping the existing memory functions. We
    therefore only perform basic testing. This resets the counters in
    memory, runs the task and validates that sample has been called.
    """

    # TODO: Add test for continue_func.

    def test_always_samples_on_first_call(self):
        """
        Validates that memory monitor always samples on first call even if it
        immediately terminates.
        """
        memory.reset_memory_usage()

        task = create(1, 1, continue_func=utils.stop)
        assert not task()

        assert memory.peak_used_ram != 0
        assert memory.used_ram != 0
        assert memory.free_ram != 0
        assert memory.total_ram != 0

    def test_correctly_terminate(self):
        """
        Validates that memory monitor correct uses the continue_func.
        """
        task = create(1, 1, continue_func=utils.count_limiter(1))
        assert task()
        assert not task()

        task = create(1, 1, continue_func=utils.count_limiter(3))
        assert task()
        assert task()
        assert task()
        assert not task()

    def test_samples_correctly(self):
        """
        Validates that memory monitor correctly samples at the desired rate. We use the fact
        that memory monitor will continue to sample even if the continue_func returns False.
        """
        memory.reset_memory_usage()

        # First call always samples, so reset and immediately call again. This should not sample.
        task = create(4, 1, continue_func=utils.stop)
        task()
        memory.reset_memory_usage()
        task()
        assert memory.peak_used_ram == 0
        assert memory.used_ram == 0
        assert memory.free_ram == 0
        assert memory.total_ram == 0

        # Wait a quarter second (and a bit) and sample again.
        time.sleep(0.26)
        task()

        assert memory.peak_used_ram != 0
        assert memory.used_ram != 0
        assert memory.free_ram != 0
        assert memory.total_ram != 0

        # Immediately call again and it wont sample.
        memory.reset_memory_usage()
        task()
        assert memory.peak_used_ram == 0
        assert memory.used_ram == 0
        assert memory.free_ram == 0
        assert memory.total_ram == 0

    def test_sample_and_reporting_limits(self):
        """
        Validates that using invalid values for sample and reporting get defaulted to 1.
        """
        # First validate that we do not get errors.
        task = create(0, 0, continue_func=utils.stop)
        task()

        task = create(-1, -1, continue_func=utils.stop)
        task()

        # Now validate the timing
        task = create(-1, -1, continue_func=utils.stop)
        task()
        memory.reset_memory_usage()
        task()
        assert memory.peak_used_ram == 0
        assert memory.used_ram == 0
        assert memory.free_ram == 0
        assert memory.total_ram == 0

        time.sleep(0.45)
        task()
        assert memory.peak_used_ram == 0
        assert memory.used_ram == 0
        assert memory.free_ram == 0
        assert memory.total_ram == 0

        time.sleep(0.45)
        task()
        assert memory.peak_used_ram == 0
        assert memory.used_ram == 0
        assert memory.free_ram == 0
        assert memory.total_ram == 0

        # Now tick over the 1-second boundary.
        time.sleep(0.11)
        task()
        assert memory.peak_used_ram != 0
        assert memory.used_ram != 0
        assert memory.free_ram != 0
        assert memory.total_ram != 0
