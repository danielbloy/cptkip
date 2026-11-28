def execute():
    from time import monotonic
    import validate.utils as utils

    import cptkip.config.configuration as config
    import cptkip.pin.pwm_pin as pwm_pin

    utils.require_pins(config.LED_PIN)
    try:
        pin = pwm_pin.PwmPin(config.LED_PIN, invert=config.LED_INVERT)
    except ValueError as e:
        # e.g. the Pico W LED is on the WiFi chip and does not support PWM.
        raise utils.Skip(f"PWM is not supported on LED_PIN: {e}")

    with pin:

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
        utils.execute(task, use_reliable_runner=True)


if __name__ == '__main__':
    execute()
