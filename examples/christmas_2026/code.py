from adafruit_led_animation.animation.blink import Blink

import cptkip.config.configuration as config
from cptkip.animation.flicker import Flicker
from cptkip.device.melody import decode_melody, Melody, MelodySequence
from cptkip.zero.button import create_button
from cptkip.zero.buzzer import create_buzzer_pin
from cptkip.zero.led import create_led, stop_animation, stop_led
from cptkip.zero.run import update_for

################################################################################
# S O U N D
################################################################################
buzzer = create_buzzer_pin()

jingle_bells = Melody(buzzer, decode_melody(config.JINGLE_BELLS), 480)
rudolph = Melody(buzzer, decode_melody(config.RUDOLPH), 480)
santa_got_stuck = Melody(buzzer, decode_melody(config.SANTA_GOT_STUCK), 480)
merry_christmas = Melody(buzzer, decode_melody(config.MERRY_CHRISTMAS), 480)
songs = MelodySequence(jingle_bells, rudolph, santa_got_stuck, merry_christmas)


################################################################################
# B U T T O N
################################################################################
def single_click_handler() -> None:
    if songs.paused:
        songs.resume()
    else:
        songs.pause()


def multi_click_handler() -> None:
    songs.reset()


button = create_button(click=single_click_handler, multi_click=multi_click_handler)

################################################################################
# L E D S
################################################################################
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

# TODO: Migrate the zero/led change to core cptkip.


update_for(3, *animations)

for animation in animations:
    stop_animation(animation)

# TODO: This may not be needed
for led in leds:
    stop_led(led)
