def execute():
    import validate.utils as utils

    # There is nothing much to do because utils.execute() uses reliable_runner
    # to execute the task when use_reliable_runner is set to True.
    utils.execute(lambda: None, use_reliable_runner=True)


if __name__ == '__main__':
    execute()
