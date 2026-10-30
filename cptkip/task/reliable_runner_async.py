import asyncio

from cptkip.core.environment import is_running_on_desktop
from cptkip.core.logging import error, warn, info, stacktrace

# TODO: Validate
# TODO: Validate-performance

if is_running_on_desktop():
    from typing import Callable, Awaitable


def run(*funcs: Callable[[], Awaitable[None]],
        restart_on_exception: bool = True,
        continue_func: Callable[[], bool] | None = None) -> None:
    """

    Runs a list of functions and waits for them to finish, providing a configurable
    amount of error handling based on the passed in properties. The runner will
    execute for as long as continue_func returns True.

    By default, where a task errors with an exception, the runner will consider the
    function to have not completed and keep it in the list of functions to execute.
    If restart_on_exception is False, the runner will remove the function from the
    list of functions to execute.

    Functions should play nicely and ensure they regularly await with at least:
        await asyncio.sleep(0)

    :param restart_on_exception: If True, the runner will restart the task if it
      raises an exception.
    :param continue_func: A function that returns whether to cancel the task or not.
    """
    running = True

    def new_handler(task: Callable[[], Awaitable[None]]) -> Callable[[], Awaitable[None]]:
        """
        This wraps any task and provides the exception and completion handling
        such as restart as defined by the Runners properties.

        :param task: The task that is to be wrapped.
        """

        async def handler():

            while running:
                try:
                    # This sleep ensures the cancellation handler is the first to execute.
                    await asyncio.sleep(0)
                    await task()
                    return

                except asyncio.CancelledError:
                    error('Caught CancelledError exception for task -', task)
                    return

                except Exception as e:
                    warn('Exception raised by task', task, "-", e)
                    stacktrace(e)

                    if restart_on_exception:
                        warn('Rerunning task', task)

                    else:
                        return

        return handler

    async def cancellation_handler(tasks: list[asyncio.Task]) -> None:
        """
        The cancellation handler is only required if a continue_func was specified. If so,
        this just loops until the continue_func returns False.
        """
        if not continue_func:
            return

        nonlocal running
        while continue_func():
            await asyncio.sleep(0)

        # This stops the restarts
        running = False

        # Cancel all remaining tasks.
        info('Cancelling', len(tasks), 'tasks')
        for task in tasks:
            info('   ', task)
            task.cancel()

    async def execute() -> None:
        # noinspection PyTypeChecker
        tasks: list[asyncio.Task] = [
            asyncio.create_task(new_handler(func)()) for func in funcs
        ]

        await asyncio.gather(asyncio.create_task(cancellation_handler(tasks)), *tasks)

    asyncio.run(execute())
