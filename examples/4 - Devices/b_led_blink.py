#
# This example blinks the board LED using a simple loop.
#
import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.core.memory as memory
from cptkip.device.led import Led
from cptkip.pin.pwm_pin import PwmPin

memory.report_memory_usage()

log.set_log_level(log.INFO)

pin = PwmPin(config.LED_PIN, invert=config.LED_INVERT)
led = Led(pin)

# Loop, turning the pin on and off.
finish = time.monotonic() + 5
while time.monotonic() < finish:
    led.on()
    time.sleep(0.25)
    led.off()
    time.sleep(0.25)

led.off()

memory.report_memory_usage_and_free()
