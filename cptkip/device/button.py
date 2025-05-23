from adafruit_debouncer import Button as DebounceButton

import cptkip.core.environment as environment
from cptkip.pin.input_pin import InputPin

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable


class Button:
    def __init__(self, pin: InputPin,
                 click: Callable[[], None] = None,
                 multi_click: Callable[[], None] = None,
                 long_click: Callable[[], None] = None):
        if pin is None:
            raise ValueError("pin cannot be None")

        self.pin = pin
        self.click = click
        self.multi_click = multi_click
        self.long_click = long_click
        self.button = DebounceButton(pin, long_duration_ms=2000)

    def update(self):
        self.button.update()

        short_count = self.button.short_count
        if short_count != 0:

            if short_count == 1 and self.click:
                self.click()

            elif short_count > 1 and self.multi_click:
                self.multi_click()

        if self.button.long_press and self.long_click is not None:
            self.long_click()
