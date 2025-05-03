import asyncio

import cptkip.core.environment as environment
import cptkip.core.logging as logging

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable, Awaitable


def run(funcs: list[Callable[[], Awaitable[None]]]) -> None:
    """
    TODO: Comments
    """

    async def execute() -> None:
        tasks: list[asyncio.Task] = [asyncio.create_task(func()) for func in funcs]

        try:
            await asyncio.gather(*tasks)

        except asyncio.CancelledError:
            logging.error('Caught CancelledError exception cancelling tasks!')

        except Exception as e:
            logging.error(f'Caught the following exception cancelling tasks: {e}!')
            logging.stacktrace(e)

    try:
        asyncio.run(execute())
    except Exception as e:
        logging.error(f'run(): Exception caught running interactive: {e}')
        logging.stacktrace(e)
