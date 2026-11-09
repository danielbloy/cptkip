#
# This example runs two synchronous tasks, each of which output a piece
# of text ('one' or 'two') at a defined interval of time (every 0.3
# seconds or every 0.5 seconds). The first will also throw an exception
# immediately after setting the time for the next output.
#

import time

import cptkip.core.logging as log
import cptkip.task.reliable_runner as runner

finish = time.monotonic() + 3

next_one = 0


def one() -> bool:
    global next_one
    if time.monotonic() >= next_one:
        log.info(f"{time.monotonic()}: one")
        next_one = time.monotonic() + 0.3
        raise Exception("Manually raising exception")
    return time.monotonic() < finish


next_two = 0


def two() -> bool:
    global next_two
    if time.monotonic() >= next_two:
        log.info(f"{time.monotonic()}: two")
        next_two = time.monotonic() + 0.5
    return time.monotonic() < finish


log.set_log_level(log.INFO)
runner.run(one, two, restart_on_exception=True)
