def execute():
    from adafruit_led_animation.animation.pulse import Pulse
    from adafruit_led_animation.color import WHITE

    import cptkip.config.configuration as config
    import cptkip.device.led as led
    import cptkip.pin.pwm_pin as pwm_pin
    import validate.utils as utils

    # Add in validation for LED.
    led_pin = pwm_pin.PwmPin(config.LED_PIN, invert=config.LED_INVERT)
    onboard_led = led.Led(led_pin)
    animation = Pulse(onboard_led, speed=0.1, color=WHITE)

    def task():
        animation.animate()

    print("LED will pulse")
    utils.execute(task)

    animation.freeze()
    del animation

    onboard_led.off()
    led_pin.deinit()
    del led_pin


if __name__ == '__main__':
    execute()
