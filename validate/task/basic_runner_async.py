import asyncio


def execute():
    from time import monotonic
    import validate.utils as utils

    async def task():
        while True:
            await asyncio.sleep(0)

    # There is nothing much to do because utils.execute_async() uses basic_runner_async
    # to execute the task. This will run forever if the cancellation does not work,
    # so also check the runner stopped on time.
    start = monotonic()
    utils.execute_async(task)
    elapsed = monotonic() - start
    assert elapsed < utils.RUNTIME + 1, f"runner took {elapsed:.2f}s to stop"


if __name__ == '__main__':
    execute()
