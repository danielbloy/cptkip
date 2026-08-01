#
# This example uses biplane to run a simple server that can respond to a
# single route which triggers some PWM audio through the buzzer. At the
# same time it is blinking the LED and flashing the NeoPixels.
#
import time

from adafruit_led_animation.animation.blink import Blink

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.device.pixels as pixel
from cptkip.core.environment import is_running_under_test
from cptkip.device.audio import PwmAudio as Audio, Queue
from cptkip.device.led import Led
from cptkip.network.biplane import Server, Response
from cptkip.pin.pwm_pin import PwmPin
from cptkip.task import memory_monitor_task

log.set_log_level(log.INFO)

AUDIO_FILE = "examples/lion.mp3"

audio = Audio(config.BUZZER_PIN)
queue = Queue(audio)

pin = PwmPin(config.LED_PIN, invert=config.LED_INVERT)
led = Led(pin)
animation = Blink(led, speed=0.5, color=(255, 255, 255))

pixels = pixel.create(config.PIXELS_PIN, 8, brightness=0.5)

r = 10
rdx = 10


def pulse_pixels():
    global change, r, rdx
    now = time.monotonic()
    if now > change:
        change = now + 0.02
        r += rdx
        if r > 200:
            rdx = -10
        if r < 40:
            rdx = 10

        pixels.fill((r, 0, 0))
        pixels.write()


server = Server()


@server.route("/", "GET")
def main(query_parameters, headers, body):
    queue.queue(AUDIO_FILE)
    return Response("<b>Queued roar!</b>", content_type="text/html")


monitor = memory_monitor_task.create(4, 1, lambda: True)
listen = server.create_task(lambda: True)

finish = time.monotonic() + (10 if is_running_under_test() else 120)
change = time.monotonic() + 0.01

while time.monotonic() < finish:
    listen()
    monitor()
    queue.update()
    animation.animate()
    pulse_pixels()

animation.freeze()

led.off()
led.show()

pixels.fill(pixel.OFF)
pixels.write()
