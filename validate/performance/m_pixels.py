from time import monotonic

import cptkip.config.configuration as config
import cptkip.device.pixels as pixel
from validate.performance.task_runner import execute

pixels = pixel.create(config.PIXELS_PIN, 8, brightness=0.5)

r = 10
rdx = 10


def task():
    global change, r, rdx
    now = monotonic()
    if now > change:
        change = now + 0.02
        r += rdx
        if r > 200:
            rdx = -10
        if r < 40:
            rdx = 10

        pixels.fill((r, 0, 0))
        pixels.write()


change = monotonic() + 0.01
execute(task, False)
execute(task, True)

pixels.fill(pixel.OFF)
pixels.write()

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
