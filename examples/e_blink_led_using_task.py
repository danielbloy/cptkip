# Blink LEDs but use a task to do it.
import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.core.memory as memory
import cptkip.hal.digitalpin as pin

memory.report_memory_usage()

log.set_log_level(log.INFO)

led = pin.DigitalPin(config.LED_PIN, invert=config.LED_INVERT)

# Run the loop for 5 seconds
log.info("Using value to control the LED")
finish = time.monotonic() + 5

while time.monotonic() < finish:
    led.value = not led.value

    time.sleep(0.25)
    led.value = False
    time.sleep(0.25)

led.off()

memory.report_memory_usage_and_free()
