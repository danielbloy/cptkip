import asyncio

import cptkip.core.environment as environment
import cptkip.core.logging as log
import cptkip.core.memory as memory
import cptkip.task.runner as tasks

if __name__ == '__main__':

    memory.report_memory_usage()

    log.set_log_level(log.CRITICAL)
    log.info(f'Is running on a microcontroller: {environment.is_running_on_microcontroller()}')


    async def runs_forever_task():
        while True:
            log.debug("LOOP: runs_forever_task")
            await asyncio.sleep(2.0)


    async def completes_task():
        log.debug("START: completes_task")
        await asyncio.sleep(0.005)
        log.debug("FINISH: completes_task")


    async def raises_exception_task():
        log.debug("START: raises_exception_task")
        await asyncio.sleep(0.005)
        log.debug("EXCEPTION: raises_exception_task")
        raise Exception("Raised by task 3")


    runner = tasks.Runner()

    runner.restart_on_completion = True
    runner.restart_on_exception = True
    runner.cancel_on_exception = False

    runner.add_task(runs_forever_task)
    runner.add_task(completes_task)
    runner.add_task(raises_exception_task)

    i: int = 0


    async def callback() -> None:
        global i
        i += 1
        log.debug(f'Callback: i={i}')
        runner.cancel = i == 30


    runner.run(callback)

    memory.report_memory_usage_and_free()
