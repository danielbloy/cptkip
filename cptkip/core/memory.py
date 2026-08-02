# This module contains utility functions for tracking and reporting how much RAM the
# system has available whilst it is running.
import gc

import cptkip.core.environment as environment
import cptkip.core.logging as log

# TODO: Strictly speaking the memory sizes are heap RAM available, not total RAM.
#       Review all of RAM monitoring and refine to make it clearer and even more useful.
# See: https://docs.circuitpython.org/en/latest/docs/library/gc.html#functions
# And: https://docs.circuitpython.org/en/latest/shared-bindings/memorymap/index.html
# And: https://picogame.makerclass.cz/memory/

__is_running_on_desktop: bool = environment.is_running_on_desktop()

peak_used_ram = 0
used_ram = 0
free_ram = 0
total_ram = 0


def reset_memory_usage() -> None:
    """
    Resets the internal counters to zero used when sampling. Units are MB on
    desktop and bytes on a microcontroller (see sample_memory_usage()).
    """
    global peak_used_ram, used_ram, free_ram, total_ram
    peak_used_ram = 0
    used_ram = 0
    free_ram = 0
    total_ram = 0


def sample_memory_usage() -> None:
    """
    Samples the memory usage statistics, storing them in the global counters.
    Values are in MB when running on desktop and in bytes when running on a
    microcontroller.
    """
    global peak_used_ram, used_ram, free_ram, total_ram

    if __is_running_on_desktop:
        import psutil
        stats = psutil.virtual_memory()  # returns a named tuple
        used_ram = stats.used // 1_048_576
        free_ram = stats.free // 1_048_576
        total_ram = stats.total // 1_048_576
    else:
        # noinspection PyUnresolvedReferences
        used_ram = gc.mem_alloc()
        # noinspection PyUnresolvedReferences
        free_ram = gc.mem_free()
        total_ram = used_ram + free_ram

    if used_ram > peak_used_ram:
        peak_used_ram = used_ram


def report_memory_usage() -> None:
    """
    Provides basic reporting of the memory usage. It performs a sample, prior to
    reporting.
    """
    sample_memory_usage()
    if __is_running_on_desktop:
        log.critical(
            "Peak:", peak_used_ram, "MB, Used:", used_ram, "MB, Free:", free_ram, "MB, Total:",
            total_ram, "MB")
    else:
        # noinspection PyUnresolvedReferences
        log.critical("Peak:", peak_used_ram, "bytes, Used:", used_ram, "bytes, Free:", free_ram,
                     "bytes, Total:",
                     total_ram, "bytes")


def report_memory_usage_and_free() -> None:
    """
    Convenience function that reports memory usage, runs the garbage collector then
    runs the report again.
    """
    report_memory_usage()
    gc.collect()
    report_memory_usage()
