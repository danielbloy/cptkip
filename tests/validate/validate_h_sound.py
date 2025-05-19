def execute_melody():
    import time

    import cptkip.config.configuration as config
    import cptkip.pin.buzzerpin as buzzerpin
    import cptkip.sound.melody as melody

    pin = buzzerpin.BuzzerPin(config.BUZZER_PIN)
    pin.volume = 0.1

    scale = [
        "C4:1", "D:1", "E:1", "F:1", "G:1", "A:1", "B:1", "C5:1",
        "B4:1", "A:1", "G:1", "F:1", "E:1", "D:1", "C:1"]

    tune = [
        "E:2", "E:2", "E:4", "E:2", "E:2", "E:4",
        "E:2", "G:2", "C:2", "D:2", "E:8", "R:8"]

    melody_sequence = melody.MelodySequence(
        melody.Melody(pin, melody.decode_melody(scale), 0.05),
        melody.Melody(pin, melody.decode_melody(tune), 0.05))

    finish = time.monotonic() + 3
    while time.monotonic() < finish:
        melody_sequence.play()

    pin.off()
    del pin


def execute():
    execute_melody()


if __name__ == '__main__':
    execute()
