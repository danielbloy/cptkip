import cptkip.core.logging as logging

logging.info("This will not be displayed as the default log level is Warning")

import cptkip.config.configuration as config

print('Test value ... :', config.TEST_VALUE)
print('Test string .. :', config.TEST_STRING)
print('Debug ........ :', config.DEBUG)

logging.info("This will be displayed as the configuration file changes the log level")
