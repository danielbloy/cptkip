#
# This example demonstrates using the Buzzer which provides more
# control for beeping and playing notes for a duration than a
# plain BuzzerPin. Uses `cptkip.zero.buzzer`.
#
import time

import cptkip.core.logging as log
from cptkip.zero.buzzer import create_buzzer

log.set_log_level(log.INFO)

buzzer = create_buzzer()

buzzer.beep()
buzzer.beep()
finish = time.monotonic() + 1.0
while time.monotonic() < finish:
    buzzer.update()

buzzer.volume = 0.5

buzzer.beeps(4)
finish = time.monotonic() + 2.5
while time.monotonic() < finish:
    buzzer.update()

# Get quieter
buzzer.volume = 1.0
buzzer.play(500, 3)
finish = time.monotonic() + 2

while time.monotonic() < finish:
    buzzer.volume -= 0.1
    time.sleep(0.25)

buzzer.off()
