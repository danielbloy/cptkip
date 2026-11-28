# This test is a bit of a bodge as the utils.execute() function wraps the passed in
# task to enforce a configured time limit. Therefore, not all the periodic_task
# functionality can be tested. This is fine as we are only really validating that
# it works on the device, the full functionality testing is done as part of tests.
def execute():
    import validate.utils as utils
    from cptkip.task.periodic_task import create

    task_count: int = 0
    begin_count: int = 0

    def task() -> None:
        nonlocal task_count
        task_count += 1

    # Executed once at the beginning and before any initial delay.
    def begin() -> None:
        nonlocal begin_count
        begin_count += 1

    task = create(task, frequency=3, continue_func=utils.continue_func, begin=begin,
                  initial_delay=1)

    utils.execute(task)

    assert begin_count == 1
    # 3Hz after a 1 second delay for the remaining ~3 seconds of a 4 second run
    # gives about 10 calls; allow some slack for slower devices and other runtimes.
    expected = 1 + 3 * (utils.RUNTIME - 1)
    assert expected - 2 <= task_count <= expected + 1, f"task_count {task_count}, expected about {expected}"


if __name__ == '__main__':
    execute()
