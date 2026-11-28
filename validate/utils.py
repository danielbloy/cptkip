"""
This module contains all the setup and instrumentation code to assist executing
the on device validation and profiling. The only function you should need to use
is execute() as it bootstraps everything else.
"""

import traceback
from time import monotonic

import cptkip.config.configuration as config
from cptkip.core.environment import is_running_on_desktop, are_pins_available
from cptkip.core.memory import report_memory_usage_and_free
from cptkip.core.memory import reset_memory_usage

if is_running_on_desktop():
    from typing import Callable, Awaitable

RUNTIME = 4
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


class Skip(Exception):
    """
    Raised by a validation module to indicate it cannot run on this device (for
    example because the hardware it needs is not configured). The module is then
    reported as skipped rather than failed.
    """
    pass


def skip_unless(condition, reason: str) -> None:
    """
    Skips the current validation module (by raising Skip) unless condition is true.
    """
    if not condition:
        raise Skip(reason)


def require_pins(*pins) -> None:
    """
    Skips the current validation module if pins are available (i.e. on a device) but
    any of the given pins has not been configured. On a desktop there are no pins, so
    the module still runs against the desktop stand-ins.
    """
    if are_pins_available():
        for pin in pins:
            skip_unless(pin is not None, "required pin is not configured in config.py")


def _report_process_memory(label: str) -> None:
    """
    On a desktop, report this process's resident memory. The memory monitor reports
    system-wide RAM on a desktop, which says little about cptkip itself.
    """
    if is_running_on_desktop():
        import psutil
        rss = psutil.Process().memory_info().rss // 1024
        print(f"{label} process memory (RSS): {rss:,} KB")


def execute_modules(modules: list[object]) -> list:
    """
    Executes each of the modules in turn and prints a summary. This is expected to be
    used only by the top level validate scripts. A module that raises Skip is reported
    as skipped; any other exception is reported as a failure and the remaining
    modules still run.

    NOTE: Memory figures are cumulative: modules (and the cptkip modules they import)
    stay loaded after they run, so later modules include the memory of earlier ones.

    Returns a list of (module, status, detail) tuples, status being PASS, SKIP or FAIL.
    """
    results = []
    for module in modules:
        name = getattr(module, "__name__", str(module))
        print(f"\nExecuting module {name}")
        status = "PASS"
        detail = ""
        try:
            reset_memory_usage()
            print("Initial memory profile (before and after GC):")
            report_memory_usage_and_free()
            _report_process_memory("Initial")
            __start_profiling()
            print("Execute:")
            # noinspection PyUnresolvedReferences
            module.execute()
            __end_profiling()
            print("Final memory profile (before and after GC):")
            report_memory_usage_and_free()
            _report_process_memory("Final")

        except Skip as err:
            status = "SKIP"
            detail = str(err)
            print("SKIPPED:", detail)

        except Exception as err:
            status = "FAIL"
            detail = f"{type(err).__name__}: {err}"
            print("FAILED:", detail)
            traceback.print_exception(err)

        results.append((name, status, detail))

    print_summary(results)
    return results


def print_summary(results: list) -> None:
    """
    Prints a one line per module summary of the results from execute_modules().
    """
    print("\nValidation summary:")
    for name, status, detail in results:
        print(f"  {status} {name} {detail}")

    failed = len([r for r in results if r[1] == "FAIL"])
    skipped = len([r for r in results if r[1] == "SKIP"])
    print(f"{len(results) - failed - skipped} passed, {skipped} skipped, {failed} failed")


def exit_on_failure(results: list) -> None:
    """
    Exits with a non-zero status if any of the results failed, so CI notices.
    """
    if any(r[1] == "FAIL" for r in results):
        import sys
        sys.exit(1)


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
        current, peak = tracemalloc.get_traced_memory()
        print(f"tracemalloc current: {current:,} bytes, peak: {peak:,} bytes")
        tracemalloc.stop()


finish = 0
continue_func = lambda: monotonic() < finish


def _print_rate(cycles: int, start: float, label: str = "Total number of cycles executed") -> None:
    elapsed = max(monotonic() - start, 0.001)
    print(f"{label} .. : {cycles:,} in {elapsed:.2f}s, {((cycles / elapsed) // 100) / 10:,.1f} K/s")


def execute(
        task: Callable[[], None] | Callable[[], bool],
        runtime: int = RUNTIME,
        sample_frequency: int = SAMPLE_FREQUENCY,
        report_frequency: int = REPORT_FREQUENCY,
        use_reliable_runner: bool = False):
    """
    Executes a single task with basic instrumentation of RAM usage and number of
    execution cycles achieved. This is a utility function to make it easier to
    validate functionality without repeating the same time management code over
    and over. If task returns a boolean value, it is ignored.

    :param task - Called to execute the test
    :param runtime - The number of seconds to execute for
    :param sample_frequency - The number of memory samples per second.
    :param report_frequency - The number of times to report memory usage per second.
    :param use_reliable_runner - Use reliable_runner instead of basic_runner.
    """
    if use_reliable_runner:
        import cptkip.task.reliable_runner as runner
    else:
        import cptkip.task.basic_runner as runner
    from cptkip.task import memory_monitor_task

    cycles = 0

    def update() -> bool:
        """
        Executes the task under test. This also tracks the number of cycles executed.
        """
        nonlocal cycles
        cycles += 1
        result = task()
        if result is not None:
            return result

        return True

    tasks = []
    if sample_frequency * report_frequency != 0:
        tasks.append(
            memory_monitor_task.create(
                sample_frequency,
                report_frequency,
                continue_func))

    tasks.append(update)  # We add the update function last so memory monitor is always first.

    global finish
    start = monotonic()
    finish = start + runtime + 0.05  # Make sure we get the start AND finish reports.

    runner.run(*tasks, continue_func=continue_func)
    _print_rate(cycles, start)


def execute_async(
        task: Callable[[], Awaitable[None]],
        runtime: int = RUNTIME,
        sample_frequency: int = SAMPLE_FREQUENCY,
        report_frequency: int = REPORT_FREQUENCY,
        use_reliable_runner: bool = False):
    """
    This is an async version of execute(). It provides the same functionality but is adapted
    to use async/await syntax and the different style of tasks that are used by the async runner.
    As async tasks usually run as one long coroutine, the rate reported is the number of event
    loop cycles achieved (measured by a task that yields with sleep(0)), not task invocations.

    :param task - Called to execute the test
    :param runtime - The number of seconds to execute for
    :param sample_frequency - The number of memory samples per second.
    :param report_frequency - The number of times to report memory usage per second.
    :param use_reliable_runner - Use reliable_runner instead of basic_runner.
    """
    import asyncio
    if use_reliable_runner:
        import cptkip.task.reliable_runner_async as runner_async
    else:
        import cptkip.task.basic_runner_async as runner_async

    from cptkip.task import memory_monitor_task_async

    cycles = 0

    async def count_cycles() -> None:
        nonlocal cycles
        while continue_func():
            cycles += 1
            await asyncio.sleep(0)

    tasks = []
    if sample_frequency * report_frequency != 0:
        tasks.append(
            memory_monitor_task_async.create(
                sample_frequency,
                report_frequency,
                continue_func))

    tasks.append(count_cycles)
    tasks.append(task)  # We add the update function last so memory monitor is always first.

    global finish
    start = monotonic()
    finish = start + runtime + 0.05  # Make sure we get the start AND finish reports.

    runner_async.run(*tasks, continue_func=continue_func)
    _print_rate(cycles, start, "Total number of event loop cycles")
