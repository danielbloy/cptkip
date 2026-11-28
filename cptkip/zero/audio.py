import cptkip.config.configuration as config
from cptkip.device.audio import Audio, PwmAudio, I2sAudio, Queue


def create_pwm_audio(pin=None) -> Audio:
    """
    Simple utility function to make it easy to create a PwmAudio.
    If no pin is specified, it defaults to the config value BUZZER_PIN.
    """
    return PwmAudio(config.BUZZER_PIN if pin is None else pin)


def create_i2s_audio(clock=None, lr=None, data=None) -> Audio:
    """
    Simple utility function to make it easy to create a I2sAudio.
    If no pins are specified, they default to the config values I2S_BIT_CLOCK,
    I2S_LEFT_RIGHT_CLOCK and I2S_DATA.
    """
    return I2sAudio(config.I2S_BIT_CLOCK if clock is None else clock,
                    config.I2S_LEFT_RIGHT_CLOCK if lr is None else lr,
                    config.I2S_DATA if data is None else data)


def create_pwm_queue(pin=None) -> Queue:
    """
    Returns a Queue that uses a PwmAudio.
    If no pin is specified, it defaults to the config value BUZZER_PIN.
    """
    return Queue(create_pwm_audio(pin))


def create_i2s_queue(clock=None, lr=None, data=None) -> Queue:
    """
    Returns a Queue that uses a I2sAudio.
    If no pins are specified, they default to the config values I2S_BIT_CLOCK,
    I2S_LEFT_RIGHT_CLOCK and I2S_DATA.
    """
    return Queue(create_i2s_audio(clock, lr, data))
