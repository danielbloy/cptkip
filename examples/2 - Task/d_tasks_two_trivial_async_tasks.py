# The disadvantage of this example over the periodic tasks example is
# that the functions one and two will "drift" from the desired
# frequencies whereas the period tasks example will not.

import asyncio
import time

import cptkip.core.logging as log
import cptkip.core.memory as memory
import cptkip.task.basic_runner_async as runner

memory.report_memory_usage()

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

memory.report_memory_usage_and_free()
