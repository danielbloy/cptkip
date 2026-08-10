#
# This example plays an MP3 audio file using the I2SAudio and Queue classes.
# A Button is used to add more "songs" to the queue as well as pause/unpause
# the audio. This example is almost identical to f_pwm_audio.py. Uses
# `cptkip.zero.audio`, `cptkip.zero.button` and `cptkip.zero.run`.
#

import cptkip.core.logging as log
from cptkip.zero.audio import create_i2s_queue
from cptkip.zero.button import create_button
from cptkip.zero.run import update_for

log.set_log_level(log.INFO)

AUDIO_FILE = "examples/lion.mp3"

queue = create_i2s_queue()


def single_click_handler() -> None:
    if queue.playing:
        if queue.paused:
            queue.resume()
        else:
            queue.pause()


def multi_click_handler() -> None:
    queue.queue(AUDIO_FILE)


button = create_button(click=single_click_handler, multi_click=multi_click_handler)

# Run the loop for 10 seconds
log.info("Press the button to pause/unpause the audio.")
log.info("Multi-press the button add a song to the queue.")
update_for(10, button, queue)

queue.deinit()
