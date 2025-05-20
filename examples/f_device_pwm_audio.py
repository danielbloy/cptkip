import time
from email.utils import decode_rfc2231

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.core.memory as memory
import cptkip.pin.inputpin as inputpin
import cptkip.pin.pwmaudio as audio
from cptkip.device.button import Button

memory.report_memory_usage()

log.set_log_level(log.INFO)

AUDIO_FILE = "lion.mp3"

pin = ???
decoder = ???
audio = audio.Audio(pin, decoder)

queue = audio.Queue()

def single_click_handler() -> None:
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
    queue.play()

pin.off()

memory.report_memory_usage_and_free()
