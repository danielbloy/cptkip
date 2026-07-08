"""
This module contains all the setup and instrumentation code to assist executing
the on device validation and profiling. The only function you should need to use
is execute() as it bootstraps everything else.
"""
import gc
import time
import traceback

from cptkip.core.environment import is_running_on_desktop
from cptkip.config import configuration as config

# These are not available in CircuitPython.
if is_running_on_desktop():
    from collections.abc import Callable

RUNTIME = 1
SAMPLE_FREQUENCY = 10
REPORT_FREQUENCY = 1
PROFILE = False
PROFILE_TOP = 10

if hasattr(config, 'RUNTIME'):
    RUNTIME = config.RUNTIME

if hasattr(config, 'SAMPLE_FREQUENCY'):
    SAMPLE_FREQUENCY = config.SAMPLE_FREQUENCY

if hasattr(config, 'REPORT_FREQUENCY'):
    REPORT_FREQUENCY = config.REPORT_FREQUENCY

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
            execute(module.execute)
            del module

        except MemoryError as err:
            print("Memory Error")
            traceback.print_exception(err)


def execute(
        execute_func: Callable[[], None],
        runtime: int = RUNTIME,
        sample_frequency: int = SAMPLE_FREQUENCY,
        report_frequency: int = REPORT_FREQUENCY):
    """
    Instruments and executes the validation module, reporting all details out
    afterwards.

    A single Game instance is created with update() and draw() functions
    attached which count the number of cycles executed as well as terminating
    after the desired number of seconds. The memory usage is also tracked, which
    is expensive so the recording and reporting rate are configurable from defaults.

    @param execute_func - Called to execute the validation module.
    @param runtime - The number of seconds to execute for
    @param sample_frequency - The number of memory samples per second.
    @param report_frequency - The number of times to report memory usage per second.
    """
    sample_period = 1_000_000_000 // max(sample_frequency, 1)
    last_sample = 0

    reporting_period = 1_000_000_000 // max(report_frequency, 1)
    last_report = 0

    def monitor_ram(dt: float):
        """
        Samples and reports the memory usage at the required frequencies.
        """
        nonlocal last_sample, last_report
        now = time.monotonic_ns()

        sample = (now - last_sample) >= sample_period
        report = (now - last_report) >= reporting_period

        if sample:
            last_sample = now
            __sample_memory_usage()

        if report:
            last_report = now
            __report_memory_usage()

    update_cycles = 0

    def update(dt: float):
        nonlocal update_cycles
        update_cycles += 1

        if time.monotonic() > finish:
            game.terminate()

    # TODO: Add in limiter.

    if sample_frequency * report_frequency != 0:
        # TODO: game.add_update_func(monitor_ram)
        pass

    __reset_memory_usage()
    __start_profiling()
    finish = time.monotonic() + runtime + 0.05  # ake sure we get the start AND finish reports.
    execute_func()
    __end_profiling()

    print(f"Achieved {update_cycles / runtime:.2f} updates/s")

    # Free all memory and reset
    gc.collect()
    sample_period, last_sample, reporting_period, last_report = 0, 0, 0, 0
    monitor_ram(0)


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
