from adafruit_led_animation.animation.blink import Blink

import cptkip.config.configuration as config
from cptkip.animation.flicker import Flicker
from cptkip.device.melody import decode_melody, Melody, MelodySequence
from cptkip.pin.output_pin import OutputPin
from cptkip.zero.button import create_button
from cptkip.zero.buzzer import create_buzzer_pin
from cptkip.zero.led import stop_animation, create_led
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
FLICKER = "Flicker"
BLINK = "BLink"

leds = {
    "tl": {
        "pin": config.TOP_LEFT_LED_PIN,
        "pwm": True,
        "animation": FLICKER,
    },
    "tc": {
        "pin": config.TOP_CENTRE_LED_PIN,
    },
    "tr": {
        "pin": config.TOP_RIGHT_LED_PIN,
    },
    "ml": {
        "pin": config.MIDDLE_LEFT_LED_PIN,
    },
    "mc": {
        "pin": config.MIDDLE_CENTRE_LED_PIN,
    },
    "mr": {
        "pin": config.MIDDLE_RIGHT_LED_PIN,
    },
    "bl": {
        "pin": config.BOTTOM_LEFT_LED_PIN,
    },
    "bc": {
        "pin": config.BOTTOM_CENTRE_LED_PIN,
    },
    "br": {
        "pin": config.BOTTOM_RIGHT_LED_PIN,
    },
}

for data in leds.values():
    pwm = data.get("pwm", False)
    pin = data["pin"]

    led = create_led(pin) if pwm else OutputPin(pin, invert=config.LED_INVERT)
    data["led"] = led

    animation = data.get("animation", BLINK)
    if pwm and data["animation"] == FLICKER:
        data["animation"] = Flicker(led, speed=0.5, color=255, base=100, flame=155),

    if pwm and data["animation"] == BLINK:
        data["animation"] = Blink(led, speed=0.5, color=255)

    if not pwm:
        data["animation"] = Blink(led, speed=0.5, color=255)

animations = [led["animation"] for led in leds if "animation" in led]

update_for(3, button, songs, *animations)
songs.pause()

for animation in animations:
    stop_animation(animation)
