# The configuration values loaded in here are expected can be overridden
# through settings in a config.py file which is located in the same place
# as the working directory when the application is executed.
import cptkip.core.logging as logging
from cptkip.core.environment import is_running_on_desktop

LOG_LEVEL = logging.WARNING

# Try loading local device settings as overrides.
try:

    if is_running_on_desktop():
        # noinspection PyUnusedImports
        import importlib.util

        config = importlib.import_module('config')
        config = importlib.reload(config)
    else:
        # FUTURE: This could benefit from further investigation to see if we can
        #         do something better. See the notes in import_driver().
        config = __import__('config')

    print(f"Config file {config.__file__} loaded.")

    # noinspection PyPackageRequirements
    from config import *

    print("Config file loaded.")

except ImportError:
    print("No config file found.")

logging.set_log_level(LOG_LEVEL)
