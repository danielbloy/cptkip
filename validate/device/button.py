def execute():
    import validate.utils as utils

    import cptkip.config.configuration as config
    from cptkip.device.button import Button
    import cptkip.pin.input_pin as inputpin

    def single_click_handler() -> None:
        print("Single click event")

    def multi_click_handler() -> None:
        print("Multi-click event")

    def long_press_handler() -> None:
        print("Long-press event")

    input_pin = inputpin.InputPin(config.BUTTON_PIN, config.BUTTON_PULLUP)

    button = Button(
        input_pin,
        click=single_click_handler,
        multi_click=multi_click_handler,
        long_click=long_press_handler)

    def task():
        button.update()

    print("Press the button to test")
    utils.execute(task)

    input_pin.deinit()
    del input_pin

    del button


if __name__ == '__main__':
    execute()
