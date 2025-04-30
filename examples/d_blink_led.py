import time

import cptkip.core.environment as environment
import cptkip.core.logging as log
import cptkip.core.memory as memory
import cptkip.hal.pwmpin as pin

memory.report_memory_usage()

LED_PIN = None

if environment.are_pins_available():
    # noinspection PyPackageRequirements
    import board

    LED_PIN = board.LED

log.set_log_level(log.INFO)

led = pin.PwmPin(LED_PIN)

# Run the loop for 5 seconds
log.info("Using value for brightness")
finish = time.monotonic() + 5

while time.monotonic() < finish:
    led.value = 0.8
    time.sleep(0.25)
    led.value = 0.2
    time.sleep(0.25)

log.info("Using on()/off() for brightness")
finish = time.monotonic() + 5

while time.monotonic() < finish:
    led.on()
    time.sleep(0.25)
    led.off()
    time.sleep(0.25)

led.off()

memory.report_memory_usage_and_free()
