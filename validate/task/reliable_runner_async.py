def execute():
    import asyncio
    import validate.utils as utils

    # Tests the successful restarting of failed tasks: the task raises on its first
    # few runs (each is logged with a warning) and is then restarted and keeps
    # running until cancelled. This will run forever if the cancellation does not work.
    failures_wanted = 3
    starts = 0

    async def task():
        nonlocal starts
        starts += 1
        if starts <= failures_wanted:
            raise Exception("Manually raising exception")
        while True:
            await asyncio.sleep(0)

    utils.execute_async(task, use_reliable_runner=True)

    assert starts == failures_wanted + 1, f"task started {starts} times, expected {failures_wanted + 1}"


if __name__ == '__main__':
    execute()
