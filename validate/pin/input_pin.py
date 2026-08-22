def execute():
    import validate.utils as utils
    import cptkip.config.configuration as config
    import cptkip.pin.input_pin as input_pin

    # Use the BUTTON as an input pin
    with input_pin.InputPin(config.BUTTON_PIN, config.BUTTON_PULLUP) as pin:
        def task():
            nonlocal value
            if value != pin.value:
                value = pin.value
                print(f"Input pin changed value to {value}")

        value = pin.value
        print("Press the button to validate")
        utils.execute(task)


if __name__ == '__main__':
    execute()
