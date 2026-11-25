import cptkip.config.configuration as config
import cptkip.core.environment as environment
from cptkip.device.button import Button
from cptkip.pin.input_pin import InputPin

if environment.is_running_on_desktop():
    from typing import Callable


def create_button_pin(pin=None) -> InputPin:
    """
    Simple utility function to make it easy to create a Button InputPin based on configuration.
    If no pin is specified, it defaults to the config value BUTTON_PIN.
    """
    return InputPin(pin or config.BUTTON_PIN, config.BUTTON_PULLUP)


def create_button(pin=None,
                  click: Callable[[], None] | None = None,
                  multi_click: Callable[[], None] | None = None,
                  long_click: Callable[[], None] | None = None) -> Button:
    """
    Simple utility function to make it easy to create a button.
    If no pin is specified, it defaults to the config value BUTTON_PIN.

    :param pin:         The pin to use for button, default for config.BUTTON_PIN.
    :param click:       Called on a single short press, if specified.
    :param multi_click: Called on two or more short presses in quick succession, if specified.
    :param long_click:  Called when the button is held down for a long press (2 seconds), if specified.
    """
    input_pin = create_button_pin(pin)
    return Button(input_pin, click=click, multi_click=multi_click, long_click=long_click)
