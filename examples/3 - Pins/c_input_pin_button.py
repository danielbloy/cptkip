#
# This example loops and reads the InputPin which is connected to the
# boards button.
#
import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
from cptkip.pin.input_pin import InputPin

log.set_log_level(log.INFO)

input_pin = InputPin(config.BUTTON_PIN, config.BUTTON_PULLUP)

# Run the loop for 10 seconds
finish = time.monotonic() + 10

while time.monotonic() < finish:
    log.info("Input value: {}".format(input_pin.value))
    time.sleep(0.25)
