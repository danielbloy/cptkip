def execute():
    from time import monotonic
    import validate.utils as utils
    import cptkip.config.configuration as config
    import cptkip.pin.output_pin as output_pin

    # Use the LED as an output pin
    pin = output_pin.OutputPin(config.LED_PIN, invert=config.LED_INVERT)

    def task():
        nonlocal next_change
        change = monotonic() >= next_change
        if change:
            print("Change output pin")
            next_change += 0.25
            pin.value = not pin.value

    pin.on()
    next_change = monotonic() + 0.25
    print("LED will flash")
    utils.execute(task)
    pin.off()

    pin.deinit()
    del pin


if __name__ == '__main__':
    execute()
