import time

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.color import JADE

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.core.memory as memory
import cptkip.device.led as led
import cptkip.hal.pwmpin as pin
import cptkip.task.basic_runner as runner

memory.report_memory_usage()

log.set_log_level(log.INFO)

# TODO: Create the animation attached to the
# TODO: Whatever we do here we need to extend to button.

animation = Blink(led, speed=0.5, color=JADE)


async def animate() -> None:
    log.info('Single click!')
    led.value = not led.value


# Run the loop for 10 seconds
log.info("Press the button to change the LED.")
finish = time.monotonic() + 10


# Should we continue to run or not?
def should_continue() -> bool:
    return time.monotonic() < finish


# Executed once at the beginning and before any initial delay.
async def begin() -> None:
    log.info(f"{time.monotonic()}: BEGIN")
    led.off()
    # TODO: We could create the animation here


# Executed once at the end.
async def end() -> None:
    log.info(f"{time.monotonic()}: END")
    led.off()


task = led.create(
    pin.PwmPin(config.LED_PIN),
    update=animate,
    continue_func=should_continue,
    begin=begin,
    end=end)

runner.run([task])

memory.report_memory_usage_and_free()
