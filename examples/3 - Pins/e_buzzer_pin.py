#
# This example demonstrates how to use the `volume` and `frequency`
# properties of a BuzzerPin to make sounds. It also uses the `on()`
# and `off()` methods.
#
import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.core.memory as memory
from cptkip.pin.buzzer_pin import BuzzerPin

memory.report_memory_usage()

log.set_log_level(log.INFO)

# Create the pin, set the frequency and volume.
pin = BuzzerPin(config.BUZZER_PIN)
pin.frequency = 300
pin.volume = 0.5
time.sleep(1)

# Loop, turning the pin on and off.
finish = time.monotonic() + 2
while time.monotonic() < finish:
    pin.off()
    time.sleep(0.25)
    pin.frequency += 300
    pin.on()
    time.sleep(0.25)

# Loop, turning the pin on and off.
finish = time.monotonic() + 2
while time.monotonic() < finish:
    pin.off()
    time.sleep(0.25)
    pin.frequency -= 300
    pin.on()
    time.sleep(0.25)

# Loop, getting quieter
pin.volume = 1.0
pin.frequency = 300
finish = time.monotonic() + 2

while time.monotonic() < finish:
    pin.volume -= 0.1
    time.sleep(0.25)

# Don't forget this
pin.off()

memory.report_memory_usage_and_free()
