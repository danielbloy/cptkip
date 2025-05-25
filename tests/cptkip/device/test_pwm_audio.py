import pytest

from cptkip.device.pwm_audio import Audio, Queue


class TestAudio:

    def test_creating_with_none_audio_errors(self) -> None:
        """
        Validates an Audio cannot be constructed with a None value.
        """
        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Audio(None)

    def test_play_validates_name(self) -> None:
        """Validates a name cannot be none or an empty string."""
        audio = Audio(1)

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            audio.play(None)

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            audio.play("")

    def test_play_can_be_called(self) -> None:
        """Validate that play() can be called safely."""
        audio = Audio(1)
        audio.play("my-file.mp3")
        audio.play("another-file.mp3")

    def test_deinit_can_be_called(self) -> None:
        """Validate that deinit() can be called safely."""
        audio = Audio(1)
        audio.deinit()
        audio.deinit()

    def test_playing_can_be_called(self) -> None:
        """Validate that playing() can be called safely."""
        audio = Audio(1)
        assert not audio.playing
        assert not audio.playing

    def test_paused_can_be_called(self) -> None:
        """Validate that paused() can be called safely."""
        audio = Audio(1)
        assert not audio.paused
        assert not audio.paused

    def test_pause_can_be_called(self) -> None:
        """Validate that pause() can be called safely."""
        audio = Audio(1)
        audio.pause()
        audio.pause()

    def test_resume_can_be_called(self) -> None:
        """Validate that resume() can be called safely."""
        audio = Audio(1)
        audio.resume()
        audio.resume()

    def test_stop_can_be_called(self) -> None:
        """Validate that stop() can be called safely."""
        audio = Audio(1)
        audio.stop()
        audio.stop()


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


class TestQueue:

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

        assert not queue.pause()
        assert audio.pause_called
        audio.pause_called = False

        assert not queue.resume()
        assert audio.resume_called
        audio.resume_called = False

        assert not queue.stop()
        assert audio.stop_called
        audio.stop_called = False

        # Validate cancel stops anything playing and emptys the queue
        assert not queue.cancel()
        assert audio.stop_called
        audio.stop_called = False

        queue.update()
        assert len(audio.files) == 0
        assert audio.playing_count <= 0
