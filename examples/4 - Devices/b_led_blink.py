#
# This example blinks the board LED using a simple loop.
#
import time

import cptkip.config.configuration as config
from cptkip.device.led import Led
from cptkip.pin.pwm_pin import PwmPin

with Led(PwmPin(config.LED_PIN, invert=config.LED_INVERT)) as led:
    finish = time.monotonic() + 3
    while time.monotonic() < finish:
        led.toggle()
        time.sleep(0.25)
