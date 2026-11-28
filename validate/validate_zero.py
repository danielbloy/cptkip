import validate.utils as utils
import validate.zero.zero_helpers as zero_helpers

modules = [zero_helpers]

if __name__ == '__main__':
    utils.exit_on_failure(utils.execute_modules(modules))
