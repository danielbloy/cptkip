# This test is a bit of a bodge as the utils.execute_async() function wraps the passed in
# task to enforce a configured time limit. Therefore, not all the periodic_task_async
# functionality can be tested. This is fine as we are only really validating that it
# works on the device, the full functionality testing is done as part of tests.
def execute():
    import validate.utils as utils
    import cptkip.task.periodic_task_async as periodic_task

    task_count: int = 0
    begin_count: int = 0

    async def task() -> None:
        nonlocal task_count
        task_count += 1

    # Executed once at the beginning and before any initial delay.
    async def begin() -> None:
        nonlocal begin_count
        begin_count += 1

    periodic_task = periodic_task.create(
        task, frequency=3, continue_func=utils.continue_func, begin=begin, initial_delay=1)

    utils.execute_async(periodic_task)

    assert begin_count == 1
    assert task_count > 1


if __name__ == '__main__':
    execute()
