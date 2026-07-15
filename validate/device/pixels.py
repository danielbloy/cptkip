def execute():
    from adafruit_led_animation.animation.rainbow import Rainbow

    import cptkip.config.configuration as config
    import cptkip.device.pixels as pixel
    import validate.utils as utils

    # Use the PIXELS pin
    pixels = pixel.create(config.PIXELS_PIN, 8, brightness=0.5)
    animation = Rainbow(pixels, speed=0.1, period=2)
    animation.animate()

    def task():
        animation.animate()

    print("Pixels will display a rainbow animation")
    utils.execute(task)

    animation.freeze()
    del animation

    pixels.fill(pixel.OFF)
    pixels.write()

    pixels.deinit()
    del pixels


if __name__ == '__main__':
    execute()
