# This module contains utility functions for tracking and reporting how much RAM the
# system has available whilst it is running. Strictly speaking the memory sizes
# refer to the amount of heap RAM available, not total system RAM. Some of the system
# RAM is allocated to CircuitPython; the amount reserved is statically allocated and
# depends on the CircuitPython build used. See the following references:
#  * https://docs.circuitpython.org/en/latest/docs/library/gc.html#functions
#  * https://docs.circuitpython.org/en/latest/shared-bindings/memorymap/index.html
#
import gc

import cptkip.core.environment as environment
import cptkip.core.logging as log

__is_running_on_desktop: bool = environment.is_running_on_desktop()

peak_used_heap = 0
used_heap = 0
free_heap = 0
total_heap = 0


def reset_memory_usage() -> None:
    """
    Resets the internal counters to zero used when sampling. Units are MB on
    desktop and bytes on a microcontroller (see sample_memory_usage()).
    """
    global peak_used_heap, used_heap, free_heap, total_heap
    peak_used_heap = 0
    used_heap = 0
    free_heap = 0
    total_heap = 0


def sample_memory_usage() -> None:
    """
    Samples the memory usage statistics, storing them in the global counters.
    Values are in MB when running on desktop and in bytes when running on a
    microcontroller.
    """
    global peak_used_heap, used_heap, free_heap, total_heap

    if __is_running_on_desktop:
        import psutil
        stats = psutil.virtual_memory()  # returns a named tuple
        used_heap = stats.used // 1_048_576
        free_heap = stats.free // 1_048_576
        total_heap = stats.total // 1_048_576
    else:
        # noinspection PyUnresolvedReferences
        used_heap = gc.mem_alloc()
        # noinspection PyUnresolvedReferences
        free_heap = gc.mem_free()
        total_heap = used_heap + free_heap

    if used_heap > peak_used_heap:
        peak_used_heap = used_heap


def report_memory_usage() -> None:
    """
    Provides basic reporting of the memory usage. It performs a sample, prior to
    reporting.
    """
    sample_memory_usage()
    if __is_running_on_desktop:
        log.critical(
            "Heap details: Total:", total_heap, "MB, Peak:", peak_used_heap,
            "MB, Used:", used_heap, "MB, Free:", free_heap, "MB, Total:")
    else:
        # noinspection PyUnresolvedReferences
        log.critical(
            "Heap details: Total:", total_heap, "bytes, Peak:", peak_used_heap,
            "bytes, Used:", used_heap, "bytes, Free:", free_heap, "bytes")


def report_memory_usage_and_free() -> None:
    """
    Convenience function that reports memory usage, runs the garbage collector then
    runs the report again.
    """
    report_memory_usage()
    gc.collect()
    report_memory_usage()
