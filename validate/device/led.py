def execute():
    from adafruit_led_animation.animation.pulse import Pulse
    from adafruit_led_animation.color import WHITE

    import cptkip.config.configuration as config
    import cptkip.device.led as led
    import cptkip.pin.pwm_pin as pwm_pin
    import validate.utils as utils

    utils.require_pins(config.LED_PIN)
    try:
        pin = pwm_pin.PwmPin(config.LED_PIN, invert=config.LED_INVERT)
    except ValueError as e:
        # e.g. the Pico W LED is on the WiFi chip and does not support PWM.
        raise utils.Skip(f"PWM is not supported on LED_PIN: {e}")

    with led.Led(pin) as onboard_led:
        onboard_led.off()
        animation = Pulse(onboard_led, speed=1 / 30, color=WHITE)

        def task():
            animation.animate()

        print("LED will pulse")
        utils.execute(task)


if __name__ == '__main__':
    execute()
