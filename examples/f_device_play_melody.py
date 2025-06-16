import time

import cptkip.config.configuration as config
import cptkip.core.logging as log
import cptkip.core.memory as memory
import cptkip.device.melody as melody
import cptkip.pin.buzzer_pin as buzzerpin
import cptkip.pin.input_pin as inputpin
from cptkip.device.button import Button

memory.report_memory_usage()

log.set_log_level(log.INFO)

pin = buzzerpin.BuzzerPin(config.BUZZER_PIN)
pin.volume = 0.1

scale = '''C4:1 D:1 E:1 F:1 G:1 A:1 B:1 C5:1
           B4:1 A:1 G:1 F:1 E:1 D:1 C:1'''

jingle_bells = [
    "E4:2", "E:2", "E:4", "E:2", "E:2", "E:4",
    "E:2", "G:2", "C:2", "D:2", "E:8",
    "F:2", "F:2", "F:2", "F:2", "F:2", "E:2", "E:2", "E:1", "E:1",
    "E:2", "D:2", "D:2", "E:2", "D:4", "G:2", "R:2",
    "E:2", "E:2", "E:4", "E:2", "E:2", "E:4",
    "E:2", "G:2", "C:2", "D:2", "E:8",
    "F:2", "F:2", "F:2", "F:2", "F:2", "E:2", "E:2", "E:1", "E:1",
    "G:2", "G:2", "F:2", "D:2", "C:8",
    "R:8"]

melody_sequence = melody.MelodySequence(
    melody.Melody(pin, melody.decode_melody(scale.split()), 240),
    melody.Melody(pin, melody.decode_melody(jingle_bells), 480))
melody_sequence.pause()


def single_click_handler() -> None:
    if melody_sequence.paused:
        melody_sequence.resume()
    else:
        melody_sequence.pause()


def multi_click_handler() -> None:
    melody_sequence.reset()


input_pin = inputpin.InputPin(config.BUTTON_PIN)
button = Button(input_pin, click=single_click_handler, multi_click=multi_click_handler)

# Run the loop for 10 seconds
log.info("Press the button to pause/unpause the sound.")
log.info("Multi-press the button to reset the melody.")
finish = time.monotonic() + 10

while time.monotonic() < finish:
    button.update()
    melody_sequence.update()

pin.off()

memory.report_memory_usage_and_free()
