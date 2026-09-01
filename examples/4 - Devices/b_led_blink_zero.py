#
# This example blinks the board LED using a simple loop.
# Uses `cptkip.zero.led` and `cptkip.zero.run`.
#
import time

from cptkip.zero.led import create_led
from cptkip.zero.run import run_for

with create_led() as led:
    def blink():
        led.toggle()
        time.sleep(0.25)


    run_for(3, blink)
