def execute():
    import cptkip.config.configuration as config
    from cptkip.device.audio import I2sAudio as Audio, Queue
    import validate.utils as utils

    with Queue(Audio(config.I2S_BIT_CLOCK, config.I2S_LEFT_RIGHT_CLOCK, config.I2S_DATA)) as queue:
        queue.queue("validate/lion.mp3")
        queue.queue("validate/lion.mp3")

        def task():
            queue.update()

        print("Lion roar will play through speaker")
        utils.execute(task)


if __name__ == '__main__':
    execute()
