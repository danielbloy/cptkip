import asyncio

from cptkip.core.environment import is_running_on_desktop

if is_running_on_desktop():
    from typing import Callable, Awaitable


def run(*funcs: Callable[[], Awaitable[None]]) -> None:
    """
    Simply runs a list of functions and waits for them to finish.
    No error handling is performed. Tasks should play nicely and ensure they
    regularly sleep with at least:
        await asyncio.sleep(0)

    NOTE: This runner does not have a continue_func parameter as implementing support
          for it will complicate the code unnecessarily for cases where this is intended
          to be used.
    """

    async def execute() -> None:
        # noinspection PyTypeChecker
        tasks: list[asyncio.Task] = [asyncio.create_task(func()) for func in funcs]

        await asyncio.gather(*tasks)

    asyncio.run(execute())
