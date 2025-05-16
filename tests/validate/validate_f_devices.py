def execute():
    import time

    from adafruit_led_animation.animation.pulse import Pulse
    from adafruit_led_animation.color import WHITE

    import cptkip.config.configuration as config
    import cptkip.core.logging as log
    import cptkip.device.button as button
    import cptkip.hal.digitalpin as digitalpin
    import cptkip.hal.pwmpin as pwmpin
    import cptkip.task.basic_runner as runner
    import cptkip.task.periodic_task as periodic_task

    import cptkip.device.led as led

    log.set_log_level(log.INFO)

    single_click_count: int = 0
    multi_click_count: int = 0
    long_click_count: int = 0
    begin_count: int = 0
    end_count: int = 0

    # Run the loop for 2 seconds
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

    input_pin = digitalpin.InputPin(config.BUTTON_PIN)
    task = button.create(
        input_pin,
        click=single_click_handler,
        multi_click=multi_click_handler,
        long_click=long_press_handler,
        continue_func=should_continue,
        begin=begin,
        end=end)

    runner.run([task])

    input_pin.deinit()
    del input_pin

    assert single_click_count == 0
    assert multi_click_count == 0
    assert long_click_count == 0
    assert begin_count == 1
    assert end_count == 1

    # Add in validation for LED.
    led_pin = pwmpin.PwmPin(config.LED_PIN, invert=config.LED_INVERT)
    onboard_led = led.Led(led_pin)
    animation = Pulse(onboard_led, speed=0.1, color=WHITE)

    # Run the loop for 2 seconds
    finish = time.monotonic() + 2

    async def update() -> None:
        animation.animate()

    task = periodic_task.create(update, frequency=30, continue_func=should_continue)

    runner.run([task])

    led_pin.deinit()
    del led_pin


if __name__ == '__main__':
    execute()
