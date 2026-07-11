#
# This example uses the configured LED to demonstrate using an OutputPin.
# The first lop uses the `value` property to change the state of the LED
# and the second loop uses the `on()` and `off()` methods to do the same.
#
import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
from cptkip.pin.output_pin import OutputPin

log.set_log_level(log.INFO)

led = OutputPin(config.LED_PIN, invert=config.LED_INVERT)

# Run the loop for 5 seconds
log.info("Using value to control the LED")
finish = time.monotonic() + 5

while time.monotonic() < finish:
    led.value = True
    time.sleep(0.25)
    led.value = False
    time.sleep(0.25)

log.info("Using on()/off() to control the LED")
# noinspection DuplicatedCode
finish = time.monotonic() + 5

while time.monotonic() < finish:
    led.on()
    time.sleep(0.25)
    led.off()
    time.sleep(0.25)

led.off()
