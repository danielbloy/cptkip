def execute():
    import validate.utils as utils

    # Tests the successful restarting of failed tasks: the task raises on its first
    # few calls (each is logged with a warning) and then succeeds. This will run
    # forever if the cancellation does not work.
    failures_wanted = 3
    calls = 0
    failures = 0

    def task() -> bool:
        nonlocal calls, failures
        calls += 1
        if failures < failures_wanted:
            failures += 1
            raise Exception("Manually raising exception")
        return True

    utils.execute(task, use_reliable_runner=True)

    assert failures == failures_wanted
    assert calls > failures_wanted, "the task was not rerun after raising"


if __name__ == '__main__':
    execute()
