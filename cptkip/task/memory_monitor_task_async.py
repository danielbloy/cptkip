import asyncio
from time import monotonic_ns

import cptkip.core.control as control
import cptkip.core.environment as environment
from cptkip.core.memory import report_memory_usage
from cptkip.core.memory import sample_memory_usage

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable, Awaitable


def create(
        sample_frequency: int,
        report_frequency: int,
        continue_func: Callable[[], bool] | None = None) -> Callable[[], Awaitable[None]]:
    """
    Provides a relatively simple way to monitor the memory usage on the device over
    time. This monitoring function is susceptible to drift so is not suitable for
    high-precision monitoring. The minimum sample and report frequency are 1 second.

    :param sample_frequency: The number of memory samples per second.
    :param report_frequency: The number of times to report memory usage per second.
    :param continue_func: If specified, this will be periodically called to confirm
        the func should continue to be called.
    """

    sample_period = control.NS_PER_SECOND // max(sample_frequency, 1)
    last_sample = 0

    reporting_period = control.NS_PER_SECOND // max(report_frequency, 1)
    last_report = 0

    sleep_interval = (min(sample_period, reporting_period) / control.PERIODIC_LOOP_WAIT_RATIO) / control.NS_PER_SECOND

    async def monitor() -> None:
        """
        Samples and reports the memory usage at the required frequencies.
        """
        nonlocal last_sample, last_report
        while True:
            now = monotonic_ns()
            sample = (now - last_sample) >= sample_period
            report = (now - last_report) >= reporting_period

            if sample:
                last_sample = now
                sample_memory_usage()

            if report:
                last_report = now
                report_memory_usage()

            if continue_func and not continue_func():
                break

            await asyncio.sleep(sleep_interval)

    return monitor
