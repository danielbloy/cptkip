def execute():
    from adafruit_led_animation.animation.rainbow import Rainbow

    import cptkip.config.configuration as config
    import cptkip.device.pixels as pixel
    import validate.utils as utils

    utils.require_pins(config.PIXELS_PIN)

    with pixel.create(config.PIXELS_PIN, config.PIXELS_COUNT, brightness=0.5) as pixels:
        animation = Rainbow(pixels, speed=0.1, period=2)
        animation.animate()

        def task():
            animation.animate()

        print("Pixels will display a rainbow animation")
        utils.execute(task)


if __name__ == '__main__':
    execute()
