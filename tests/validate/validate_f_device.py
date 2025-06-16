def execute_button():
    import time

    import cptkip.config.configuration as config
    from cptkip.device.button import Button
    import cptkip.pin.input_pin as inputpin

    single_click_count: int = 0
    multi_click_count: int = 0
    long_click_count: int = 0

    def single_click_handler() -> None:
        nonlocal single_click_count
        single_click_count += 1

    def multi_click_handler() -> None:
        nonlocal multi_click_count
        multi_click_count += 1

    def long_press_handler() -> None:
        nonlocal long_click_count
        long_click_count += 1

    input_pin = inputpin.InputPin(config.BUTTON_PIN)

    button = Button(
        input_pin,
        click=single_click_handler,
        multi_click=multi_click_handler,
        long_click=long_press_handler)

    # Run the loop for 2 seconds
    finish = time.monotonic() + 2
    while time.monotonic() < finish:
        button.update()

    assert single_click_count == 0
    assert multi_click_count == 0
    assert long_click_count == 0

    input_pin.deinit()
    del input_pin

    del button


def execute_led():
    import time

    from adafruit_led_animation.animation.pulse import Pulse
    from adafruit_led_animation.color import WHITE

    import cptkip.config.configuration as config
    import cptkip.device.led as led
    import cptkip.pin.pwm_pin as pwmpin

    # Add in validation for LED.
    led_pin = pwmpin.PwmPin(config.LED_PIN, invert=config.LED_INVERT)
    onboard_led = led.Led(led_pin)
    animation = Pulse(onboard_led, speed=0.1, color=WHITE)

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
    import cptkip.pin.buzzer_pin as buzzerpin
    from cptkip.device.buzzer import Buzzer

    pin = buzzerpin.BuzzerPin(config.BUZZER_PIN)
    buzzer = Buzzer(pin)

    buzzer.beep()
    buzzer.beep()
    finish = time.monotonic() + 1.0
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


def execute_melody():
    import time

    import cptkip.config.configuration as config
    import cptkip.pin.buzzer_pin as buzzerpin
    import cptkip.device.melody as melody

    pin = buzzerpin.BuzzerPin(config.BUZZER_PIN)
    pin.volume = 0.1

    scale = '''C4:1 D:1 E:1 F:1 G:1 A:1 B:1 C5:1
               B4:1 A:1 G:1 F:1 E:1 D:1 C:1'''

    tune = [
        "E:2", "E:2", "E:4", "E:2", "E:2", "E:4",
        "E:2", "G:2", "C:2", "D:2", "E:8", "R:8"]

    melody_sequence = melody.MelodySequence(
        melody.Melody(pin, melody.decode_melody(scale.split()), 120),
        melody.Melody(pin, melody.decode_melody(tune)))

    finish = time.monotonic() + 3
    while time.monotonic() < finish:
        melody_sequence.update()

    pin.off()
    del pin


def execute_pwm_audio():
    import time

    import cptkip.config.configuration as config
    import cptkip.device.pwm_audio as pwm_audio

    audio = pwm_audio.Audio(config.BUZZER_PIN if config.BUZZER_PIN else "none")
    queue = pwm_audio.Queue(audio)
    queue.queue("tests/validate/lion.mp3")
    queue.queue("tests/validate/lion.mp3")

    finish = time.monotonic() + 5

    while time.monotonic() < finish:
        queue.update()

    audio.deinit()


def execute():
    import cptkip.core.logging as log

    log.set_log_level(log.INFO)

    execute_button()
    execute_led()
    execute_pixels()
    execute_buzzer()
    execute_melody()
    execute_pwm_audio()


if __name__ == '__main__':
    execute()
