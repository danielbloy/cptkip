# This module contains utility functions for examining how much RAM the
# system has available whilst it is running.
import gc

import cptkip.core.environment as environment
import cptkip.core.log as log


def report_memory_usage(msg: str = ""):
    log.critical(f"MEMORY USAGE: {msg}")
    if environment.is_running_on_desktop():
        import psutil as psutil
        stats = psutil.virtual_memory()  # returns a named tuple
        total_ram = stats.total / 1_073_741_824
        free_ram = stats.free / 1_073_741_824
        used_ram = stats.used / 1_073_741_824
        log.critical(f"RAM: Used: {used_ram:.2f} GB, Free: {free_ram:.2f} GB, Total: {total_ram:.2f} GB")
    else:
        log.critical(f"HEAP: Allocated: {gc.mem_alloc()} bytes, Free: {gc.mem_free()} bytes")


def report_memory_usage_and_free(msg: str = ""):
    report_memory_usage(f"{msg} before gc")
    gc.collect()
    report_memory_usage(f"{msg} after gc")
