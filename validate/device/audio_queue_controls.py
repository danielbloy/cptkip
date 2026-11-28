def execute():
    from time import monotonic
    import cptkip.config.configuration as config
    from cptkip.device.audio import I2sAudio, Queue
    import validate.utils as utils

    utils.require_pins(config.I2S_BIT_CLOCK, config.I2S_LEFT_RIGHT_CLOCK, config.I2S_DATA)

    # Plays the lion roar, pauses and resumes it, then cancels the rest of the queue.
    with Queue(I2sAudio(config.I2S_BIT_CLOCK, config.I2S_LEFT_RIGHT_CLOCK, config.I2S_DATA)) as queue:
        for _ in range(3):
            queue.queue("validate/lion.mp3")

        start = monotonic()
        actions = [(0.5, "pause"), (1.0, "resume"), (2.0, "cancel")]
        done = []

        def task():
            elapsed = monotonic() - start
            for at, action in actions:
                if elapsed >= at and action not in done:
                    print(f"Queue {action}")
                    getattr(queue, action)()
                    done.append(action)
            if "cancel" not in done:
                queue.update()

        print("Lion roar will play, pause, resume and then stop")
        utils.execute(task)

        assert done == ["pause", "resume", "cancel"]
        assert not queue.playing


if __name__ == '__main__':
    execute()
