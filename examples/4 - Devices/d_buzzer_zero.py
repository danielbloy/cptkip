#
# This example demonstrates using the Buzzer which provides more
# control for beeping and playing notes for a duration than a
# plain BuzzerPin. Uses `cptkip.zero.buzzer` and `cptkip.zero.run`.
#
import time

import cptkip.core.logging as log
from cptkip.zero.buzzer import create_buzzer
from cptkip.zero.run import run_for

log.set_log_level(log.INFO)

with create_buzzer() as buzzer:
    buzzer.beeps(2)
    run_for(1, lambda: buzzer.update())

    buzzer.volume = 0.5

    buzzer.beeps(4)
    run_for(2.5, lambda: buzzer.update())

    # Get quieter
    buzzer.volume = 1.0
    buzzer.play(500, 3)


    def get_quieter():
        buzzer.volume -= 0.1
        time.sleep(0.25)


    run_for(2, get_quieter)
