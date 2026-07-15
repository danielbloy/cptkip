def execute():
    import cptkip.config.configuration as config
    import cptkip.device.pwm_audio as pwm_audio
    import validate.utils as utils

    audio = pwm_audio.Audio(config.BUZZER_PIN if config.BUZZER_PIN else "none")
    queue = pwm_audio.Queue(audio)
    queue.queue("validate/lion.mp3")
    queue.queue("validate/lion.mp3")

    def task():
        queue.update()

    print("Lion roar will play through buzzer")
    utils.execute(task)

    audio.deinit()


if __name__ == '__main__':
    execute()
