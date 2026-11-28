def execute():
    import cptkip.config.configuration as config
    import validate.utils as utils
    from cptkip.core.environment import are_pins_available
    from cptkip.zero.button import create_button
    from cptkip.zero.buzzer import create_buzzer
    from cptkip.zero.led import create_led
    from cptkip.zero.pixels import create_pixels, stop_pixels

    # Builds each device purely from config.py, which checks the board configuration
    # end to end. On a device, devices that are not configured are left out.
    on_device = are_pins_available()
    checked = []

    if not on_device or config.LED_PIN is not None:
        try:
            with create_led() as led:
                led.on()
                checked.append("led")
        except ValueError as e:  # e.g. the Pico W LED does not support PWM
            print("LED left out:", e)

    if not on_device or config.BUTTON_PIN is not None:
        with create_button() as button:
            button.update()
            checked.append("button")

    if not on_device or config.BUZZER_PIN is not None:
        with create_buzzer() as buzzer:
            buzzer.volume = 0.1
            buzzer.beep()
            checked.append("buzzer")

    if not on_device or config.PIXELS_PIN is not None:
        with create_pixels(brightness=0.2) as pixels:
            pixels.fill((0, 32, 0))
            pixels.write()
            stop_pixels(pixels)
            checked.append("pixels")

    print("Created from config:", checked)
    utils.skip_unless(checked, "no devices are configured")


if __name__ == '__main__':
    execute()
