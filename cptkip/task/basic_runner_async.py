import asyncio

from cptkip.core.environment import is_running_on_desktop
from cptkip.core.logging import error, info

if is_running_on_desktop():
    from typing import Callable, Awaitable


# TODO: Add test that runner finishes when all tasks have finished even if cancellation_func has been provided
def run(*funcs: Callable[[], Awaitable[None]],
        continue_func: Callable[[], bool] | None = None) -> None:
    """
    Simply runs a list of functions and waits for them to finish. No error handling is
    performed, except for cancellation handling which is required for continue_func
    to work as it cancels the tasks. The runner will execute for as long as
    continue_func returns True and there are functions running.

    Functions should play nicely and ensure they regularly sleep with at least:
        await asyncio.sleep(0)

    :param continue_func: A function that returns whether to cancel the task or not.
    """

    def new_handler(task: Callable[[], Awaitable[None]]) -> Callable[[], Awaitable[None]]:
        """
        This wraps any task and provides the cancellation handling.
        """

        async def handler():
            try:
                # This sleep ensures the cancellation handler is the first to execute.
                await asyncio.sleep(0)
                await task()
                return

            except asyncio.CancelledError:
                error('Caught CancelledError exception for task -', task)
                return

        return handler

    async def cancellation_handler(tasks: list[asyncio.Task]) -> None:
        """
        The cancellation handler is only required if a continue_func was specified. If so,
        this just loops until the continue_func returns False.
        """
        if not continue_func:
            return

        while continue_func():
            await asyncio.sleep(0)

        # Cancel all remaining tasks.
        info('Cancelling', len(tasks), 'tasks')
        for task in tasks:
            info('   ', task)
            task.cancel()

    async def execute() -> None:
        # noinspection PyTypeChecker
        tasks: list[asyncio.Task] = [asyncio.create_task(new_handler(func)()) for func in funcs]

        await asyncio.gather(asyncio.create_task(cancellation_handler(tasks)), *tasks)

    asyncio.run(execute())
