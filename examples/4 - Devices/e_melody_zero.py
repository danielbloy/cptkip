#
# This example uses Melody to play some tunes through the Buzzer.
# A Button is used to play, pause and unpause the melody. Uses
# `cptkip.zero.button`, `cptkip.zero.buzzer` and `cptkip.zero.run`.
#
# noinspection unused-imports
import time  # BUG: This prevents a crash when executed via Thonny

import cptkip.core.logging as log
import cptkip.device.melody as melody
from cptkip.zero.button import create_button
from cptkip.zero.buzzer import create_buzzer_pin
from cptkip.zero.run import update_for

log.set_log_level(log.INFO)

with create_buzzer_pin() as pin:
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

    with melody.MelodySequence(
            melody.Melody(pin, melody.decode_melody(scale.split()), 240),
            melody.Melody(pin, melody.decode_melody(jingle_bells), 480)) as melody_sequence:

        def single_click_handler() -> None:
            if melody_sequence.paused:
                melody_sequence.resume()
            else:
                melody_sequence.pause()


        def multi_click_handler() -> None:
            melody_sequence.reset()


        with create_button(click=single_click_handler, multi_click=multi_click_handler) as button:

            log.info("Press the button to pause/unpause the sound.")
            log.info("Multi-press the button to reset the melody.")

            update_for(5, button, melody_sequence)
