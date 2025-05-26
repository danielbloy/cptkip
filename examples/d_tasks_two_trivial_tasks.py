# The disadvantage of this example over the periodic tasks example is
# that the functions one and two will "drift" from the desired
# frequencies whereas the period tasks example will not.

import time

import cptkip.core.logging as log
import cptkip.core.memory as memory
import cptkip.task.basic_runner as runner

memory.report_memory_usage()

log.set_log_level(log.INFO)

# Run the loop for 5 seconds
finish = time.monotonic() + 5

next_one = 0


def one() -> bool:
    global next_one
    if time.monotonic() >= next_one:
        log.info(f"{time.monotonic()}: one")
        next_one = time.monotonic() + 0.3
    return time.monotonic() < finish


next_two = 0


def two() -> bool:
    global next_two
    if time.monotonic() >= next_two:
        log.info(f"{time.monotonic()}: two")
        next_two = time.monotonic() + 0.5
    return time.monotonic() < finish


runner.run([one, two])

memory.report_memory_usage_and_free()
