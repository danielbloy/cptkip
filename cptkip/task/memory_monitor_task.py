from time import monotonic_ns

import cptkip.core.environment as environment
from cptkip.core.control import NS_PER_SECOND
from cptkip.core.memory import report_memory_usage
from cptkip.core.memory import sample_memory_usage

if environment.is_running_on_desktop():
    from typing import Callable


def create(
        sample_frequency: float,
        report_frequency: float,
        continue_func: Callable[[], bool] | None = None) -> Callable[[], bool]:
    """
    Provides a relatively simple way to monitor the memory usage on the device over
    time. This monitoring function is susceptible to drift so is not suitable for
    high-precision monitoring.

    Frequencies may be fractional to sample or report less than once per second,
    e.g. report_frequency=1/60 reports once a minute. A frequency of zero or less
    defaults to once per second.

    :param sample_frequency: The number of memory samples per second.
    :param report_frequency: The number of times to report memory usage per second.
    :param continue_func: If specified, this will be periodically called to confirm
        the func should continue to be called.
    """

    sample_period = _period_ns(sample_frequency)
    last_sample = 0

    reporting_period = _period_ns(report_frequency)
    last_report = 0

    def monitor() -> bool:
        """
        Samples and reports the memory usage at the required frequencies.
        """
        nonlocal last_sample, last_report
        now = monotonic_ns()

        sample = (now - last_sample) >= sample_period
        report = (now - last_report) >= reporting_period

        if report:
            # report_memory_usage() takes a sample itself, so this also counts as one.
            last_report = now
            last_sample = now
            report_memory_usage()
        elif sample:
            last_sample = now
            sample_memory_usage()

        return not continue_func or continue_func()

    return monitor


def _period_ns(frequency: float) -> int:
    """
    Converts a frequency (per second, may be fractional) to a period in nanoseconds.
    Integer frequencies give an exact period; zero or less defaults to one second.
    """
    if frequency <= 0:
        return NS_PER_SECOND
    return max(1, int(NS_PER_SECOND // frequency))
