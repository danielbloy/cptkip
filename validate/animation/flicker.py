def execute():
    from adafruit_led_animation.color import AMBER

    import cptkip.animation.flicker as animation
    import cptkip.config.configuration as config
    import cptkip.device.pixels as pixel
    import validate.utils as utils

    utils.require_pins(config.PIXELS_PIN)

    with pixel.create(config.PIXELS_PIN, config.PIXELS_COUNT, brightness=0.5) as pixels:
        flicker = animation.Flicker(pixels, speed=1 / 20, color=AMBER, spacing=2)

        def task():
            flicker.animate()

        print("Pixels will display a flicker animation")
        utils.execute(task)


if __name__ == '__main__':
    execute()
