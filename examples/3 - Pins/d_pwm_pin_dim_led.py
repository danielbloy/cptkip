#
# This examples uses a PwmPin to dim the pin connected to the
# boards LED. There are two loops, the first one uses the
# `value` property to set the relative brightness. The second
# loop uses the `on()` and `off()` methods to either turn off
# the pin or set it to maximum.
#
import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.core.memory as memory
from cptkip.pin.pwm_pin import PwmPin

memory.report_memory_usage()

log.set_log_level(log.INFO)

led = PwmPin(config.LED_PIN, invert=config.LED_INVERT)

# Run the loop for 5 seconds
log.info("Using value for brightness")
finish = time.monotonic() + 5

while time.monotonic() < finish:
    led.value = 0.8
    time.sleep(0.25)
    led.value = 0.2
    time.sleep(0.25)

log.info("Using on()/off() for brightness")
# noinspection DuplicatedCode
finish = time.monotonic() + 5

while time.monotonic() < finish:
    led.on()
    time.sleep(0.25)
    led.off()
    time.sleep(0.25)

led.off()

memory.report_memory_usage_and_free()
