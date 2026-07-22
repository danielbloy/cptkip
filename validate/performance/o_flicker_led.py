import cptkip.config.configuration as config
from cptkip.animation.flicker import Flicker
from cptkip.device.led import Led
from cptkip.pin.pwm_pin import PwmPin
from validate.performance.task_runner import execute

pin = PwmPin(config.LED_PIN, invert=config.LED_INVERT)
led = Led(pin)
animation = Flicker(led, speed=0.1, color=(255, 255, 255), base=100, flame=155)


def task():
    animation.animate()


execute(task, False)
execute(task, True)
animation.freeze()
led.off()
led.show()

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
