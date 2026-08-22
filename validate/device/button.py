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

    with Button(
            input_pin.InputPin(config.BUTTON_PIN, config.BUTTON_PULLUP),
            click=single_click_handler,
            multi_click=multi_click_handler,
            long_click=long_press_handler) as button:
        def task():
            button.update()

        print("Press the button to validate")
        utils.execute(task)


if __name__ == '__main__':
    execute()
