#
# This example runs two asynchronous tasks, the first task contains a delay
# # which triggers the second task which triggers some timed events that are
# # used to control the state of the LED. In this example, the trigger task
# # ends as soon as the self-resetting trigger is fired.

import asyncio
import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.task.basic_runner_async as runner
from cptkip.pin.output_pin import OutputPin
from cptkip.task.triggered_events_task_async import create, Trigger

led = OutputPin(config.LED_PIN, invert=config.LED_INVERT)


def should_continue() -> bool:
    return time.monotonic() < finish


trigger = Trigger(False)


async def delay() -> None:
    log.info(f"{time.monotonic()}: start delay")
    await asyncio.sleep(1.0)
    log.info(f"{time.monotonic()}: trigger")
    trigger.triggered = True


async def begin() -> None:
    log.info(f"{time.monotonic()}: Begin - LED ON")
    led.on()


async def end() -> None:
    log.info(f"{time.monotonic()}: End - LED OFF")
    led.off()


async def fallback(value: int) -> None:
    log.info(f"{time.monotonic()}: Fallback handler, Value: {value}")
    if value:
        led.on()
    else:
        led.off()

    log.info(f"{time.monotonic()}: LED {"on" if led.value else "off"}")


async def custom(value: str) -> None:
    log.info(f"{time.monotonic()}: Custom handler, Value: {value}")


# Note: the events are deliberately out of order with respect to time.
events = [
    (1.5, "Last event"),
    (0.1,),
    (0.5, 1),
    (1.2, "A", custom),
    (1.0, 0),
]

task = create(trigger, events, begin=begin, callback=fallback, end=end,
              continue_func=should_continue)

finish = time.monotonic() + 3

log.set_log_level(log.INFO)
runner.run(delay, task)
led.off()
