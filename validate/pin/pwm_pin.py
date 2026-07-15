def execute():
    from time import monotonic
    import validate.utils as utils

    import cptkip.config.configuration as config
    import cptkip.pin.pwm_pin as pwm_pin

    pin = pwm_pin.PwmPin(config.LED_PIN, invert=config.LED_INVERT)

    def task():
        nonlocal next_change
        change = monotonic() >= next_change
        if change:
            print("Change PWM pin")
            next_change += 0.25
            if pin.value > 0.5:
                pin.value = 0.25
            else:
                pin.value = 0.75

    pin.on()
    next_change = monotonic() + 0.25
    print("LED will pulse")
    utils.execute(task)
    pin.off()

    pin.deinit()
    del pin


if __name__ == '__main__':
    execute()
