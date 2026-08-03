import cptkip.config.configuration as config
import cptkip.core.environment as environment
from cptkip.device.button import Button
from cptkip.pin.input_pin import InputPin

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable


def create_button(click: Callable[[], None] | None = None,
                  multi_click: Callable[[], None] | None = None,
                  long_click: Callable[[], None] | None = None) -> Button:
    """
    Simple utility function to make it easy to create a button.
    :param click:       Called on a single short press, if specified.
    :param multi_click: Called on two or more short presses in quick succession, if specified.
    :param long_click:  Called when the button is held down for a long press (2 seconds), if specified.
    """
    input_pin = InputPin(config.BUTTON_PIN, config.BUTTON_PULLUP)

    return Button(input_pin, click=click, multi_click=multi_click, long_click=long_click)
