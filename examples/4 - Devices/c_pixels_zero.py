#
# This example demonstrates using Pixels/NeoPixels. An Animation is
# used to provide a Rainbow effect. Uses `cptkip.zero.pixels` and
# `cptkip.zero.run`.
#

from adafruit_led_animation.animation.rainbow import Rainbow

import cptkip.core.logging as log
from cptkip.zero.pixels import create_pixels, stop_animation
from cptkip.zero.run import update_for

log.set_log_level(log.INFO)

pixels = create_pixels(brightness=0.5)
animation = Rainbow(pixels, speed=0.1, period=2)

update_for(5, animation)
stop_animation(animation)
