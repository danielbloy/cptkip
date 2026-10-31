import asyncio

from cptkip.core.environment import is_running_on_desktop

if is_running_on_desktop():
    from typing import Callable, Awaitable


# TODO: Add tests for continue_func
# TODO: Implement continue_func
def run(*funcs: Callable[[], Awaitable[None]],
        continue_func: Callable[[], bool] | None = None) -> None:
    """
    Simply runs a list of functions and waits for them to finish.
    No error handling is performed. Tasks should play nicely and ensure they
    regularly sleep with at least:
        await asyncio.sleep(0)

    :param continue_func: A function that returns whether to cancel the task or not.
    """

    async def execute() -> None:
        # noinspection PyTypeChecker
        tasks: list[asyncio.Task] = [asyncio.create_task(func()) for func in funcs]

        await asyncio.gather(*tasks)

    asyncio.run(execute())
