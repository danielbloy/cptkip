import cptkip.config.configuration as config
from cptkip.device.led import Led
from cptkip.pin.pwm_pin import PwmPin
from validate.performance.task_runner import execute

led_pin = PwmPin(config.LED_PIN, invert=config.LED_INVERT)
led = Led(led_pin)
led.brightness = 0.0


def task():
    led.brightness += 0.0001


execute(task, False)
execute(task, True)

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
