def execute():
    import cptkip.config.configuration as config
    from cptkip.device.audio import PwmAudio as Audio, Queue
    import validate.utils as utils

    audio = Audio(config.BUZZER_PIN if config.BUZZER_PIN else "none")
    queue = Queue(audio)
    queue.queue("validate/lion.mp3")
    queue.queue("validate/lion.mp3")

    def task():
        queue.update()

    print("Lion roar will play through buzzer")
    utils.execute(task)

    audio.deinit()


if __name__ == '__main__':
    execute()
