import cptkip.config.configuration as config
from cptkip.device.audio import Audio, PwmAudio, I2sAudio, Queue


def create_pwm_audio() -> Audio:
    """
    Simple utility function to make it easy to create a PwmAudio.
    """
    return PwmAudio(config.BUZZER_PIN)


def create_i2s_audio() -> Audio:
    """
    Simple utility function to make it easy to create a I2sAudio.
    """
    return I2sAudio(config.I2S_BIT_CLOCK, config.I2S_LEFT_RIGHT_CLOCK, config.I2S_DATA)


def create_pwm_queue() -> Queue:
    """
    Returns a Queue that uses a PwmAudio.
    """
    return Queue(create_pwm_audio())


def create_i2s_queue() -> Queue:
    """
    Returns a Queue that uses a I2sAudio.
    """
    return Queue(create_i2s_audio())
