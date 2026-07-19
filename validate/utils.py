"""
This module contains all the setup and instrumentation code to assist executing
the on device validation and profiling. The only function you should need to use
is execute() as it bootstraps everything else.
"""

import traceback
from time import monotonic

import cptkip.config.configuration as config
from cptkip.core.environment import is_running_on_desktop
from cptkip.core.memory import report_memory_usage_and_free
from cptkip.core.memory import reset_memory_usage

# These are not available in CircuitPython.
if is_running_on_desktop():
    from collections.abc import Callable, Awaitable

RUNTIME = 4
SAMPLE_FREQUENCY = 10
REPORT_FREQUENCY = 4
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
            print("\nExecuting module {}".format(module))
            reset_memory_usage()
            print("Initial memory profile (before and after GC):")
            report_memory_usage_and_free()
            __start_profiling()
            print("Execute:")
            # noinspection PyUnresolvedReferences
            module.execute()
            __end_profiling()
            print("Final memory profile (before and after GC):")
            report_memory_usage_and_free()

            del module

        except MemoryError as err:
            print("Memory Error")
            traceback.print_exception(err)


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


finish = 0
continue_func = lambda: monotonic() < finish


def execute(
        task: Callable[[], None],
        runtime: int = RUNTIME,
        sample_frequency: int = SAMPLE_FREQUENCY,
        report_frequency: int = REPORT_FREQUENCY):
    """
    Executes a single task with basic instrumentation of RAM usage and number of
    execution cycles achieved. This is a utility function to make it easier to
    validate functionality without repeating the same time management code over
    and over.

    :param task - Called to execute the test
    :param runtime - The number of seconds to execute for
    :param sample_frequency - The number of memory samples per second.
    :param report_frequency - The number of times to report memory usage per second.
    """
    import cptkip.task.basic_runner as runner
    from cptkip.task import memory_monitor_task

    cycles = 0

    def update() -> bool:
        """
        Executes the task under test. This also tracks the number of cycles executed.
        """
        nonlocal cycles
        cycles += 1
        task()
        return continue_func()

    tasks = []
    if sample_frequency * report_frequency != 0:
        tasks.append(
            memory_monitor_task.create(
                sample_frequency,
                report_frequency,
                continue_func))

    tasks.append(update)  # We add the update function last so memory monitor is always first.

    global finish
    finish = monotonic() + runtime + 0.05  # ake sure we get the start AND finish reports.

    runner.run(tasks)
    print(f"Total number of cycles executed .. : {((cycles / runtime) // 100) / 10:,.1f} K/s")


def execute_async(
        task: Callable[[], Awaitable[None]],
        runtime: int = RUNTIME,
        sample_frequency: int = SAMPLE_FREQUENCY,
        report_frequency: int = REPORT_FREQUENCY):
    """
    This is an async version of execute(). It provides the same functionality but is adapted
    to use async/await syntax and the different style of tasks that are used by the async runner.

    :param task - Called to execute the test
    :param runtime - The number of seconds to execute for
    :param sample_frequency - The number of memory samples per second.
    :param report_frequency - The number of times to report memory usage per second.
    """
    import asyncio
    import cptkip.task.basic_runner_async as runner_async
    from cptkip.task import memory_monitor_task_async

    cycles = 0

    async def update() -> None:
        """
        Executes the task under test. This also tracks the number of cycles executed.
        """
        nonlocal cycles
        while continue_func():
            cycles += 1
            await task()
            await asyncio.sleep(0)

    tasks = []
    if sample_frequency * report_frequency != 0:
        tasks.append(
            memory_monitor_task_async.create(
                sample_frequency,
                report_frequency,
                continue_func))

    tasks.append(update)  # We add the update function last so memory monitor is always first.

    global finish
    finish = monotonic() + runtime + 0.05  # ake sure we get the start AND finish reports.

    runner_async.run(tasks)
    print(f"Total number of cycles executed .. : {((cycles / runtime) // 100) / 10:,.1f} K/s")
