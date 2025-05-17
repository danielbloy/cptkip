def execute():
    import time

    import cptkip.pin.digitalpin as digitalpin
    import cptkip.pin.pwmpin as pwmpin

    import cptkip.config.configuration as config

    # Use the LED as an output pin
    pin = digitalpin.OutputPin(config.LED_PIN, invert=config.LED_INVERT)
    finish = time.monotonic() + 2
    while time.monotonic() < finish:
        pin.on()
        time.sleep(0.25)
        pin.off()
        time.sleep(0.25)

    pin.deinit()
    del pin

    pin = pwmpin.PwmPin(config.LED_PIN, invert=config.LED_INVERT)
    finish = time.monotonic() + 2
    while time.monotonic() < finish:
        pin.on()
        time.sleep(0.25)
        pin.off()
        time.sleep(0.25)

    pin.deinit()
    del pin

    # Use the BUTTON as an input pin
    pin = digitalpin.InputPin(config.BUTTON_PIN)
    finish = time.monotonic() + 2
    while time.monotonic() < finish:
        assert pin.value
        time.sleep(0.25)

    pin.deinit()
    del pin


if __name__ == '__main__':
    execute()
