def execute():
    import cptkip.config.configuration as config
    import cptkip.pin.buzzer_pin as buzzer_pin
    import validate.utils as utils
    from cptkip.device.buzzer import Buzzer

    with Buzzer(buzzer_pin.BuzzerPin(config.BUZZER_PIN)) as buzzer:
        buzzer.volume = 0.5
        frequency = 500
        buzzer.play(frequency, 0.25)

        def task():
            nonlocal frequency
            buzzer.update()
            if buzzer.playing:
                return

            frequency += 100
            buzzer.play(frequency, 0.25)

        print("Buzzer will change frequency")
        utils.execute(task)


if __name__ == '__main__':
    execute()
