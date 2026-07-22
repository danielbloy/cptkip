import cptkip.config.configuration as config
from cptkip.pin.pwm_pin import PwmPin
from validate.performance.task_runner import execute

pin = PwmPin(config.LED_PIN, invert=config.LED_INVERT)
pin.off()


def task():
    pin.value += 0.00001


execute(task, False)

pin.off()

execute(task, True)

pin.off()

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
