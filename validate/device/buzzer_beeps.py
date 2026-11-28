def execute():
    import cptkip.config.configuration as config
    import cptkip.pin.buzzer_pin as buzzer_pin
    import validate.utils as utils
    from cptkip.device.buzzer import Buzzer

    utils.require_pins(config.BUZZER_PIN)

    # Three beeps (0.3s each with a 0.1s gap) then silence.
    with Buzzer(buzzer_pin.BuzzerPin(config.BUZZER_PIN)) as buzzer:
        buzzer.volume = 0.5
        starts = 0
        was_playing = False

        def task():
            nonlocal starts, was_playing
            buzzer.update()
            if buzzer.playing and not was_playing:
                starts += 1
            was_playing = buzzer.playing

        buzzer.beeps(3)
        print("Buzzer will beep 3 times")
        utils.execute(task)

        assert starts == 3, f"expected 3 beeps, counted {starts}"
        assert not buzzer.playing


if __name__ == '__main__':
    execute()
