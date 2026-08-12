#
# This example runs two asynchronous tasks, the first task contains a delay
# which triggers the second task which pulses the LED. Once triggered, the
# LED will remain pulsing because we do not clear the trigger variable.

import asyncio
import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.task.basic_runner_async as runner
import cptkip.task.triggered_task_async as triggered_task
from cptkip.pin.output_pin import OutputPin

log.set_log_level(log.INFO)

led = OutputPin(config.LED_PIN, invert=config.LED_INVERT)


def should_continue() -> bool:
    return time.monotonic() < finish


trigger = False


async def delay() -> None:
    global trigger
    log.info(f"{time.monotonic()}: start delay")
    await asyncio.sleep(1.0)
    log.info(f"{time.monotonic()}: trigger")
    trigger = True


async def led_on() -> None:
    log.info(f"{time.monotonic()}: LED on")
    led.on()


async def led_off() -> None:
    log.info(f"{time.monotonic()}: LED off")
    led.off()


led_task = triggered_task.create(lambda: trigger, 1, begin=led_on, end=led_off,
                                 continue_func=should_continue)

# Run the loop for 5 seconds
finish = time.monotonic() + 5

runner.run([delay, led_task])
led.off()
