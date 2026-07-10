import validate.pin.buzzer_pin as buzzer_pin
import validate.pin.input_pin as input_pin
import validate.pin.output_pin as output_pin
import validate.pin.pwm_pin as pwm_pin
import validate.utils as utils

modules = [input_pin, output_pin, pwm_pin, buzzer_pin]

if __name__ == '__main__':
    utils.execute_modules(modules)
