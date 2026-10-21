#
# This example runs two synchronous tasks, the first task contains a delay
# which triggers the second task which pulses the LED. Once triggered, the
# LED will remain pulsing because we do not clear the trigger variable.

import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.task.basic_runner as runner
from cptkip.pin.output_pin import OutputPin
from cptkip.task.triggered_events_task import create

led = OutputPin(config.LED_PIN, invert=config.LED_INVERT)


def should_continue() -> bool:
    return time.monotonic() < finish


# TODO: Use resettable trigger.
trigger = False


def delay() -> bool:
    global trigger, trigger_time

    if not trigger and time.monotonic() >= trigger_time:
        log.info(f"{time.monotonic()}: trigger")
        trigger = True

    return should_continue()


def begin() -> None:
    global trigger
    log.info(f"{time.monotonic()}: Begin")
    trigger = False


def end() -> None:
    log.info(f"{time.monotonic()}: End")


def fallback(value: int) -> None:
    log.info(f"{time.monotonic()}: Fallback handler, Value: {value}")
    if value:
        led.on()
    else:
        led.off()

    log.info(f"{time.monotonic()}: LED {"on" if led.value else "off"}")


def custom(value: str) -> None:
    log.info(f"{time.monotonic()}: Custom handler, Value: {value}")


events = [
    (0.1,),
    (0.5, 1),
    (1.2, "A", custom),
    (1.0, 0, None),
]

led_task = create(lambda: trigger, events, begin=begin, func=fallback, end=end,
                  continue_func=should_continue)

finish = time.monotonic() + 3
trigger_time = time.monotonic() + 1

runner.run(delay, led_task)
led.off()
