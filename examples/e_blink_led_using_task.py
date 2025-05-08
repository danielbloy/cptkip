# Blink LEDs but use a task to do it.
import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.core.memory as memory
import cptkip.hal.digitalpin as pin
import cptkip.task.basic_runner as runner
import cptkip.task.periodic_task as periodic_task

memory.report_memory_usage()

log.set_log_level(log.INFO)

led = pin.DigitalPin(config.LED_PIN, invert=config.LED_INVERT)

# Run the loop for 5 seconds
log.info("Using value to control the LED")
finish = time.monotonic() + 5


# Should we continue to run or not?
def should_continue() -> bool:
    return time.monotonic() < finish


# The operation that we want to perform
async def operation() -> None:
    led.value = not led.value
    log.info(f"{time.monotonic()}: {led.value}")


# Executed once at the beginning and before any initial delay.
async def begin() -> None:
    log.info(f"{time.monotonic()}: BEGIN")


# Executed once at the end.
async def end() -> None:
    log.info(f"{time.monotonic()}: END")
    led.off()


# Wrap the operation in a rate limiter function
blink = periodic_task.create(
    operation, frequency=4, initial_delay=1.5,
    continue_func=should_continue,
    begin_func=begin, end_func=end)

runner.run([blink])

memory.report_memory_usage_and_free()
