import cptkip.config.configuration as config
import cptkip.core.environment as environment
from cptkip.device.audio import PwmAudio, I2sAudio, Queue

# collections.abc is not available in CircuitPython.
if environment.is_running_on_desktop():
    pass


def create_pwm_audio() -> PwmAudio:
    """
    Simple utility function to make it easy to create a PwmAudio.
    """
    return PwmAudio(config.BUZZER_PIN)


def create_i2s_audio() -> I2sAudio:
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
