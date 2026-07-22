import cptkip.config.configuration as config
from cptkip.device.melody import Melody, MelodySequence, decode_melody
from cptkip.pin.buzzer_pin import BuzzerPin
from validate.performance.task_runner import execute

pin = BuzzerPin(config.BUZZER_PIN)
pin.volume = 0.1

scale = [
    "C4:1", "D:1", "E:1", "F:1", "G:1", "A:1", "B:1", "C5:1",
    "B4:1", "A:1", "G:1", "F:1", "E:1", "D:1", "C:1"]

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

melody_sequence = MelodySequence(
    Melody(pin, decode_melody(scale), 240),
    Melody(pin, decode_melody(jingle_bells), 480))


def task():
    melody_sequence.update()


execute(task, False)
execute(task, True)
pin.off()

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
