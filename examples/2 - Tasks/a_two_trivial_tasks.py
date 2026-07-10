#
# This example runs two synchronous tasks, each of which output a piece
# of text ('one' or 'two') at a defined interval of time (every 0.3
# seconds or every 0.5 seconds).
#
# An advantage of trivial tasks over periodic tasks is that it uses
# less RAM. The disadvantage is the presence of drift.
#
# An advantage of synchronous tasks over asynchronous tasks is that
# it uses significantly less RAM (approximately 10 Kb less).
#
# The disadvantage of this example over the periodic tasks example is
# that the functions one and two will "drift" from the desired
# frequencies as the next "output" is determined from now plus the
# desired interval whereas the periodic tasks example do not drift.
#

import time

import cptkip.core.logging as log
import cptkip.task.basic_runner as runner

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
