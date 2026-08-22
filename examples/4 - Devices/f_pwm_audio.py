#
# This example plays an MP3 audio file using the PwmAudio and Queue classes.
# A Button is used to add more "songs" to the queue as well as pause/unpause
# the audio. This example is almost identical to g_i2sß_audio.py.
#
import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
from cptkip.device.audio import PwmAudio as Audio, Queue
from cptkip.device.button import Button
from cptkip.pin.input_pin import InputPin

log.set_log_level(log.INFO)

AUDIO_FILE = "examples/lion.mp3"

with Queue(Audio(config.BUZZER_PIN)) as queue:
    queue.queue(AUDIO_FILE)


    def single_click_handler() -> None:
        if queue.playing:
            if queue.paused:
                queue.resume()
            else:
                queue.pause()


    def multi_click_handler() -> None:
        queue.queue(AUDIO_FILE)


    with Button(
            InputPin(config.BUTTON_PIN, config.BUTTON_PULLUP),
            click=single_click_handler,
            multi_click=multi_click_handler) as button:

        log.info("Press the button to pause/unpause the audio.")
        log.info("Multi-press the button add a song to the queue.")
        finish = time.monotonic() + 5

        while time.monotonic() < finish:
            button.update()
            queue.update()
