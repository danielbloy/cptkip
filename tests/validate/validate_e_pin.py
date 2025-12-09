def execute():
    import time

    import cptkip.config.configuration as config
    import cptkip.pin.input_pin as inputpin
    import cptkip.pin.output_pin as outputpin
    import cptkip.pin.pwm_pin as pwmpin

    # Use the LED as an output pin
    pin = outputpin.OutputPin(config.LED_PIN, invert=config.LED_INVERT)
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
    pin = inputpin.InputPin(config.BUTTON_PIN, config.BUTTON_INVERT)
    finish = time.monotonic() + 2
    while time.monotonic() < finish:
        assert pin.value
        time.sleep(0.25)

    pin.deinit()
    del pin


if __name__ == '__main__':
    execute()
