# This is designed to work with a Pimoroni Tiny 2040. If your board
# differs then adjust for the appropriate pins.

import time

import cptkip.core.environment as environment
import cptkip.core.logging as log

LED = None

if environment.are_pins_available():
    # noinspection PyPackageRequirements
    import board

    LED = board.LED_R

log.set_log_level(INFO)

runner = Runner()

led = Led(new_led_pin(LED))

led_animation = Blink(led, speed=0.5, color=WHITE)


async def animate_leds() -> None:
    if led_animation:
        led_animation.animate()


runner.add_loop_task(animate_leds)

# Allow the application to only run for a defined number of seconds.
finish = time.monotonic() + 10


async def callback() -> None:
    runner.cancel = time.monotonic() > finish


async def cleanup() -> None:
    led_animation.freeze()
    led.off()
    led.show()


runner.run(callback)
