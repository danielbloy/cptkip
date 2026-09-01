#
# This example demonstrates how to use the `volume` and `frequency`
# properties of a BuzzerPin to make sounds. It also uses the `on()`
# and `off()` methods as well as the `toggle()` method.
#
import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
from cptkip.pin.buzzer_pin import BuzzerPin

# Create the pin, set the frequency and volume.
with BuzzerPin(config.BUZZER_PIN) as pin:
    log.info("Play for 1 second")
    pin.frequency = 300
    pin.volume = 0.5
    time.sleep(1)

    log.info("Increasing frequency")
    finish = time.monotonic() + 2
    while time.monotonic() < finish:
        pin.off()
        time.sleep(0.125)
        pin.frequency += 300
        pin.on()
        time.sleep(0.125)

    log.info("Decreasing frequency")
    finish = time.monotonic() + 2
    while time.monotonic() < finish:
        pin.off()
        time.sleep(0.125)
        pin.frequency -= 300
        pin.on()
        time.sleep(0.125)

    log.info("Getting quieter")
    pin.volume = 1.0
    pin.frequency = 300
    finish = time.monotonic() + 2

    while time.monotonic() < finish:
        pin.volume -= 0.1
        time.sleep(0.25)

    log.info("Using toggle() to control the buzzer")
    pin.volue = 0.25
    finish = time.monotonic() + 2

    while time.monotonic() < finish:
        pin.toggle()
        time.sleep(0.25)
