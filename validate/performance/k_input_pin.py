import cptkip.config.configuration as config
from cptkip.pin.input_pin import InputPin
from validate.performance.task_runner import execute

pin = InputPin(config.BUTTON_PIN, config.BUTTON_PULLUP)


def task():
    _ = pin.value


execute(task, False)
execute(task, True)

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
