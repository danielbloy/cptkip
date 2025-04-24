# This module contains utility functions for examining how much RAM the
# system has available whilst it is running.

import gc

import cptkip.core.log as log


def report_memory_usage(msg: str = ""):
    log.critical(f"MEMORY USAGE: {msg}")
    log.critical(f"HEAP: Allocated: {gc.mem_alloc()} bytes, Free: {gc.mem_free()} bytes")


def report_memory_usage_and_free(msg: str = ""):
    report_memory_usage(f"{msg} before gc")
    gc.collect()
    report_memory_usage(f"{msg} after gc")
