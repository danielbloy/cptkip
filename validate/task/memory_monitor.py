def execute():
    import cptkip.core.memory as memory
    import validate.utils as utils

    # utils.execute() uses basic_runner to execute the task and uses memory_monitor
    # to monitor it; check that the monitor actually sampled memory.
    memory.reset_memory_usage()
    utils.execute(lambda: None)
    assert memory.peak_used_heap > 0, "memory was not sampled"


if __name__ == '__main__':
    execute()
