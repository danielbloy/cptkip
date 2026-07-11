from time import monotonic_ns

import cptkip.core.environment as environment
from cptkip.core.memory import report_memory_usage
from cptkip.core.memory import sample_memory_usage

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable


def create(
        sample_frequency: int,
        report_frequency: int,
        continue_func: Callable[[], bool] | None = None) -> Callable[[], bool]:
    """
    Provides a relatively simple way to monitor the memory usage on the device over
    time. This monitoring function is susceptible to drift so is not suitable for
    high precision monitoring. The minimum sample and report frequency are 1 second.

    :param sample_frequency: The number of memory samples per second.
    :param report_frequency: The number of time to report memory usage per second.
    :param continue_func: If specified, this will be periodically called to confirm
        the func should continue to be called.
    """

    sample_period = 1_000_000_000 // max(sample_frequency, 1)
    last_sample = 0

    reporting_period = 1_000_000_000 // max(report_frequency, 1)
    last_report = 0

    def monitor() -> bool:
        """
        Samples and reports the memory usage at the required frequencies.
        """
        nonlocal last_sample, last_report
        now = monotonic_ns()

        sample = (now - last_sample) >= sample_period
        report = (now - last_report) >= reporting_period

        if sample:
            last_sample = now
            sample_memory_usage()

        if report:
            last_report = now
            report_memory_usage()

        return not continue_func or continue_func()

    return monitor
