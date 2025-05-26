def execute():
    import time

    from adafruit_led_animation.color import AMBER

    import cptkip.animation.flicker as animation
    import cptkip.config.configuration as config
    import cptkip.device.pixels as pixel
    import cptkip.task.basic_runner_async as runner

    pixels = pixel.create(config.PIXELS_PIN, 8, brightness=0.5)
    flicker = animation.Flicker(pixels, speed=0.1, color=AMBER, spacing=2)

    # Run the loop for 5 seconds
    finish = time.monotonic() + 2

    async def animate() -> None:
        while time.monotonic() < finish:
            flicker.animate()

    runner.run([animate])

    flicker.freeze()
    pixels.fill(pixel.OFF)
    pixels.write()


if __name__ == '__main__':
    execute()
