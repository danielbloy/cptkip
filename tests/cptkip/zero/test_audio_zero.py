from cptkip.zero.audio import create_pwm_audio, create_i2s_audio, create_pwm_queue, create_i2s_queue


class TestAudioZero:
    """
    The tests in here are trivial. They are not intended to test the functionality
    of the underlying pins or devices, just that the `cptkip.zero.audui` module
    constructs them correctly.
    """

    def test_create_pwm_audio(self):
        """
        Validates that a pwm audio is created "properly".
        """
        audio = create_pwm_audio()
        assert audio

        audio = create_pwm_audio(pin="pin")
        assert audio

    def test_create_i2s_audio(self):
        """
        Validates that I2S audio is created "properly".
        """
        audio = create_i2s_audio()
        assert audio

        audio = create_i2s_audio(clock="clock", lr="lr", data="data")
        assert audio

    def test_create_pwm_queue(self):
        """
        Validates that a pwm audio queue is created "properly".
        """
        queue = create_pwm_queue()
        assert queue
        assert queue._audio

        queue = create_pwm_queue(pin="pin")
        assert queue
        assert queue._audio

    def test_create_i2s_queue(self):
        """
        Validates that I2S audio queue is created "properly".
        """
        queue = create_i2s_queue()
        assert queue
        assert queue._audio

        queue = create_i2s_queue(clock="clock", lr="lr", data="data")
        assert queue
        assert queue._audio
