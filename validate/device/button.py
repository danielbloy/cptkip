def execute():
    import cptkip.config.configuration as config
    import cptkip.pin.input_pin as input_pin
    import validate.utils as utils
    from cptkip.device.button import Button

    def single_click_handler() -> None:
        print("Single click event")

    def multi_click_handler() -> None:
        print("Multi-click event")

    def long_press_handler() -> None:
        print("Long-press event")

    pin = input_pin.InputPin(config.BUTTON_PIN, config.BUTTON_PULLUP)

    button = Button(
        pin,
        click=single_click_handler,
        multi_click=multi_click_handler,
        long_click=long_press_handler)

    def task():
        button.update()

    print("Press the button to test")
    utils.execute(task)

    pin.deinit()
    del pin

    del button


if __name__ == '__main__':
    execute()
