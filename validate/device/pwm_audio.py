def execute():
    import cptkip.config.configuration as config
    from cptkip.device.audio import PwmAudio as Audio, Queue
    import validate.utils as utils

    try:
        with Queue(Audio(config.BUZZER_PIN if config.BUZZER_PIN else "none")) as queue:
            queue.queue("validate/lion.mp3")
            queue.queue("validate/lion.mp3")

            def task():
                queue.update()

            print("Lion roar will play through buzzer")
            utils.execute(task)
    except ValueError as e:
        # ESP-32 S3 and ESP-32 C3 boards do not support audioio nor audiopwmio on
        # CircuitPython versions earlier tha 11.0.0.
        print(e)


if __name__ == '__main__':
    execute()
