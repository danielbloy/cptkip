#
# This example plays an MP3 audio file using the Audio and Queue classes.
# A Button is used to add more "songs" to the queue as well as pause/unpause
# the audio.
#
import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.core.memory as memory
from cptkip.device.button import Button
from cptkip.device.pwm_audio import Audio, Queue
from cptkip.pin.input_pin import InputPin

memory.report_memory_usage()

log.set_log_level(log.INFO)

AUDIO_FILE = "examples/lion.mp3"

audio = Audio(config.BUZZER_PIN)
queue = Queue(audio)


def single_click_handler() -> None:
    if queue.playing:
        if queue.paused:
            queue.resume()
        else:
            queue.pause()


def multi_click_handler() -> None:
    queue.queue(AUDIO_FILE)


input_pin = InputPin(config.BUTTON_PIN, config.BUTTON_PULLUP)
button = Button(input_pin, click=single_click_handler, multi_click=multi_click_handler)

# Run the loop for 10 seconds
log.info("Press the button to pause/unpause the audio.")
log.info("Multi-press the button add a song to the queue.")
finish = time.monotonic() + 10

while time.monotonic() < finish:
    button.update()
    queue.update()

audio.deinit()

memory.report_memory_usage_and_free()
