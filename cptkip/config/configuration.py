# The configuration values loaded in here are expected can be overridden
# through settings in a `config.py` file which is located in the same place
# as the working directory when the application is executed.
#
# The `config.py` file is useful for general purpose configuration settings
# that are fairly universal and control the application. An additional file
# called `device.py` is also loaded if present and this is to be used to load
# device specific settings which will override those from `config.py`.

import cptkip.core.logging as log

LOG_LEVEL = log.WARNING

# Defaults for the hardware settings used by cptkip.zero and the examples. A pin of
# None means the device is not connected/configured. These are overridden by
# config.py and device.py; defining them here means a config.py that omits one does
# not cause an AttributeError when it is used.
LED_PIN = None
LED_INVERT = False

BUTTON_PIN = None
BUTTON_PULLUP = True

BUZZER_PIN = None

PIXELS_PIN = None
PIXELS_COUNT = 1

I2S_BIT_CLOCK = None
I2S_LEFT_RIGHT_CLOCK = None
I2S_DATA = None

# Try loading local device settings as overrides.
__config_loaded = False
try:

    # noinspection PyPackageRequirements
    from config import *

    __config_loaded = True

except ImportError:
    pass

__device_loaded = False
try:

    # noinspection PyPackageRequirements
    from device import *

    __device_loaded = True

except ImportError:
    pass


def report() -> None:
    """
    Prints which configuration files were loaded and which devices are configured.
    This is called automatically when the configuration is loaded if LOG_LEVEL is
    INFO or above; otherwise nothing is printed.
    """
    print("Config file loaded." if __config_loaded else "No config file found.")
    print("Device file loaded." if __device_loaded else "No device file found.")

    # print() with multiple args avoids building temporary strings.
    if LED_PIN:
        print("LED pin", LED_PIN)
    else:
        print("LED not configured")

    if BUTTON_PIN:
        print("Button pin", BUTTON_PIN)
    else:
        print("Button not configured")

    if BUZZER_PIN:
        print("Buzzer pin", BUZZER_PIN)
    else:
        print("Buzzer not configured")

    if PIXELS_PIN:
        print("Pixels pin", PIXELS_PIN)
    else:
        print("Pixels not configured")

    if I2S_BIT_CLOCK and I2S_LEFT_RIGHT_CLOCK and I2S_DATA:
        print("I2S audio pins", I2S_BIT_CLOCK, I2S_LEFT_RIGHT_CLOCK, I2S_DATA)
    else:
        print("I2S audio not configured")


# Apply logging level after both config.py and device.py have had a chance to
# override LOG_LEVEL.
log.set_log_level(LOG_LEVEL)

if LOG_LEVEL >= log.INFO:
    report()
