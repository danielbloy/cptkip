#
# This example demonstrates using Pixels/NeoPixels. An Animation is
# used to provide a Rainbow effect.
#
import time

from adafruit_led_animation.animation.rainbow import Rainbow

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.device.pixels as pixel

log.set_log_level(log.INFO)

pixels = pixel.create(config.PIXELS_PIN, 8, brightness=0.5)
animation = Rainbow(pixels, speed=0.1, period=2)

# Run the loop for 5 seconds
finish = time.monotonic() + 5

while time.monotonic() < finish:
    animation.animate()

animation.freeze()
pixels.fill(pixel.OFF)
pixels.write()
