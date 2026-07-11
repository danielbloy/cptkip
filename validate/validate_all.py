# This script runs all the validation tests. It is a convenient way to
# test a large subset of the functionality on a single device.
import validate.utils as utils
import validate.validate_animation as animation
import validate.validate_core as core
import validate.validate_device as device
import validate.validate_performance as performance
import validate.validate_pin as pin
import validate.validate_task as task

scripts = [core, task, pin, device, animation, performance]


def execute():
    for script in scripts:
        modules = script.modules
        utils.execute_modules(modules)


if __name__ == '__main__':
    execute()
