import cptkip.config.configuration as config
from cptkip.device.button import Button
from cptkip.pin.input_pin import InputPin
from validate.performance.task_runner import execute

pin = InputPin(config.BUTTON_PIN, config.BUTTON_PULLUP)


def single_click_handler() -> None:
    print("Single click event")


def multi_click_handler() -> None:
    print("Multi-click event")


button = Button(pin, click=single_click_handler, multi_click=multi_click_handler)


def task():
    button.update()


execute(task, False)
execute(task, True)

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
