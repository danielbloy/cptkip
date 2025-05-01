def execute():
    import time
    import cptkip.core.logging as log
    import cptkip.core.environment as environment
    import cptkip.hal.digitalpin as digitalpin
    import cptkip.hal.pwmpin as pwmpin

    log.set_log_level(log.INFO)

    LED_PIN = None

    if environment.are_pins_available():
        # noinspection PyPackageRequirements
        import board

        LED_PIN = board.LED

    finish = time.monotonic() + 2

    for pin in [digitalpin.DigitalPin(LED_PIN), pwmpin.PwmPin(LED_PIN)]:

        while time.monotonic() < finish:
            pin.on()
            time.sleep(0.25)
            pin.off()
            time.sleep(0.25)

        pin.deinit()


if __name__ == '__main__':
    execute()
