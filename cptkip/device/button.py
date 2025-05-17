from adafruit_debouncer import Button

import cptkip.core.environment as environment
import cptkip.task.periodic_task as periodic_task
from cptkip.pin.inputpin import InputPin

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable, Awaitable


def create(
        pin: InputPin,
        click: Callable[[], Awaitable[None]] = None,
        multi_click: Callable[[], Awaitable[None]] = None,
        long_click: Callable[[], Awaitable[None]] = None,
        continue_func: Callable[[], bool] = None,
        begin: Callable[[], Awaitable[None]] = None,
        end: Callable[[], Awaitable[None]] = None) -> Callable[[], Awaitable[None]]:
    """
    Returns a task that will respond to button events and call the `click`, `multi_click`
    or `long_click` callbacks based on the events on the button.

    :param pin:           This should be a digital input pin connected to the button.
    :param click:         Callback that is invoked for a single click event.
    :param multi_click:   Callback that is invoked for a multiple click event.
    :param long_click:    Callback that is invoked for a long click event.
    :param continue_func: If specified, this will be periodically called to confirm
                          the func should continue to be called.
    :param begin:         If specified, this will be executed once at the beginning
                          and before any initial delay.
    :param end:           If specified, this will be executed once at the end.
    """
    if pin is None:
        raise ValueError("pin cannot be None")

    if not isinstance(pin, InputPin):
        raise ValueError("pin must be of type InputPin")

    button = Button(pin, short_duration_ms=200, long_duration_ms=2000)

    async def operation() -> None:
        button.update()

        short_count = button.short_count
        if short_count != 0:

            if short_count == 1 and click:
                await click()

            elif short_count > 1 and multi_click:
                await multi_click()

        if button.long_press and long_click is not None:
            await long_click()

    task = periodic_task.create(
        operation, frequency=80, initial_delay=0, continue_func=continue_func, begin=begin, end=end)

    return task
