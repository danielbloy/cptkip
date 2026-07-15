def execute():
    import cptkip.config.configuration as config
    import cptkip.device.melody as melody
    import cptkip.pin.buzzer_pin as buzzer_pin
    import validate.utils as utils

    pin = buzzer_pin.BuzzerPin(config.BUZZER_PIN)
    pin.volume = 0.1

    scale = '''C4:1 D:1 E:1 F:1 G:1 A:1 B:1 C5:1
               B4:1 A:1 G:1 F:1 E:1 D:1 C:1'''

    tune = [
        "E:2", "E:2", "E:4", "E:2", "E:2", "E:4",
        "E:2", "G:2", "C:2", "D:2", "E:8", "R:8"]

    melody_sequence = melody.MelodySequence(
        melody.Melody(pin, melody.decode_melody(scale.split()), 120),
        melody.Melody(pin, melody.decode_melody(tune)))

    def task():
        melody_sequence.update()

    print("Buzzer will play a tune")
    utils.execute(task)

    pin.off()
    del pin


if __name__ == '__main__':
    execute()
