#
# This example demonstrates using Pixels/NeoPixels. An Animation is
# used to provide a Rainbow effect. Uses `cptkip.zero.pixels`.
#
import time

from adafruit_led_animation.animation.rainbow import Rainbow

import cptkip.core.logging as log
from cptkip.zero.pixels import create_pixels, stop_animation

log.set_log_level(log.INFO)

pixels = create_pixels(brightness=0.5)
animation = Rainbow(pixels, speed=0.1, period=2)

# Run the loop for 5 seconds
finish = time.monotonic() + 5

while time.monotonic() < finish:
    animation.animate()

stop_animation(animation)
