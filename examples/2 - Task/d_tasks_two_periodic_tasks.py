# The advantage of this example over the trivial tasks example is
# that the functions one and two will not "drift" from the desired
# frequencies whereas in the trivial tasks example they will "drift".

import time

import cptkip.core.logging as log
import cptkip.core.memory as memory
import cptkip.task.basic_runner as runner
import cptkip.task.periodic_task as periodic_task

memory.report_memory_usage()

log.set_log_level(log.INFO)

# Run the loop for 5 seconds
finish = time.monotonic() + 5


def should_continue() -> bool:
    return time.monotonic() < finish


def one() -> None:
    log.info(f"{time.monotonic()}: one")


def two() -> None:
    log.info(f"{time.monotonic()}: two")


task_one = periodic_task.create(one, frequency=3, continue_func=should_continue)
task_two = periodic_task.create(two, frequency=2, continue_func=should_continue)

runner.run([task_one, task_two])

memory.report_memory_usage_and_free()
