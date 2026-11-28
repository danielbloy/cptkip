import time

import cptkip.core.memory as memory
from cptkip.task.basic_runner import run
from cptkip.task.limiters import count_limiter
from cptkip.task.memory_monitor_task import create


class TestMemoryMonitorTask:
    """
    The memory monitor task is not easy to test as it is designed to be
    a basic reporting tool, wrapping the existing memory functions. We
    therefore only perform basic testing. This resets the counters in
    memory, runs the task and validates that sample has been called.
    """

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
        run(task)
        assert left == 0
        assert count == 5

        left = 20
        count = 0
        run(task)
        assert left == 0
        assert count == 20

    def test_no_continue_func(self):
        """
        Validates that the task will run forever when no continue func is provided.
        """
        task = create(1, 1)
        for _ in range(1000):
            assert task()

    def test_always_samples_on_first_call(self):
        """
        Validates that memory monitor always samples on first call even if it
        immediately terminates.
        """
        memory.reset_memory_usage()

        task = create(1, 1, continue_func=lambda: False)
        assert not task()

        assert memory.peak_used_heap != 0
        assert memory.used_heap != 0
        assert memory.free_heap != 0
        assert memory.total_heap != 0

    def test_correctly_terminate(self):
        """
        Validates that memory monitor correct uses the continue_func.
        """
        task = create(1, 1, continue_func=count_limiter(1))
        assert task()
        assert not task()

        task = create(1, 1, continue_func=count_limiter(3))
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
        task = create(4, 1, continue_func=lambda: False)
        task()
        memory.reset_memory_usage()
        task()
        assert memory.peak_used_heap == 0
        assert memory.used_heap == 0
        assert memory.free_heap == 0
        assert memory.total_heap == 0

        # Wait a quarter second (and a bit) and sample again.
        time.sleep(0.26)
        task()

        assert memory.peak_used_heap != 0
        assert memory.used_heap != 0
        assert memory.free_heap != 0
        assert memory.total_heap != 0

        # Immediately call again and it wont sample.
        memory.reset_memory_usage()
        task()
        assert memory.peak_used_heap == 0
        assert memory.used_heap == 0
        assert memory.free_heap == 0
        assert memory.total_heap == 0

    def test_sample_and_reporting_limits(self):
        """
        Validates that using invalid values for sample and reporting get defaulted to 1.
        """
        # First validate that we do not get errors.
        task = create(0, 0, continue_func=lambda: False)
        task()

        task = create(-1, -1, continue_func=lambda: False)
        task()

        # Now validate the timing
        task = create(-1, -1, continue_func=lambda: False)
        task()
        memory.reset_memory_usage()
        task()
        assert memory.peak_used_heap == 0
        assert memory.used_heap == 0
        assert memory.free_heap == 0
        assert memory.total_heap == 0

        time.sleep(0.45)
        task()
        assert memory.peak_used_heap == 0
        assert memory.used_heap == 0
        assert memory.free_heap == 0
        assert memory.total_heap == 0

        time.sleep(0.45)
        task()
        assert memory.peak_used_heap == 0
        assert memory.used_heap == 0
        assert memory.free_heap == 0
        assert memory.total_heap == 0

        # Now tick over the 1-second boundary.
        time.sleep(0.11)
        task()
        assert memory.peak_used_heap != 0
        assert memory.used_heap != 0
        assert memory.free_heap != 0
        assert memory.total_heap != 0

    def test_fractional_frequency_reports_less_than_once_a_second(self, monkeypatch):
        """
        A fractional report frequency (e.g. 0.5 = every 2 seconds) must be honoured;
        previously frequencies were clamped to at least once per second.
        """
        import cptkip.task.memory_monitor_task as module
        reports = []
        monkeypatch.setattr(module, "report_memory_usage", lambda: reports.append(time.monotonic()))
        monkeypatch.setattr(module, "sample_memory_usage", lambda: None)

        finish = time.monotonic() + 1.3
        run(create(10, 0.5, continue_func=lambda: time.monotonic() < finish))
        assert len(reports) == 1  # Only the initial report within 1.3 seconds.

    def test_report_does_not_take_a_second_sample(self, monkeypatch):
        """
        report_memory_usage() samples itself, so a tick that reports must not also
        call sample_memory_usage().
        """
        import cptkip.task.memory_monitor_task as module
        calls = []
        monkeypatch.setattr(module, "report_memory_usage", lambda: calls.append("report"))
        monkeypatch.setattr(module, "sample_memory_usage", lambda: calls.append("sample"))

        create(1, 1)()
        assert calls == ["report"]
