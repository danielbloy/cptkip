import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.core.memory as memory
import cptkip.device.pwm_audio as pwmaudio
import cptkip.pin.inputpin as inputpin
from cptkip.device.button import Button

memory.report_memory_usage()

log.set_log_level(log.INFO)

AUDIO_FILE = "examples/lion.mp3"

audio = pwmaudio.Audio(config.BUZZER_PIN)
queue = pwmaudio.Queue(audio)


def single_click_handler() -> None:
    if queue.playing:
        if queue.paused:
            queue.resume()
        else:
            queue.pause()


def multi_click_handler() -> None:
    queue.queue(AUDIO_FILE)


input_pin = inputpin.InputPin(config.BUTTON_PIN)
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
