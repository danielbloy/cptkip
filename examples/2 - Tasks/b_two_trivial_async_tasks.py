#
# This example runs two asynchronous tasks, each of which output a piece
# of text ('one' or 'two') at a defined interval of time (every 0.3
# seconds or every 0.5 seconds).
#
# An advantage of trivial tasks over periodic tasks tasks is that it uses
# less RAM. The disadvantage is the presence of drift.
#
# A disadvantage of asynchronous tasks over synchronous tasks is that
# it uses significantly more RAM due to the async library (approximately
# an extra 10 Kb).
#
# The disadvantage of this example over the periodic tasks example is
# that the functions one and two will "drift" from the desired
# frequencies as the next "output" is determined from now plus the
# desired interval whereas the periodic tasks example do not drift.
#

import asyncio
import time

import cptkip.core.logging as log
import cptkip.task.basic_runner_async as runner

log.set_log_level(log.INFO)

# Run the loop for 5 seconds
finish = time.monotonic() + 5


async def one() -> None:
    while time.monotonic() < finish:
        log.info(f"{time.monotonic()}: one")
        await asyncio.sleep(0.3)


async def two() -> None:
    while time.monotonic() < finish:
        log.info(f"{time.monotonic()}: two")
        await asyncio.sleep(0.5)


runner.run([one, two])
