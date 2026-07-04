#
# This example demonstrates using the configuration package to load user
# defined values into the framework. The LOG_LEVEL configuration value
# is treated special because it will change the logging level used by
# the framework as demonstrated in the example.
#
import cptkip.core.logging as logging

logging.info("This will not be displayed as the default log level is Warning")

# noinspection PyPep8
import cptkip.config.configuration as config

logging.info("This will be displayed as the configuration file changes the log level")

logging.info(f'Test value ... : {config.TEST_VALUE}')
logging.info(f'Test string .. : {config.TEST_STRING}')
logging.info(f'Debug ........ : {config.DEBUG}')
