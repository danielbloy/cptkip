from adafruit_debouncer import Button as DebounceButton

import cptkip.core.environment as environment
from cptkip.pin.input_pin import InputPin

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable


class Button:
    """
    Wraps an InputPin with adafruit_debouncer to provide debounced click,
    multi-click and long-click callbacks. Call update() regularly (e.g. once
    per main loop iteration) to poll the pin and fire the relevant callback.
    """

    def __init__(self, pin: InputPin,
                 click: Callable[[], None] | None = None,
                 multi_click: Callable[[], None] | None = None,
                 long_click: Callable[[], None] | None = None):
        """
        :param pin:         The InputPin the button is connected to.
        :param click:       Called on a single short press, if specified.
        :param multi_click: Called on two or more short presses in quick succession, if specified.
        :param long_click:  Called when the button is held down for a long press (2 seconds), if specified.
        """
        if pin is None:
            raise ValueError("pin cannot be None")

        self.pin = pin
        self.click = click
        self.multi_click = multi_click
        self.long_click = long_click
        # If the pin does not have a value for pullup then we assume it is a pullup
        value_when_pressed = not pin.pullup if pin.pullup is not None else False
        self.button = DebounceButton(pin, long_duration_ms=2000, value_when_pressed=value_when_pressed)

    def update(self):
        """
        Polls the pin and fires click/multi_click/long_click as appropriate.
        Call this regularly, e.g. once per main loop iteration.
        """
        self.button.update()

        short_count = self.button.short_count
        if short_count != 0:

            if short_count == 1 and self.click:
                self.click()

            elif short_count > 1 and self.multi_click:
                self.multi_click()

        if self.button.long_press and self.long_click is not None:
            self.long_click()
