def execute():
    import time

    import cptkip.core.logging as log
    import cptkip.task.basic_runner as runner
    import cptkip.device.button as button
    import cptkip.hal.digitalpin as pin
    import cptkip.config.configuration as config

    log.set_log_level(log.INFO)

    single_click_count: int = 0
    multi_click_count: int = 0
    long_click_count: int = 0
    begin_count: int = 0
    end_count: int = 0

    # Run the loop for 5 seconds
    finish = time.monotonic() + 2

    def should_continue() -> bool:
        return time.monotonic() < finish

    async def single_click_handler() -> None:
        nonlocal single_click_count
        single_click_count += 1

    async def multi_click_handler() -> None:
        nonlocal multi_click_count
        multi_click_count += 1

    async def long_press_handler() -> None:
        nonlocal long_click_count
        long_click_count += 1

    # Executed once at the beginning and before any initial delay.
    async def begin() -> None:
        nonlocal begin_count
        begin_count += 1

    # Executed once at the end.
    async def end() -> None:
        nonlocal end_count
        end_count += 1

    button = button.create(
        pin.InputPin(config.BUTTON_PIN),
        click=single_click_handler,
        multi_click=multi_click_handler,
        long_click=long_press_handler,
        continue_func=should_continue,
        begin=begin,
        end=end)

    runner.run([button])

    assert single_click_count == 0
    assert multi_click_count == 0
    assert long_click_count == 0
    assert begin_count == 1
    assert end_count == 1


if __name__ == '__main__':
    execute()
