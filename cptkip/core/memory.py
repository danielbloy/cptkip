# This module contains utility functions for examining how much RAM the
# system has available whilst it is running.
import gc

import cptkip.core.environment as environment
import cptkip.core.logging as log


def report_memory_usage():
    if environment.is_running_on_desktop():
        import psutil as psutil
        stats = psutil.virtual_memory()  # returns a named tuple
        total_ram = stats.total / 1_048_576
        free_ram = stats.free / 1_048_576
        used_ram = stats.used / 1_048_576
        log.critical(f"Used: {used_ram:.2f} MB, Free: {free_ram:.2f} MB, Total: {total_ram:.2f} MB")
    else:
        log.critical(f"Used: {gc.mem_alloc()} bytes, Free: {gc.mem_free()} bytes")


def report_memory_usage_and_free():
    report_memory_usage()
    gc.collect()
    report_memory_usage()
