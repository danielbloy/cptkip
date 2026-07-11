def execute():
    import validate.utils as utils

    # There is nothing much to do because utils.execute() uses basic_runner
    # to execute the task.
    utils.execute(lambda: None)


if __name__ == '__main__':
    execute()
