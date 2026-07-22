import cptkip.config.configuration as config
from cptkip.device.pwm_audio import Audio, Queue
from validate.performance.task_runner import execute

AUDIO_FILE = "examples/lion.mp3"

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

# Load the next file
from validate.performance.script_runner import execute_next_script

execute_next_script(__file__)
