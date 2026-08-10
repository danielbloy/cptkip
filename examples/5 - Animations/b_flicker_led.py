#
# This example uses the Flicker animation to flicker the board LED.
#

from adafruit_led_animation.color import JADE

import cptkip.animation.flicker as animations
import cptkip.core.logging as log
from cptkip.zero.led import create_led, stop_animation
from cptkip.zero.run import update_for

log.set_log_level(log.INFO)

led = create_led()
animation = animations.Flicker(led, speed=0.5, color=JADE, base=100, flame=155)

update_for(5, animation)

stop_animation(animation)
