import cptkip.config.configuration as config
from cptkip.pin.output_pin import OutputPin
from validate.performance.task_runner import execute

pin = OutputPin(config.LED_PIN, invert=config.LED_INVERT)


def task():
    pin.value = not pin.value


execute(task, False)
execute(task, True)

pin.off()

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
