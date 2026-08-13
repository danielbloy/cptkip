#
# This example runs two synchronous tasks, the first task contains a delay
# which triggers the second task which pulses the LED. Once triggered, the
# LED will remain pulsing because we do not clear the trigger variable.

import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.task.basic_runner as runner
from cptkip.pin.output_pin import OutputPin
from cptkip.task.triggered_task import create

log.set_log_level(log.INFO)

led = OutputPin(config.LED_PIN, invert=config.LED_INVERT)


def should_continue() -> bool:
    return time.monotonic() < finish


trigger = False


def delay() -> bool:
    global trigger, trigger_time

    if not trigger and time.monotonic() >= trigger_time:
        log.info(f"{time.monotonic()}: trigger")
        trigger = True

    return should_continue()


def led_pulse() -> None:
    if led.value:
        log.info(f"{time.monotonic()}: LED off")
        led.off()
    else:
        log.info(f"{time.monotonic()}: LED on")
        led.on()


led_task = create(lambda: trigger, 0.5, begin=led_pulse, continue_func=should_continue)

# Run the loop for 5 seconds
finish = time.monotonic() + 5
trigger_time = time.monotonic() + 1

runner.run([delay, led_task])
led.off()
