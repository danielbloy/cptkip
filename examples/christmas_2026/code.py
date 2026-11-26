from adafruit_led_animation.animation.blink import Blink

import cptkip.config.configuration as config
from cptkip.device.melody import decode_melody, Melody, MelodySequence
from cptkip.pin.output_pin import OutputPin
from cptkip.zero.button import create_button
from cptkip.zero.buzzer import create_buzzer_pin
from cptkip.zero.led import create_led, stop_animation
from cptkip.zero.run import update_for
from songs import JINGLE_BELLS, RUDOLPH, SANTA_GOT_STUCK, MERRY_CHRISTMAS

################################################################################
# S O U N D
################################################################################
buzzer = create_buzzer_pin()

jingle_bells = Melody(buzzer, decode_melody(JINGLE_BELLS), 480)
rudolph = Melody(buzzer, decode_melody(RUDOLPH), 480)
santa_got_stuck = Melody(buzzer, decode_melody(SANTA_GOT_STUCK), 480)
merry_christmas = Melody(buzzer, decode_melody(MERRY_CHRISTMAS), 480)
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
LED_PINS = [
    TOP_LEFT_LED_PIN, TOP_CENTRE_LED_PIN, TOP_RIGHT_LED_PIN,
    MIDDLE_LEFT_LED_PIN, MIDDLE_CENTRE_LED_PIN, MIDDLE_RIGHT_LED_PIN,
    BOTTOM_LEFT_LED_PIN, BOTTOM_CENTRE_LED_PIN, BOTTOM_RIGHT_LED_PIN
]

TL = 0
TC = 1
TR = 2
ML = 3
MC = 4
MR = 5
BL = 6
BC = 7
BR = 9
# leds = [create_led(pin) for pin in config.LED_PINS]
leds = [OutputPin(pin, invert=config.LED_INVERT) for pin in config.LEDS]

# TODO: Individually select
animations = [
    Blink(create_led(config.MIDDLE_LEFT_LED_PIN), speed=0.5, color=255),
    Blink(create_led(config.MIDDLE_CENTRE_LED_PIN), speed=0.5, color=255),
    # Flicker(create_led(config.MIDDLE_RIGHT_LED_PIN), speed=0.5, color=255, base=100, flame=155),
]

# TODO: All animations are uniform
# animations = [Flicker(led, speed=0.1, color=255, base=100, flame=155) for led in leds]
# animations = [Blink(led, speed=0.1, color=255) for led in leds]


# TODO: Control the animations
# animations[config.TL].freeze()
# animations[config.TL].resume()
animations[0].speed = 0.1
animations[0].color = 30
# This turns the LED off
# leds[config.TL].off()
# leds[config.TL].show()

update_for(3, button, songs, *animations)
songs.pause()

for animation in animations:
    stop_animation(animation)
