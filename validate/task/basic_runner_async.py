def execute():
    import validate.utils as utils

    async def task():
        pass
    
    # There is nothing much to do because utils.execute_async() uses basic_runner_async
    # to execute the task.
    utils.execute_async(task)


if __name__ == '__main__':
    execute()
