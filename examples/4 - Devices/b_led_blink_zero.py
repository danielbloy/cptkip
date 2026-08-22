#
# This example blinks the board LED using a simple loop.
# Uses `cptkip.zero.led` and `cptkip.zero.run`.
#
import time

import cptkip.core.logging as log
from cptkip.zero.led import create_led
from cptkip.zero.run import run_for

log.set_log_level(log.INFO)

with create_led() as led:
    # Loop, turning the pin on and off.
    def blink():
        led.on()
        time.sleep(0.25)
        led.off()
        time.sleep(0.25)


    run_for(5, blink)
