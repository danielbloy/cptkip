def execute():
    from time import monotonic
    import validate.utils as utils
    import cptkip.config.configuration as config
    import cptkip.pin.output_pin as output_pin

    # Use the LED as an output pin
    pin = output_pin.OutputPin(config.LED_PIN, invert=config.LED_INVERT)

    next_change = 0

    def task():
        change = monotonic() >= next_change
        if change:
            pin.value = not pin.value

    utils.execute(task)

    pin.deinit()
    del pin


if __name__ == '__main__':
    execute()
