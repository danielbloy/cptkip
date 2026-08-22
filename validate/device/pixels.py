def execute():
    from adafruit_led_animation.animation.rainbow import Rainbow

    import cptkip.config.configuration as config
    import cptkip.device.pixels as pixel
    import validate.utils as utils

    with pixel.create(config.PIXELS_PIN, 8, brightness=0.5) as pixels:
        animation = Rainbow(pixels, speed=0.1, period=2)
        animation.animate()

        def task():
            animation.animate()

        print("Pixels will display a rainbow animation")
        utils.execute(task)


if __name__ == '__main__':
    execute()
