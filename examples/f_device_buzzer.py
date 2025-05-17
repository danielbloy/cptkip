import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.core.memory as memory
import cptkip.pin.buzzerpin as buzzerpin
from cptkip.device.buzzer import Buzzer

memory.report_memory_usage()

log.set_log_level(log.INFO)

pin = buzzerpin.BuzzerPin(config.BUZZER_PIN)
buzzer = Buzzer(pin)

buzzer.beep()
finish = time.monotonic() + 0.5
while time.monotonic() < finish:
    buzzer.update()

pin.volume = 0.5

buzzer.beeps(4)
finish = time.monotonic() + 2.5
while time.monotonic() < finish:
    buzzer.update()

# Get quieter
pin.volume = 1.0
buzzer.play(500, 3)
finish = time.monotonic() + 2

while time.monotonic() < finish:
    pin.volume -= 0.1
    time.sleep(0.25)

buzzer.off()

memory.report_memory_usage_and_free()
