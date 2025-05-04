# Blink LEDs but use a task to do it.
import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.core.memory as memory
import cptkip.hal.digitalpin as pin
import cptkip.task.runner as runner
from task.periodic_task import new_periodic_task

memory.report_memory_usage()

log.set_log_level(log.INFO)

led = pin.DigitalPin(config.LED_PIN, invert=config.LED_INVERT)

# Run the loop for 5 seconds
log.info("Using value to control the LED")
finish = time.monotonic() + 5


# Should we continue to run or not?
def run() -> bool:
    return time.monotonic() < finish


# The operation that we want to perform
async def operation() -> None:
    led.value = not led.value
    log.info(f"{time.monotonic()}: {led.value}")


# Wrap the operation in a rate limiter function
blink = new_periodic_task(operation, frequency=4, run_func=run, initial_delay=0)

runner.run([blink])

# TODO: need a way to execute terminate code or is this fine here?
led.off()

memory.report_memory_usage_and_free()
