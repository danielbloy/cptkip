def execute():
    from time import monotonic
    import cptkip.config.configuration as config
    import cptkip.device.melody as melody
    import cptkip.pin.buzzer_pin as buzzer_pin
    import validate.utils as utils

    utils.require_pins(config.BUZZER_PIN)

    # Plays a short scale, pausing, resuming and resetting it part way through. On a
    # device listen for: the scale, a pause, the scale continuing, then restarting.
    with buzzer_pin.BuzzerPin(config.BUZZER_PIN) as pin:
        pin.volume = 0.1
        song = melody.decode_melody(["C4:1", "D:1", "E:1", "F:1", "G:1", "A:1", "B:1", "C5:1"])
        with melody.Melody(pin, song, tempo=240) as tune:
            start = monotonic()
            actions = [(1.0, "pause"), (1.5, "resume"), (2.5, "reset")]
            done = []

            def task():
                elapsed = monotonic() - start
                for at, action in actions:
                    if elapsed >= at and action not in done:
                        print(f"Melody {action}")
                        getattr(tune, action)()
                        done.append(action)
                tune.update()

            print("Buzzer will play a scale, pause, resume and then restart it")
            utils.execute(task)

            assert done == ["pause", "resume", "reset"]
            assert tune.playing


if __name__ == '__main__':
    execute()
