def execute():
    from time import monotonic
    import validate.utils as utils

    import cptkip.config.configuration as config
    import cptkip.pin.buzzer_pin as buzzer_pin

    with buzzer_pin.BuzzerPin(config.BUZZER_PIN) as pin:

        def task():
            nonlocal next_change
            change = monotonic() >= next_change
            if change:
                print("Change Buzzer pin")
                next_change += 0.25
                if pin.volume > 0.5:
                    pin.volume = 0.25
                else:
                    pin.volume = 0.55

        pin.frequency = 300
        pin.volume = 0.55
        next_change = monotonic() + 0.25
        print("Buzzer will sound")
        utils.execute(task)


if __name__ == '__main__':
    execute()
