def execute_button():
    import time

    import cptkip.config.configuration as config
    import cptkip.device.button as button
    import cptkip.pin.inputpin as inputpin
    import cptkip.task.basic_runner as runner

    single_click_count: int = 0
    multi_click_count: int = 0
    long_click_count: int = 0
    begin_count: int = 0
    end_count: int = 0

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

    # Run the loop for 2 seconds
    finish = time.monotonic() + 2

    def should_continue() -> bool:
        return time.monotonic() < finish

    input_pin = inputpin.InputPin(config.BUTTON_PIN)

    task = button.create(
        input_pin,
        click=single_click_handler,
        multi_click=multi_click_handler,
        long_click=long_press_handler,
        continue_func=should_continue,
        begin=begin,
        end=end)

    runner.run([task])

    assert single_click_count == 0
    assert multi_click_count == 0
    assert long_click_count == 0
    assert begin_count == 1
    assert end_count == 1

    input_pin.deinit()
    del input_pin


def execute_led():
    import time

    from adafruit_led_animation.animation.pulse import Pulse
    from adafruit_led_animation.color import WHITE

    import cptkip.config.configuration as config
    import cptkip.device.led as led
    import cptkip.pin.pwmpin as pwmpin

    # Add in validation for LED.
    led_pin = pwmpin.PwmPin(config.LED_PIN, invert=config.LED_INVERT)
    onboard_led = led.Led(led_pin)
    animation = Pulse(onboard_led, speed=0.1, color=WHITE)

    async def update() -> None:
        animation.animate()

    finish = time.monotonic() + 2
    while time.monotonic() < finish:
        animation.animate()

    animation.freeze()
    del animation

    onboard_led.off()
    led_pin.deinit()
    del led_pin


def execute_pixels():
    import time

    from adafruit_led_animation.animation.rainbow import Rainbow

    import cptkip.config.configuration as config
    import cptkip.device.pixels as pixel

    # Use the PIXELS pin
    pixels = pixel.create(config.PIXELS_PIN, 8, brightness=0.5)
    animation = Rainbow(pixels, speed=0.1, period=2)
    animation.animate()

    finish = time.monotonic() + 2
    while time.monotonic() < finish:
        animation.animate()

    animation.freeze()
    del animation

    pixels.fill(pixel.OFF)
    pixels.write()

    pixels.deinit()
    del pixels


def execute_buzzer():
    import time

    import cptkip.config.configuration as config
    import cptkip.pin.buzzerpin as buzzerpin
    from cptkip.device.buzzer import Buzzer

    pin = buzzerpin.BuzzerPin(config.BUZZER_PIN)
    buzzer = Buzzer(pin)

    buzzer.beep()
    finish = time.monotonic() + 0.5
    while time.monotonic() < finish:
        buzzer.update()

    pin.volume = 0.5

    buzzer.beeps(4)
    finish = time.monotonic() + 2.5
    while time.monotonic() < finish:
        buzzer.update()

    # Get quieter
    pin.volume = 1.0
    buzzer.play(500, 3)
    finish = time.monotonic() + 2

    while time.monotonic() < finish:
        pin.volume -= 0.1
        time.sleep(0.25)

    buzzer.off()
    pin.deinit()

    del buzzer
    del pin


def execute():
    import cptkip.core.logging as log

    log.set_log_level(log.INFO)

    execute_button()
    execute_led()
    execute_pixels()
    execute_buzzer()


if __name__ == '__main__':
    execute()
