import asyncio

from cptkip.core.environment import is_running_on_microcontroller
from cptkip.core.log import set_log_level, debug, info, INFO
from cptkip.task.runner import Runner

if __name__ == '__main__':

    set_log_level(INFO)
    info(f'Is running on a microcontroller: {is_running_on_microcontroller()}')


    async def runs_forever_task():
        while True:
            debug("LOOP: runs_forever_task")
            await asyncio.sleep(2.0)


    async def completes_task():
        debug("START: completes_task")
        await asyncio.sleep(0.005)
        debug("FINISH: completes_task")


    async def raises_exception_task():
        debug("START: raises_exception_task")
        await asyncio.sleep(0.005)
        debug("EXCEPTION: raises_exception_task")
        raise Exception("Raised by task 3")


    runner = Runner()

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
        debug(f'Callback: i={i}')
        runner.cancel = i == 30


    runner.run(callback)
