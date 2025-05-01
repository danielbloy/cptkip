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

LED_YELLOW = None
LED_GREEN = None
LED_RED = None

if are_pins_available():
    # noinspection PyPackageRequirements
    import board

    LED_YELLOW = board.GP6
    LED_GREEN = board.GP5
    LED_RED = board.GP1

if __name__ == '__main__':

    set_log_level(INFO)

    runner = Runner()

    yellow = Led(new_led_pin(LED_YELLOW))
    green = Led(new_led_pin(LED_GREEN))
    red = Led(new_led_pin(LED_RED))

    red_animation = Blink(red, speed=0.5, color=WHITE)
    green_animation = Pulse(green, speed=0.1, color=WHITE, period=2)

    yellow_animations = [
        Flicker(yellow, speed=0.1, color=WHITE),
        Pulse(yellow, speed=0.1, color=WHITE, period=1),
        Blink(yellow, speed=0.5, color=WHITE),
    ]
    yellow_animation = AnimationSequence(*yellow_animations, advance_interval=3)


    async def animate_leds() -> None:
        if not runner.cancel:
            if red_animation:
                red_animation.animate()
            if green_animation:
                green_animation.animate()
            if yellow_animation:
                yellow_animation.animate()


    runner.add_loop_task(animate_leds)

    # Allow the application to only run for a defined number of seconds.
    finish = time.monotonic() + 10


    async def callback() -> None:
        runner.cancel = time.monotonic() > finish
        if runner.cancel:
            yellow_animation.freeze()
            green_animation.freeze()
            red_animation.freeze()

            yellow.off()
            green.off()
            red.off()
            yellow.show()
            green.show()
            red.show()


    runner.run(callback)
