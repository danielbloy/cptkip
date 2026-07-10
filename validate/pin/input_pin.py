import utils


def execute():
    import cptkip.config.configuration as config
    import cptkip.pin.input_pin as input_pin

    # Use the BUTTON as an input pin
    pin = input_pin.InputPin(config.BUTTON_PIN, config.BUTTON_PULLUP)

    def task():
        assert pin.value

    utils.execute(task)

    pin.deinit()
    del pin


if __name__ == '__main__':
    execute()
