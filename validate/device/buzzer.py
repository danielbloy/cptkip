def execute():
    import cptkip.config.configuration as config
    import cptkip.pin.buzzer_pin as buzzer_pin
    import validate.utils as utils
    from cptkip.device.buzzer import Buzzer

    pin = buzzer_pin.BuzzerPin(config.BUZZER_PIN)
    buzzer = Buzzer(pin)

    pin.volume = 0.5
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

    buzzer.off()
    pin.deinit()

    del buzzer
    del pin


if __name__ == '__main__':
    execute()
