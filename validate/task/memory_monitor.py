def execute():
    import validate.utils as utils

    # There is nothing much to do because utils.execute() uses basic_runner
    # to execute the task and uses memory_monitor to monitor it.
    utils.execute(lambda: None)


if __name__ == '__main__':
    execute()
