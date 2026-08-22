#
# This example loops and reads the InputPin which is connected to the
# boards button.
#
import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
from cptkip.pin.input_pin import InputPin

log.set_log_level(log.INFO)

with InputPin(config.BUTTON_PIN, config.BUTTON_PULLUP) as input_pin:
    finish = time.monotonic() + 5

    while time.monotonic() < finish:
        log.info(f"Input value: {input_pin.value}")
        time.sleep(0.25)
