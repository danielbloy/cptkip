#
# This example plays an MP3 audio file using the PwmAudio and Queue classes.
# A Button is used to add more "songs" to the queue as well as pause/unpause
# the audio. This example is almost identical to g_i2sß_audio.py. Uses
# `cptkip.zero.audio`, `cptkip.zero.button` and `cptkip.zero.run`.
#

import cptkip.core.logging as log
from cptkip.zero.audio import create_pwm_queue
from cptkip.zero.button import create_button
from cptkip.zero.run import update_for

log.set_log_level(log.INFO)

AUDIO_FILE = "examples/lion.mp3"

with create_pwm_queue() as queue:
    queue.queue(AUDIO_FILE)


    def single_click_handler() -> None:
        if queue.playing:
            if queue.paused:
                queue.resume()
            else:
                queue.pause()


    def multi_click_handler() -> None:
        queue.queue(AUDIO_FILE)


    with create_button(click=single_click_handler, multi_click=multi_click_handler) as button:
        log.info("Press the button to pause/unpause the audio.")
        log.info("Multi-press the button add a song to the queue.")

        update_for(5, button, queue)
