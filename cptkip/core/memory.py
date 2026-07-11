# This module contains utility functions for tracking and reporting how much RAM the
# system has available whilst it is running.
import gc

import cptkip.core.environment as environment
import cptkip.core.logging as log

__is_running_on_desktop: bool = environment.is_running_on_desktop()

peak_used_ram = 0
used_ram = 0
free_ram = 0
total_ram = 0


def reset_memory_usage() -> None:
    """
    Resets the internal counters to zero used when sampling
    """
    global peak_used_ram, used_ram, free_ram, total_ram
    peak_used_ram = 0
    used_ram = 0
    free_ram = 0
    total_ram = 0


def sample_memory_usage():
    """
    Samples the memory usage statistics, storing them in the global counters.
    """
    global peak_used_ram, used_ram, free_ram, total_ram

    if __is_running_on_desktop:
        import psutil as psutil
        stats = psutil.virtual_memory()  # returns a named tuple
        used_ram = stats.total / 1_048_576
        free_ram = stats.free / 1_048_576
        total_ram = stats.used / 1_048_576
    else:
        # noinspection PyUnresolvedReferences
        used_ram = gc.mem_alloc()
        # noinspection PyUnresolvedReferences
        free_ram = gc.mem_free()
        total_ram = used_ram + free_ram

    if used_ram > peak_used_ram:
        peak_used_ram = used_ram


def report_memory_usage():
    """
    Provides basic reporting of the memory usage. It performs a sample, prior to
    reporting.
    """
    sample_memory_usage()
    if __is_running_on_desktop:
        log.critical(
            f"Peak: {peak_used_ram:.2f} MB, Used: {used_ram:.2f} MB, Free: {free_ram:.2f} MB, Total: {total_ram:.2f} MB")
    else:
        # noinspection PyUnresolvedReferences
        log.critical(
            f"Peak: {peak_used_ram} bytes, Used: {used_ram} bytes, Free: {free_ram} bytes, Total: {total_ram} bytes")


def report_memory_usage_and_free():
    """
    Convenience function that reports memory usage, runs the garbage colector then
    runs the report again.
    """
    report_memory_usage()
    gc.collect()
    report_memory_usage()
