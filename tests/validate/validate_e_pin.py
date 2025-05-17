def execute():
    import time

    from adafruit_led_animation.animation.rainbow import Rainbow

    import cptkip.pin.digitalpin as digitalpin
    import cptkip.pin.pwmpin as pwmpin
    import cptkip.pin.pixels as pixel

    import cptkip.config.configuration as config

    # Use the LED as an output pin
    pin = digitalpin.OutputPin(config.LED_PIN, invert=config.LED_INVERT)
    finish = time.monotonic() + 2
    while time.monotonic() < finish:
        pin.on()
        time.sleep(0.25)
        pin.off()
        time.sleep(0.25)

    pin.deinit()
    del pin

    pin = pwmpin.PwmPin(config.LED_PIN, invert=config.LED_INVERT)
    finish = time.monotonic() + 2
    while time.monotonic() < finish:
        pin.on()
        time.sleep(0.25)
        pin.off()
        time.sleep(0.25)

    pin.deinit()
    del pin

    # Use the BUTTON as an input pin
    pin = digitalpin.InputPin(config.BUTTON_PIN)
    finish = time.monotonic() + 2
    while time.monotonic() < finish:
        assert pin.value
        time.sleep(0.25)

    pin.deinit()
    del pin

    # Use the PIXELS pin
    pixels = pixel.create(config.PIXELS_PIN, 8, brightness=0.5)
    animation = Rainbow(pixels, speed=0.1, period=2)
    animation.animate()
    finish = time.monotonic() + 2
    while time.monotonic() < finish:
        animation.animate()

    animation.freeze()
    del animation

    pixels.fill(pixel.OFF)
    pixels.write()

    pixels.deinit()
    del pixels


if __name__ == '__main__':
    execute()
