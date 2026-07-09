# We bundle core, configuration and cpu into the core validation test
# as a nod to simplification. We do however make sure we validate them
# in dependency order.

import validate.core.configuration as config
import validate.core.cpu as cpu
import validate.core.environment as environment
import validate.core.logging as logging
import validate.utils as utils

modules = [environment, logging, config, cpu]

if __name__ == '__main__':
    utils.execute_modules(modules)
