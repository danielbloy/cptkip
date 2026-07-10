def execute():
    import time

    import cptkip.config.configuration as config
    import cptkip.pin.output_pin as outputpin

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


if __name__ == '__main__':
    execute()
