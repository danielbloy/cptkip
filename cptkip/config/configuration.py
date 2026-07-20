# The configuration values loaded in here are expected can be overridden
# through settings in a `config.py` file which is located in the same place
# as the working directory when the application is executed.
#
# The `config.py` file is useful for general purpose configuration settings
# that are fairly universal and control the application. An additional file
# called `device.py` is also loaded if present and this is to be used to load
# device specific settings which will override those from `config.py`.

import cptkip.core.logging as logging

LOG_LEVEL = logging.WARNING

# Try loading local device settings as overrides.
try:

    # noinspection PyPackageRequirements
    from config import *

    print("Config file loaded.")

except ImportError:
    print("No config file found.")

logging.set_log_level(LOG_LEVEL)

try:

    # noinspection PyPackageRequirements
    from device import *

    print("Device file loaded.")

except ImportError:
    print("No device file found.")
