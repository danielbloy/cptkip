import validate.core.environment as environment
import validate.core.logging as logging
import validate.utils as utils

modules = [environment, logging]

if __name__ == '__main__':
    utils.execute_modules(modules)
