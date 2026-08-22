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

# Try loading local device settings as overrides.
try:

    # noinspection PyPackageRequirements
    from config import *

    print("Config file loaded.")

except ImportError:
    print("No config file found.")

try:

    # noinspection PyPackageRequirements
    from device import *

    print("Device file loaded.")

except ImportError:
    print("No device file found.")

if 'LED_PIN' in locals() and LED_PIN:
    # noinspection string-conversion-without-dunder-method
    print("LED pin", LED_PIN)
else:
    print('LED not configured')

if 'BUTTON_PIN' in locals() and BUTTON_PIN:
    # noinspection string-conversion-without-dunder-method
    print("Button pin", BUTTON_PIN)
else:
    print('Button not configured')

if 'BUZZER_PIN' in locals() and BUZZER_PIN:
    # noinspection string-conversion-without-dunder-method
    print("Buzzer pin", BUZZER_PIN)
else:
    print('Buzzer not configured')

if 'PIXELS_PIN' in locals() and PIXELS_PIN:
    # noinspection string-conversion-without-dunder-method
    print("Pixels pin", PIXELS_PIN)
else:
    print('Pixels not configured')

if ('I2S_BIT_CLOCK' in locals() and 'I2S_LEFT_RIGHT_CLOCK' in locals() and 'I2S_DATA' in locals()
        and I2S_BIT_CLOCK and I2S_LEFT_RIGHT_CLOCK and I2S_DATA):
    # noinspection string-conversion-without-dunder-method
    print('I2S audio pins', I2S_BIT_CLOCK, I2S_LEFT_RIGHT_CLOCK, I2S_DATA)
else:
    print('I2S audio not configured')

# Apply logging level after both config.py and device.py have had a chance to
# override LOG_LEVEL.
log.set_log_level(LOG_LEVEL)
