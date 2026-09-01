#
# This example demonstrates using Pixels/NeoPixels. An Animation is
# used to provide a Rainbow effect. Uses `cptkip.zero.pixels` and
# `cptkip.zero.run`.
#

from adafruit_led_animation.animation.rainbow import Rainbow

from cptkip.zero.pixels import create_pixels, stop_animation
from cptkip.zero.run import update_for

with create_pixels(brightness=0.5) as pixels:
    animation = Rainbow(pixels, speed=0.1, period=2)

    update_for(3, animation)
    stop_animation(animation)
