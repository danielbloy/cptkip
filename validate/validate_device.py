import validate.device.button as button
import validate.device.buzzer as buzzer
import validate.device.led as led
import validate.device.melody as melody
import validate.device.pixels as pixels
import validate.device.pwm_audio as pwm_audio
import validate.utils as utils

modules = [button, led, pixels, buzzer, melody, pwm_audio]

if __name__ == '__main__':
    utils.execute_modules(modules)
