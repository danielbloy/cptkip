#
# This example runs two synchronous tasks, each of which output a piece
# of text ('one' or 'two') at a defined interval of time (every 0.3
# seconds or every 0.5 seconds). These tasks are wrapped as periodic
# tasks to avoid drift.
#
# The cost of periodic tasks over trivial tasks is that it uses slightly
# more RAM but the payoff is the lack of drift.
#
# A disadvantage of asynchronous tasks over synchronous tasks is that
# it uses significantly more RAM due to the async library (approximately
# an extra 10 Kb).
#
# The advantage of this example over the trivial tasks example is
# that the functions one and two will not "drift" from the desired
# frequencies whereas in the trivial tasks example they will "drift".

import time

import cptkip.core.logging as log
import cptkip.task.basic_runner_async as runner
import cptkip.task.periodic_task_async as periodic_task

log.set_log_level(log.INFO)

# Run the loop for 5 seconds
finish = time.monotonic() + 5


def should_continue() -> bool:
    return time.monotonic() < finish


async def one() -> None:
    log.info(f"{time.monotonic()}: one")


async def two() -> None:
    log.info(f"{time.monotonic()}: two")


task_one = periodic_task.create(one, frequency=3, continue_func=should_continue)
task_two = periodic_task.create(two, frequency=2, continue_func=should_continue)

runner.run([task_one, task_two])
