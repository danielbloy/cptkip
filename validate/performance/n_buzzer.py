from time import monotonic

import cptkip.config.configuration as config
from cptkip.device.buzzer import Buzzer
from cptkip.pin.buzzer_pin import BuzzerPin
from validate.performance.task_runner import execute

pin = BuzzerPin(config.BUZZER_PIN)
buzzer = Buzzer(pin)
pin.volume = 0.1


def task():
    buzzer.update()
    global change
    now = monotonic()
    if now > change:
        change = now + 0.5
        buzzer.play(500, 0.4)


change = monotonic() + 0.5
execute(task, False)
pin.off()

# noinspection PyRedeclaration
change = monotonic() + 0.5
execute(task, True)
pin.off()

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
