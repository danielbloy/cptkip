import gc
from time import monotonic

import cptkip.task.basic_runner as runner
from cptkip.core.environment import is_running_on_desktop

sample_frequency = 10
report_frequency = 1
runtime = 4

# These are not available in CircuitPython.
if is_running_on_desktop():
    from collections.abc import Callable


def execute(task: Callable[[], None], monitor: bool = True):
    """
    Executes a single task with basic instrumentation of RAM usage and number of
    execution cycles achieved. This is a utility function to make it easier to
    validate functionality without repeating the same time management code over
    and over.
    """
    print("START ...... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")

    continue_func = lambda: monotonic() < finish
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
    if monitor:
        from cptkip.task import memory_monitor_task
        tasks.append(memory_monitor_task.create(sample_frequency, report_frequency, continue_func))

    tasks.append(update)

    finish = monotonic() + runtime + 0.05  # ake sure we get the start AND finish reports.

    runner.run(tasks)
    if monitor:
        from cptkip.core.memory import report_memory_usage
        report_memory_usage()
    print(f"CYCLES ..... : {(cycles // 100) / 10:,.1f} K")
    print("BEFORE GC .. : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")
    gc.collect()
    print("AFTER GC ... : Used:", gc.mem_alloc(), "bytes, Free:", gc.mem_free(), "bytes")
