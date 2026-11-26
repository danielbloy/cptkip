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


animations = []
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

    if pwm:
        animations.append(data["animation"])

    if not pwm:
        data["animation"] = Blink(led, speed=0.5, color=255)

flicker = Flicker(leds["tl"]["pin"], speed=0.5, color=255, base=100, flame=155)
update_for(3, button, songs)
songs.pause()
