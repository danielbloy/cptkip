# TODO: Convert to cptkip
import time

from interactive.animation import Flicker
from interactive.button import ButtonController
from interactive.environment import are_pins_available, is_running_on_microcontroller
from interactive.led import Led
from interactive.log import set_log_level, INFO, info
from interactive.memory import report_memory_usage_and_free
from interactive.polyfills.animation import BLACK, WHITE, AnimationSequence
from interactive.polyfills.animation import Blink, Pulse
from interactive.polyfills.button import new_button
from interactive.polyfills.led import new_led_pin
from interactive.polyfills.pixel import new_pixels
from interactive.runner import Runner
from interactive.scheduler import new_one_time_on_off_task

PIXELS_PIN = None  # This is the single onboard NeoPixel connector

if are_pins_available():
    # noinspection PyPackageRequirements
    import board

    PIXELS_PIN = board.GP28

if __name__ == '__main__':

    set_log_level(INFO)

    runner = Runner()

    pixels = new_pixels(PIXELS_PIN, 8, brightness=0.5)
    animations = [
        Flicker(pixels, speed=0.1, color=AMBER, spacing=2),
        Blink(pixels, speed=0.5, color=JADE),
        Comet(pixels, speed=0.01, color=PINK, tail_length=7, bounce=True),
        Chase(pixels, speed=0.1, size=3, spacing=6, color=OLD_LACE),
        ColorCycle(pixels, 0.5, colors=[RED, YELLOW, ORANGE, GREEN, TEAL, CYAN, BLUE, PURPLE, MAGENTA, BLACK]),
        Pulse(pixels, speed=0.1, color=AQUA, period=3),
        Sparkle(pixels, speed=0.05, color=GOLD, num_sparkles=3),
        Rainbow(pixels, speed=0.1, period=2),
        RainbowComet(pixels, speed=0.1, tail_length=7, bounce=True),
        RainbowChase(pixels, speed=0.1, size=5),
        RainbowSparkle(pixels, speed=0.1, num_sparkles=3),
    ]
    animation = AnimationSequence(*animations, advance_interval=5)


    async def animate_pixels() -> None:
        if not runner.cancel:
            if animation:
                animation.animate()


    runner.add_loop_task(animate_pixels)

    # Allow the application to only run for a defined number of seconds.
    finish = time.monotonic() + 10


    async def callback() -> None:
        runner.cancel = time.monotonic() > finish
        if runner.cancel:
            animation.freeze()
            pixels.fill(BLACK)
            pixels.write()


    runner.run(callback)
