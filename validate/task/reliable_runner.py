def execute():
    import validate.utils as utils

    # Tests the successful restarting of failed tasks.
    def task() -> bool:
        raise Exception("Manually raising exception")

    utils.execute(task, use_reliable_runner=True)


if __name__ == '__main__':
    execute()
