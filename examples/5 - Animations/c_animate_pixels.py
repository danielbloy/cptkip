#
# This example uses a range of Adafruit animations on Pixels/NeoPixels.
#

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.colorcycle import ColorCycle
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.animation.rainbow import Rainbow
from adafruit_led_animation.animation.rainbowchase import RainbowChase
from adafruit_led_animation.animation.rainbowcomet import RainbowComet
from adafruit_led_animation.animation.rainbowsparkle import RainbowSparkle
from adafruit_led_animation.animation.sparkle import Sparkle
from adafruit_led_animation.color import *
from adafruit_led_animation.sequence import AnimationSequence

import cptkip.core.logging as log
from cptkip.animation.flicker import Flicker
from cptkip.zero.button import create_button
from cptkip.zero.pixels import create_pixels, stop_animation
from cptkip.zero.run import update_for

log.set_log_level(log.INFO)

pixels = create_pixels(brightness=0.5)

animations = [
    Flicker(pixels, speed=0.1, color=AMBER, spacing=2),
    Blink(pixels, speed=0.5, color=JADE),
    Comet(pixels, speed=0.01, color=PINK, tail_length=7, bounce=True),
    Chase(pixels, speed=0.1, size=3, spacing=6, color=OLD_LACE),
    ColorCycle(pixels, 0.5,
               colors=[RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA, BLACK]),
    Pulse(pixels, speed=0.1, color=AQUA, period=3),
    Sparkle(pixels, speed=0.05, color=GOLD, num_sparkles=3),
    Rainbow(pixels, speed=0.1, period=2),
    RainbowComet(pixels, speed=0.1, tail_length=7, bounce=True),
    RainbowChase(pixels, speed=0.1, size=5),
    RainbowSparkle(pixels, speed=0.1, num_sparkles=3),
]
animation = AnimationSequence(*animations, advance_interval=5)


def single_click_handler() -> None:
    animation.next()


def multi_click_handler() -> None:
    animation.previous()


def long_press_handler() -> None:
    animation.reset()


button = create_button(
    click=single_click_handler,
    multi_click=multi_click_handler,
    long_click=long_press_handler)

# Run the loop for 10 seconds
log.info("Press the button to change the animation.")
update_for(10, button, animation)

stop_animation(animation)
