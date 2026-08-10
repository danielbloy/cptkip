# This example uses biplane to run a simple server that can respond to a
# single route which triggers some PWM audio through the buzzer. At the
# same time it is blinking the LED and flashing the NeoPixels. This is
# primarily showing how you can do multiple thinks at the same time
# whilst listening and responding to network messages.

from adafruit_led_animation.animation.blink import Blink
from adafruit_led_animation.animation.pulse import Pulse

import cptkip.core.logging as log
from cptkip.core.environment import is_running_under_test
from cptkip.network.biplane import Server, Response
from cptkip.task import memory_monitor_task
from cptkip.zero.audio import create_pwm_queue
from cptkip.zero.led import create_led, stop_animation as stop_led_animation
from cptkip.zero.pixels import create_pixels, stop_animation as stop_pixels_animation
from cptkip.zero.run import run_for

log.set_log_level(log.INFO)

AUDIO_FILE = "examples/lion.mp3"

queue = create_pwm_queue()

led = create_led()
led_animation = Blink(led, speed=0.5, color=(255, 255, 255))

pixels = create_pixels(brightness=0.5)
pixels_animation = Pulse(pixels, speed=0.1, color=(255, 0, 0), period=3)
server = Server()


@server.route("/", "GET")
def main(query_parameters, headers, body):
    queue.queue(AUDIO_FILE)
    return Response("<b>Queued roar!</b>", content_type="text/html")


monitor = memory_monitor_task.create(4, 1, lambda: True)
listen = server.create_task(lambda: True)


def run():
    listen()
    monitor()
    queue.update()
    led_animation.animate()
    pixels_animation.animate()


run_for(10 if is_running_under_test() else 60, run)

stop_led_animation(led_animation)
stop_pixels_animation(pixels_animation)
queue.deinit()
