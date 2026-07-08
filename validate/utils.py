"""
This module contains all the setup and instrumentation code to assist executing
the on device validation and profiling. The only function you should need to use
is execute() as it bootstraps everything else.
"""
import gc
import traceback

import cptkip.config.configuration as config
from cptkip.core.environment import is_running_on_desktop

# These are not available in CircuitPython.
if is_running_on_desktop():
    pass

PROFILE = False
PROFILE_TOP = 10

if hasattr(config, 'PROFILE'):
    PROFILE = config.PROFILE

if hasattr(config, 'PROFILE_TOP'):
    PROFILE_TOP = config.PROFILE_TOP


def execute_modules(modules: list[object]):
    """
    Executes each of the modules in turn. This is expected to be used only by the
    top level validate scripts.
    """
    for module in modules:
        try:
            print("Executing module {}".format(module))
            __reset_memory_usage()
            __start_profiling()
            module.execute()
            __end_profiling()

            # Free all memory and reset
            gc.collect()

            del module

        except MemoryError as err:
            print("Memory Error")
            traceback.print_exception(err)


__peak_used_ram = 0
__used_ram = 0
__free_ram = 0
__total_ram = 0


def __reset_memory_usage():
    global __peak_used_ram, __used_ram, __free_ram, __total_ram
    __peak_used_ram = 0
    __used_ram = 0
    __free_ram = 0
    __total_ram = 0


def __sample_memory_usage():
    global __peak_used_ram, __used_ram, __free_ram, __total_ram

    if is_running_on_desktop():
        import psutil as psutil
        stats = psutil.virtual_memory()  # returns a named tuple
        __used_ram = stats.total / 1_048_576
        __free_ram = stats.free / 1_048_576
        __total_ram = stats.used / 1_048_576
    else:
        __used_ram = gc.mem_alloc()
        __free_ram = gc.mem_free()
        __total_ram = __used_ram + __free_ram

    if __used_ram > __peak_used_ram:
        __peak_used_ram = __used_ram


def __report_memory_usage():
    if is_running_on_desktop():
        print(
            f"Peak: {__peak_used_ram:.2f} MB, Used: {__used_ram:.2f} MB, Free: {__free_ram:.2f} MB, Total: {__total_ram:.2f} MB")
    else:
        print(
            f"Peak: {__peak_used_ram} bytes, Used: {__used_ram} bytes, Free: {__free_ram} bytes, Total: {__total_ram} bytes")


def __start_profiling():
    # See: https://docs.python.org/3/library/tracemalloc.html
    # And: https://stackoverflow.com/questions/552744/how-do-i-profile-memory-usage-in-python
    if is_running_on_desktop() and PROFILE:
        import tracemalloc
        tracemalloc.start()


def __end_profiling(top: int = PROFILE_TOP):
    if is_running_on_desktop() and PROFILE:
        import tracemalloc
        snapshot = tracemalloc.take_snapshot()
        top_stats = snapshot.statistics('lineno')
        print(f"[ Top {top} ]")
        for stat in top_stats[:top]:
            print(stat)
