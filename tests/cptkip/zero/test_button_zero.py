import cptkip.config.configuration as config
from cptkip.zero.button import create_button_pin, create_button


class TestButtonZero:
    """
    The tests in here are trivial. They are not intended to test the functionality
    of the underlying pins or devices, just that the `cptkip.zero.button` module
    constructs them correctly.
    """

    def test_create_button_pin(self):
        """
        Validates that a button pin is created "properly".
        """
        pin = create_button_pin()
        assert pin
        assert pin.pin == config.BUTTON_PIN == "button_pin"
        assert pin.pullup == config.BUTTON_PULLUP == "button_pullup"

    def test_create_button(self):
        """
        Validates that a button is created "properly".
        """
        btn = create_button()
        assert btn
        assert btn.pin.pin == config.BUTTON_PIN == "button_pin"
        assert btn.pin.pullup == config.BUTTON_PULLUP == "button_pullup"

    def test_create_button_click(self):
        """
        Validates that a button click is assigned "properly".
        """

        def single_click_handler() -> None:
            pass

        btn = create_button(click=single_click_handler)
        assert btn
        assert btn.click is single_click_handler

    def test_create_button_double_click(self):
        """
        Validates that a button multi-click is assigned "properly".
        """

        def multi_click_handler() -> None:
            pass

        btn = create_button(multi_click=multi_click_handler)
        assert btn
        assert btn.multi_click is multi_click_handler

    def test_create_button_long_click(self):
        """
        Validates that a button long-press is assigned "properly".
        """

        def long_press_handler() -> None:
            pass

        btn = create_button(long_click=long_press_handler)
        assert btn
        assert btn.long_click is long_press_handler

    def test_create_button_mix_clicks(self):
        """
        Validates that a buttons events are assigned "properly".
        """

        def single_click_handler() -> None:
            pass

        def multi_click_handler() -> None:
            pass

        def long_press_handler() -> None:
            pass

        # With named parameters
        btn = create_button(
            click=single_click_handler,
            multi_click=multi_click_handler,
            long_click=long_press_handler)

        assert btn
        assert btn.click is single_click_handler
        assert btn.multi_click is multi_click_handler
        assert btn.long_click is long_press_handler

        # Without named parameters
        btn = create_button(single_click_handler, multi_click_handler, long_press_handler)
        assert btn
        assert btn.click is single_click_handler
        assert btn.multi_click is multi_click_handler
        assert btn.long_click is long_press_handler
