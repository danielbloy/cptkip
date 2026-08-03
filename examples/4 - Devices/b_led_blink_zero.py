#
# This example blinks the board LED using a simple loop.
#
import time

import cptkip.core.logging as log
from cptkip.zero.led import create_led

log.set_log_level(log.INFO)

led = create_led()

# Loop, turning the pin on and off.
finish = time.monotonic() + 5
while time.monotonic() < finish:
    led.on()
    time.sleep(0.25)
    led.off()
    time.sleep(0.25)

led.off()
