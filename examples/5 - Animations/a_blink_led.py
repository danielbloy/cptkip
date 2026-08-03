#
# This example uses a Blink animation to blink the board LED.
#
import time

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.color import JADE

import cptkip.core.logging as log
import cptkip.task.basic_runner_async as runner
import cptkip.task.periodic_task_async as periodic_task
from cptkip.zero.led import create_led

log.set_log_level(log.INFO)

led = create_led()
animation = Blink(led, speed=0.5, color=JADE)


async def update() -> None:
    animation.animate()


# Run the loop for 5 seconds
finish = time.monotonic() + 5


# Should we continue to run or not?
def should_continue() -> bool:
    return time.monotonic() < finish


task = periodic_task.create(update, frequency=30, continue_func=should_continue)

runner.run([task])

animation.freeze()
led.off()
