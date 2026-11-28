def execute():
    import cptkip.core.memory as memory
    import validate.utils as utils

    async def task():
        pass

    # utils.execute_async() uses basic_runner_async to execute the task and uses the
    # async memory monitor to monitor it; check that the monitor actually sampled memory.
    memory.reset_memory_usage()
    utils.execute_async(task)
    assert memory.peak_used_heap > 0, "memory was not sampled"


if __name__ == '__main__':
    execute()
