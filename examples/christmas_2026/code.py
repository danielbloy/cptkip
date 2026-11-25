from adafruit_led_animation.animation.blink import Blink

import cptkip.config.configuration as config
from cptkip.animation.flicker import Flicker
from cptkip.zero.led import create_led, stop_animation, stop_led
from cptkip.zero.run import update_for

leds = [create_led(pin) for pin in config.LED_PINS]

# TODO: This may not be needed either
for led in leds:
    led.off()

# TODO: Individually select
animations = [
    Flicker(leds[config.TL], speed=0.5, color=(255, 255, 255), base=100, flame=155),
    Blink(leds[config.TR], speed=0.5, color=(255, 255, 255))
]

# TODO: All animations are uniform
animations = [Flicker(led, speed=0.5, color=(255, 255, 255), base=100, flame=155) for led in leds]
animations = [Blink(led, speed=0.5, color=(255, 255, 255)) for led in leds]

# TODO: Control the animations
animations[config.TL].freeze()
animations[config.TL].resume()
animations[config.TL].speed(1.0)
animations[config.TL].color((0, 0, 0))  # This might turn it off.

# TODO: AnimationSequence

# TODO: Migrate the zero/led change to core cptkip.

# TODO: Add the melody example with music.

update_for(3, *animations)

for animation in animations:
    stop_animation(animation)

# TODO: This may not be needed
for led in leds:
    stop_led(led)
