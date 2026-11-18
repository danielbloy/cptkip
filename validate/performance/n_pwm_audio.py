import cptkip.config.configuration as config
from cptkip.device.audio import PwmAudio as Audio, Queue
from validate.performance.task_runner import execute

AUDIO_FILE = "validate/lion.mp3"

try:
    audio = Audio(config.BUZZER_PIN)
    queue = Queue(audio)


    def task():
        queue.update()


    queue.queue(AUDIO_FILE)
    execute(task, False)
    queue.cancel()

    queue.queue(AUDIO_FILE)
    execute(task, True)
    queue.cancel()

    audio.deinit()

except ValueError as e:
    # ESP-32 S3 and ESP-32 C3 boards do not support audioio nor audiopwmio on
    # CircuitPython versions earlier tha 11.0.0.
    print(e)

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
