def execute():
    import validate.utils as utils
    from cptkip.task.triggered_task_async import create, Trigger

    begin_count: int = 0
    func_count: int = 0
    end_count: int = 0

    # Executed once at the beginning of the trigger.
    async def begin() -> None:
        nonlocal begin_count
        begin_count += 1

    # Executed repeatedly whilst triggered
    async def func() -> None:
        nonlocal func_count
        func_count += 1

    # Executed once at the end of the trigger.
    async def end() -> None:
        nonlocal end_count
        end_count += 1

    trigger = Trigger(True)
    task = create(trigger, 0.5, begin=begin, func=func, end=end, continue_func=utils.continue_func)

    utils.execute_async(task)

    assert begin_count == 1
    assert func_count > 1
    assert end_count == 1


if __name__ == '__main__':
    execute()
