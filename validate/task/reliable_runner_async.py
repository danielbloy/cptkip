def execute():
    import validate.utils as utils

    # Tests the successful restarting of failed tasks.
    async def task():
        raise Exception("Manually raising exception")

    utils.execute_async(task, use_reliable_runner=True)


if __name__ == '__main__':
    execute()
