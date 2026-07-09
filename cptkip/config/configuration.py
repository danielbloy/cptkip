# The configuration values loaded in here are expected can be overridden
# through settings in a config.py file which is located in the same place
# as the working directory when the application is executed.

import cptkip.core.logging as logging

LOG_LEVEL = logging.WARNING

# Try loading local device settings as overrides.
try:

    # noinspection PyPackageRequirements
    from config import *

    print("Config file loaded.")

    # TODO: Take inspiration from pmpge and add support for device specific config
    #       as well as application specific config

    # TODO: We could potentially output the configuration values.

except ImportError:
    print("No config file found.")

logging.set_log_level(LOG_LEVEL)
