def execute():
    import cptkip.config.configuration as config
    from cptkip.device.audio import PwmAudio as Audio, Queue
    import validate.utils as utils

    utils.require_pins(config.BUZZER_PIN)
    try:
        audio = Audio(config.BUZZER_PIN)
    except ValueError as e:
        # ESP-32 S3 and ESP-32 C3 boards do not support audioio nor audiopwmio on
        # CircuitPython versions earlier than 11.0.0.
        raise utils.Skip(str(e))

    with Queue(audio) as queue:
        queue.queue("validate/lion.mp3")
        queue.queue("validate/lion.mp3")

        def task():
            queue.update()

        print("Lion roar will play through buzzer")
        utils.execute(task)


if __name__ == '__main__':
    execute()
