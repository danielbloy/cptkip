import cptkip.config.configuration as config
from cptkip.pin.buzzer_pin import BuzzerPin
from validate.performance.task_runner import execute

# Create the pin, set the frequency and volume.
pin = BuzzerPin(config.BUZZER_PIN)
pin.volume = 0.5


def task():
    pin.frequency += 10


pin.frequency = 300
pin.off()

execute(task, False)

pin.frequency = 300
pin.off()

execute(task, True)

pin.off()

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
