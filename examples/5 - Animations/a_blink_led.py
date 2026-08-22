#
# This example uses a Blink animation to blink the board LED.
#

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.color import JADE

import cptkip.core.logging as log
from cptkip.zero.led import create_led, stop_animation
from cptkip.zero.run import update_for

log.set_log_level(log.INFO)

with create_led() as led:
    animation = Blink(led, speed=0.5, color=JADE)

    update_for(5, animation)

    stop_animation(animation)
