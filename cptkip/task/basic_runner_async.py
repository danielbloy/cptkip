import asyncio

from cptkip.core.environment import is_running_on_desktop

if is_running_on_desktop():
    from typing import Callable, Awaitable


# TODO: Add optional keep going function: continue_func: Callable[[], bool] | None = None
def run(*funcs: Callable[[], Awaitable[None]]) -> None:
    """
    Simply runs a list of functions and waits for them to finish.
    No error handling is performed. Tasks should play nicely and ensure they
    regularly sleep with at least:
        await asyncio.sleep(0)
    """

    async def execute() -> None:
        # noinspection PyTypeChecker
        tasks: list[asyncio.Task] = [asyncio.create_task(func()) for func in funcs]

        await asyncio.gather(*tasks)

    asyncio.run(execute())
