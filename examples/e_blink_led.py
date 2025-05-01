import time

import cptkip.core.environment as environment
import cptkip.core.logging as log
import cptkip.core.memory as memory
import cptkip.hal.digitalpin as pin

memory.report_memory_usage()

LED_PIN = None

if environment.are_pins_available():
    # noinspection PyPackageRequirements
    import board

    LED_PIN = board.LED

log.set_log_level(log.INFO)

led = pin.DigitalPin(LED_PIN)

# Run the loop for 5 seconds
log.info("Using value to control the LED")
finish = time.monotonic() + 5

while time.monotonic() < finish:
    led.value = True
    time.sleep(0.25)
    led.value = True
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

memory.report_memory_usage_and_free()
