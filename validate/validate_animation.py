import validate.animation.flicker as flicker
import validate.utils as utils

modules = [flicker]

if __name__ == '__main__':
    utils.exit_on_failure(utils.execute_modules(modules))
