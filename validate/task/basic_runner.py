def execute():
    import validate.utils as utils

    # There is nothing much to do because utils.execute() uses basic_runner to
    # execute the task. This will run forever if the cancellation does not work.
    utils.execute(lambda: True)


if __name__ == '__main__':
    execute()
