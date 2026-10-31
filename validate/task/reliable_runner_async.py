def execute():
    import validate.utils as utils

    async def task():
        pass

    # There is nothing much to do because utils.execute_async() uses reliable_runner_async
    # to execute the task when use_reliable_runner is set to True.
    utils.execute_async(task, use_reliable_runner=True)


if __name__ == '__main__':
    execute()
