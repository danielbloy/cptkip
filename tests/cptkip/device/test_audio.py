import pytest

from cptkip.device.audio import Queue, Audio, PwmAudio, I2sAudio


class TestAudio:
    def test_play_validates_name(self) -> None:
        """Validates a name cannot be none or an empty string."""
        audio = Audio(None)

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            audio.play(None)

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            audio.play("")

    def test_play_can_be_called(self) -> None:
        """Validate that play() can be called safely."""
        audio = Audio(None)
        audio.play("my-file.mp3")
        audio.play("another-file.mp3")

    def test_deinit_can_be_called(self) -> None:
        """Validate that deinit() can be called safely."""
        audio = Audio(None)
        audio.deinit()
        audio.deinit()

    def test_with_resources(self):
        """
        Validates that a Audio can be used in a with statement.
        """

        with Audio(None) as audio:
            assert audio.playing == False

    def test_playing_can_be_called(self) -> None:
        """Validate that playing() can be called safely."""
        audio = Audio(None)
        assert not audio.playing
        assert not audio.playing

    def test_paused_can_be_called(self) -> None:
        """Validate that paused() can be called safely."""
        audio = Audio(None)
        assert not audio.paused
        assert not audio.paused

    def test_pause_can_be_called(self) -> None:
        """Validate that pause() can be called safely."""
        audio = Audio(None)
        audio.pause()
        audio.pause()

    def test_resume_can_be_called(self) -> None:
        """Validate that resume() can be called safely."""
        audio = Audio(None)
        audio.resume()
        audio.resume()

    def test_stop_can_be_called(self) -> None:
        """Validate that stop() can be called safely."""
        audio = Audio(None)
        audio.stop()
        audio.stop()


class TestPwmAudio:
    """
    Very simple validation to ensure we get an Audio object that we can
    call methods and set properties on.
    """

    def test_pwm_can_be_called(self) -> None:
        """
        Validate that PwmAudio() can be called safely.
        """
        audio = PwmAudio(1)
        assert isinstance(audio, Audio)
        audio.play("my-file.mp3")
        assert not audio.paused
        audio.play("another-file.mp3")
        assert not audio.paused

    def test_with_resources(self):
        """
        Validates that a PwmAudio can be used in a with statement.
        """

        with PwmAudio(1) as audio:
            assert audio.playing == False


class TestI2sAudio:
    """
    Very simple validation to ensure we get an Audio object that we can
    call methods and set properties on.
    """

    def test_i2s_can_be_called(self) -> None:
        """
        Validate that I2sAudio() can be called safely.
        """
        audio = I2sAudio(1, 2, 3)
        assert isinstance(audio, Audio)
        audio.play("my-file.mp3")
        assert not audio.paused
        audio.play("another-file.mp3")
        assert not audio.paused

    def test_with_resources(self):
        """
        Validates that a I2sAudio can be used in a with statement.
        """

        with I2sAudio(1, 2, 3) as audio:
            assert audio.playing == False


class MockAudio(Audio):
    def __init__(self):
        super().__init__(None)
        self.playing_count = 0
        self.filename = ""
        self.files = []
        self.playing_called = False
        self.paused_called = False
        self.pause_called = False
        self.resume_called = False
        self.stop_called = False
        self.deinit_called = False

    def play(self, filename: str):
        assert self.playing_count <= 0
        self.files.append(filename)
        self.filename = filename
        self.playing_count += 10  # Adding a file to the queue requires 10 calls to playing to compete playing it.

    @property
    def playing(self) -> bool:
        self.playing_called = True
        self.playing_count -= 1
        return self.playing_count > 0

    @playing.setter
    def playing(self, value):
        pass

    @property
    def paused(self) -> bool:
        self.paused_called = True
        return False

    @paused.setter
    def paused(self, value):
        pass

    def pause(self):
        self.pause_called = True

    def resume(self):
        self.resume_called = True

    def stop(self):
        self.stop_called = True

    def deinit(self) -> None:
        self.deinit_called = True


class TestQueue:
    def test_with_resources(self):
        """
        Validates that a Queue can be used in a with statement.
        """
        with Queue(MockAudio()) as queue:
            assert not queue.playing

    def test_creating_with_none_audio_errors(self) -> None:
        """
        Validates that a AudioController cannot be constructed with
        a None value.
        """
        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Queue(None)

    def test_creating_with_string_errors(self) -> None:
        """
        Validates that a AudioController cannot be constructed with
        a value that is not a Audio.
        """
        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Queue("")

    def test_adding_to_the_queue_gets_picked_up(self) -> None:
        """
        Validates the Queue picks up a queued song and plays it.
        """
        audio = MockAudio()
        queue = Queue(audio)

        # queue a single song.
        queue.queue("track-1.mp3")

        for x in range(10):
            queue.update()
        assert audio.filename == "track-1.mp3"
        assert len(audio.files) == 1
        assert audio.playing_count <= 0
        assert audio.playing_called

    def test_adding_multiple_items_to_the_queue_get_picked_up(self) -> None:
        """
        Validates the Queue picks up multiple queued songs and
        plays them in order.
        """
        audio = MockAudio()
        queue = Queue(audio)

        # queue three songs.
        queue.queue("track-1.mp3")
        queue.queue("track-2.mp3")
        queue.queue("track-3.mp3")

        for x in range(30):
            queue.update()
        assert audio.filename == "track-3.mp3"
        assert len(audio.files) == 3
        assert audio.files[0] == "track-1.mp3"
        assert audio.files[1] == "track-2.mp3"
        assert audio.files[2] == "track-3.mp3"
        assert audio.playing_count <= 0
        assert audio.playing_called

    def test_controls_are_called_correctly(self) -> None:
        """
        Validates the Queue correctly passes on controls such
        as pause, resume and stopped to Audio.
        """
        audio = MockAudio()
        queue = Queue(audio)

        # queue three songs.
        queue.queue("track-1.mp3")
        queue.queue("track-2.mp3")
        queue.queue("track-3.mp3")

        assert not queue.playing
        assert audio.playing_called
        audio.playing_called = False

        assert not queue.paused
        assert audio.paused_called
        audio.paused_called = False

        queue.pause()
        assert audio.pause_called
        audio.pause_called = False

        queue.resume()
        assert audio.resume_called
        audio.resume_called = False

        queue.stop()
        assert audio.stop_called
        audio.stop_called = False

        # Validate cancel stops anything playing and emptys the queue
        queue.cancel()
        assert audio.stop_called
        audio.stop_called = False

        queue.update()
        assert len(audio.files) == 0
        assert audio.playing_count <= 0

    def test_deinit(self) -> None:
        """
        Validates the deinit() method correctly clears up.
        """
        audio = MockAudio()
        queue = Queue(audio)

        # queue three songs.
        queue.queue("track-1.mp3")
        queue.queue("track-2.mp3")
        queue.queue("track-3.mp3")

        queue.update()
        assert queue.playing

        queue.deinit()

        assert audio.stop_called
        assert audio.deinit_called
        assert not queue._queue
