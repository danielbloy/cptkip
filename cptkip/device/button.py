from adafruit_debouncer import Button

import cptkip.core.environment as environment
import cptkip.task.periodic_task as periodic_task

# The timeframe to consider button presses to be a sequence for multi-clicks.
BUTTON_SHORT_DURATION_MS = 200
# The timeframe to consider a button being pressed should register as a long press.
BUTTON_LONG_DURATION_MS = 2000
# How often we poll the button
BUTTON_FREQUENCY = 120

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    from collections.abc import Callable, Awaitable


# TODO: Should the handlers accept the button object as a parameter? Can we make it optional live PGZ
# TODO: Should we add type information for the handlers

def new(pin, click=None, multi_click=None, long_click=None,
        continue_func=None, begin=None, end=None) -> Callable[[], Awaitable[None]]:
    """
    Returns a task that can be added to a runner.
    TODO: Write comments

    :param pin:
    :param click:
    :param multi_click:
    :param long_click:
    :param continue_func: If specified, this will be periodically called to confirm
        the func should continue to be called.
    :param begin: If specified, this will be executed once at the beginning
        and before any initial delay.
    :param end: If specified, this will be executed once at the end.
    """

    button = Button(pin, short_duration_ms=BUTTON_SHORT_DURATION_MS, long_duration_ms=BUTTON_LONG_DURATION_MS)

    async def operation() -> None:
        button.update()

        short_count = button.short_count
        if short_count != 0:

            if short_count == 1 and click:
                await click()

            elif short_count > 1 and multi_click:
                # TODO: Should multi-click be passed the number of clicks?
                await multi_click()

        if button.long_press and long_click is not None:
            await long_click()

    task = periodic_task.create(
        operation, frequency=BUTTON_FREQUENCY, initial_delay=0,
        continue_func=continue_func, begin=begin, end=end)

    return task
