from time import monotonic

import cptkip.config.configuration as config
from cptkip.pin.buzzer_pin import BuzzerPin
from validate.performance.task_runner import execute

# Create the pin, set the frequency and volume.
pin = BuzzerPin(config.BUZZER_PIN)
pin.volume = 0.1


def task():
    global change
    now = monotonic()
    if now > change:
        change = now + 0.01
        pin.frequency += 1


change = monotonic() + 0.01
pin.play(300)
execute(task, False)
pin.off()

# noinspection PyRedeclaration
change = monotonic() + 0.01
pin.play(300)
execute(task, True)
pin.off()

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
