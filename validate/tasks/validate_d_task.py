def execute():
    import time

    import cptkip.core.logging as log
    import cptkip.task.basic_runner as runner
    import cptkip.task.periodic_task as periodic_task

    log.set_log_level(log.INFO)

    one_count: int = 0
    two_count: int = 0
    begin_count: int = 0
    end_count: int = 0

    # Run the loop for 5 seconds
    finish = time.monotonic() + 2

    def should_continue() -> bool:
        return time.monotonic() < finish

    def one() -> None:
        nonlocal one_count
        one_count += 1

    def two() -> None:
        nonlocal two_count
        two_count += 1

    # Executed once at the beginning and before any initial delay.
    def begin() -> None:
        nonlocal begin_count
        begin_count += 1

    # Executed once at the end.
    def end() -> None:
        nonlocal end_count
        end_count += 1

    task_one = periodic_task.create(one, frequency=3, continue_func=should_continue, begin=begin, end=end,
                                    initial_delay=1.5)
    task_two = periodic_task.create(two, frequency=20, continue_func=should_continue, begin=begin, end=end)

    runner.run([task_one, task_two])

    assert one_count == 2
    assert two_count == 40
    assert begin_count == 2
    assert end_count == 2


if __name__ == '__main__':
    execute()
