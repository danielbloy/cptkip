import asyncio
import time

import cptkip.core.logging as log
import cptkip.core.memory as memory
import cptkip.task.runner as runner

memory.report_memory_usage()

log.set_log_level(log.INFO)

# Run the loop for 2 seconds
finish = time.monotonic() + 2


async def one() -> None:
    while time.monotonic() < finish:
        log.info("one")
        await asyncio.sleep(0)


async def two() -> None:
    while time.monotonic() < finish:
        log.info("two")
        await asyncio.sleep(0)


runner.run([one, two])

memory.report_memory_usage_and_free()
