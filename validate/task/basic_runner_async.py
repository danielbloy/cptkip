import asyncio


def execute():
    import validate.utils as utils

    async def task():
        while True:
            await asyncio.sleep(0)

    # There is nothing much to do because utils.execute_async() uses basic_runner_async
    # to execute the task. This will run forever if the cancellation does not work.
    utils.execute_async(task)


if __name__ == '__main__':
    execute()
