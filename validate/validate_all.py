# This script runs all the validation tests. It is a convenient way to
# test a large subset of the functionality on a single device.

import validate.utils as utils
import validate.validate_core as core

scripts = [core]


def execute():
    for script in scripts:
        modules = script.modules
        utils.execute_modules(modules)


if __name__ == '__main__':
    execute()
