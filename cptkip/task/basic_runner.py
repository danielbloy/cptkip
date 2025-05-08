import asyncio

import cptkip.core.environment as environment

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable, Awaitable


def run(funcs: list[Callable[[], Awaitable[None]]]) -> None:
    """
    Simply runs a list of functions and waits for them to finish.
    No error handling is performed.
    """

    async def execute() -> None:
        tasks: list[asyncio.Task] = [asyncio.create_task(func()) for func in funcs]

        await asyncio.gather(*tasks)

    asyncio.run(execute())
