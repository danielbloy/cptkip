#
# This example runs two asynchronous tasks, each of which output a piece
# of text ('one' or 'two') at a defined interval of time (every 0.3
# seconds or every 0.5 seconds). The first will also throw an exception
# immediately after setting the time for the next output.
#

import asyncio
import time

import cptkip.core.logging as log
import cptkip.task.reliable_runner_async as runner

finish = time.monotonic() + 3

next_one = 0


async def one() -> None:
    while time.monotonic() < finish:
        log.info(f"{time.monotonic()}: one")
        await asyncio.sleep(0.3)
        raise Exception("Manually raising exception")


next_two = 0


async def two() -> None:
    while time.monotonic() < finish:
        log.info(f"{time.monotonic()}: two")
        await asyncio.sleep(0.5)


log.set_log_level(log.INFO)
runner.run(one, two, restart_on_exception=True)
