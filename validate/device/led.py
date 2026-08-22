def execute():
    from adafruit_led_animation.animation.pulse import Pulse
    from adafruit_led_animation.color import WHITE

    import cptkip.config.configuration as config
    import cptkip.device.led as led
    import cptkip.pin.pwm_pin as pwm_pin
    import validate.utils as utils

    with led.Led(pwm_pin.PwmPin(config.LED_PIN, invert=config.LED_INVERT)) as onboard_led:
        onboard_led.off()
        animation = Pulse(onboard_led, speed=1 / 30, color=WHITE)

        def task():
            animation.animate()

        print("LED will pulse")
        utils.execute(task)


if __name__ == '__main__':
    execute()
