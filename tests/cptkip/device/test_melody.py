import time

import pytest

from cptkip.core.control import NS_PER_SECOND
from cptkip.device.melody import Melody, note_to_frequency, standardise_note, decode_melody, MelodySequence
from cptkip.pin.buzzer_pin import BuzzerPin


class MockBuzzerPin(BuzzerPin):
    def __init__(self):
        self.frequencies = []
        self.play_count = 0
        self.off_count = 0
        super().__init__(None)

    def play(self, frequency: int) -> None:
        self.play_count += 1
        self.frequencies.append(frequency)
        super().play(frequency)

    def off(self) -> None:
        self.off_count += 1


def assert_duration_within_tolerance(actual, expected, percentage=5):
    """
    Ensures that the actual value is within a tolerance of the expected.
    """
    tolerance = expected * percentage / 100
    if tolerance == 0:
        tolerance = 100_000  # Allow a tolerance for zero

    lower = expected - tolerance
    upper = expected + tolerance
    print(actual, expected, percentage, lower, upper)
    assert actual >= lower
    assert actual <= upper


class TestMelody:

    def test_constructor(self) -> None:
        """
        Validates that a Melody is constructed with the correct parameters.
        """
        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Melody(None, [])

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Melody(2, [])

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            Melody("None", [])

        melody = Melody(MockBuzzerPin(), [])
        assert melody.playing
        assert not melody.paused
        assert melody.tempo == 120
        assert melody.loop
        assert melody.name is None

        melody = Melody(MockBuzzerPin(), [], loop=False)
        assert melody.playing
        assert not melody.paused
        assert melody.tempo == 120
        assert not melody.loop
        assert melody.name is None

        melody = Melody(MockBuzzerPin(), [], tempo=60)
        assert melody.playing
        assert not melody.paused
        assert melody.tempo == 60
        assert melody.loop
        assert melody.name is None

        melody = Melody(MockBuzzerPin(), [], paused=True)
        assert not melody.playing
        assert melody.paused
        assert melody.tempo == 120
        assert melody.loop
        assert melody.name is None

        melody = Melody(MockBuzzerPin(), [], name="my-song")
        assert melody.playing
        assert not melody.paused
        assert melody.tempo == 120
        assert melody.loop
        assert melody.name == "my-song"

        melody = Melody(MockBuzzerPin(), [], loop=False, tempo=30, paused=True, name="my-song-name")
        assert not melody.playing
        assert melody.paused
        assert melody.tempo == 30
        assert not melody.loop
        assert melody.name == "my-song-name"

    def test_update_with_non_looping_song(self) -> None:
        """
        Validates the simplest case for update where a single non-looping song
        is created and plays through.
        """
        tempo = 480  # 8 beats per second.
        beats_per_second = tempo / 60
        nanoseconds_per_beat = NS_PER_SECOND / beats_per_second

        # First test this works with an empty song.
        pin = MockBuzzerPin()
        melody = Melody(pin, [], loop=False, tempo=tempo)
        start = time.monotonic_ns()
        while melody.playing:
            melody.update()

        duration = time.monotonic_ns() - start
        expected_duration = nanoseconds_per_beat * 0
        assert_duration_within_tolerance(duration, expected_duration)

        assert pin.frequency == 0
        assert pin.frequencies == []
        assert pin.play_count == 0
        assert pin.off_count == 1

        # Try with a single note
        pin = MockBuzzerPin()
        melody = Melody(pin, [(100, 1)], loop=False, tempo=tempo)
        start = time.monotonic_ns()
        while melody.playing:
            melody.update()

        duration = time.monotonic_ns() - start
        expected_duration = nanoseconds_per_beat * 1
        assert_duration_within_tolerance(duration, expected_duration)

        assert pin.frequency == 100
        assert pin.frequencies == [100]
        assert pin.play_count == 1
        assert pin.off_count == 3

        # Try with two notes
        pin = MockBuzzerPin()
        melody = Melody(pin, [(100, 1), (200, 1)], loop=False, tempo=tempo)
        start = time.monotonic_ns()
        while melody.playing:
            melody.update()

        duration = time.monotonic_ns() - start
        expected_duration = nanoseconds_per_beat * 2
        assert_duration_within_tolerance(duration, expected_duration)

        assert pin.frequency == 200
        assert pin.frequencies == [100, 200]
        assert pin.play_count == 2
        assert pin.off_count == 5

        # Try with three notes
        pin = MockBuzzerPin()
        melody = Melody(pin, [(100, 1), (200, 1), (300, 1)], loop=False, tempo=tempo)
        start = time.monotonic_ns()
        while melody.playing:
            melody.update()

        duration = time.monotonic_ns() - start
        expected_duration = nanoseconds_per_beat * 3
        assert_duration_within_tolerance(duration, expected_duration)

        assert pin.frequency == 300
        assert pin.frequencies == [100, 200, 300]
        assert pin.play_count == 3
        assert pin.off_count == 7

    def test_update_with_looping_song(self) -> None:
        """
        Validates the simplest case for update where a looping song
        is created and plays through.
        """
        tempo = 480  # 8 beats per second.
        beats_per_second = tempo / 60
        nanoseconds_per_beat = NS_PER_SECOND / beats_per_second

        # First test this works with an empty song.
        pin = MockBuzzerPin()
        melody = Melody(pin, [], tempo=tempo)
        start = time.monotonic_ns()
        loop_count = 0
        while melody.playing and loop_count < 10:  # We need a way to exit.
            loop_count += 1
            melody.update()

        assert melody.playing  # Validate that we have exited the above loop forcefully.
        duration = time.monotonic_ns() - start
        expected_duration = nanoseconds_per_beat * 0
        assert_duration_within_tolerance(duration, expected_duration)

        assert pin.frequency == 0
        assert pin.play_count == 0
        assert pin.off_count == 0

        # Try with a single note
        pin = MockBuzzerPin()
        melody = Melody(pin, [(100, 1)], tempo=tempo)
        start = time.monotonic_ns()
        while melody.playing and len(pin.frequencies) < 3:  # Stop as soon as the 3rd note is played
            melody.update()

        duration = time.monotonic_ns() - start
        expected_duration = nanoseconds_per_beat * (3 - 1)  # we stop as soon as the 3rd note is played
        assert_duration_within_tolerance(duration, expected_duration)

        assert pin.frequency == 100
        assert pin.frequencies == [100, 100, 100]
        assert pin.play_count == 3
        assert pin.off_count == 3 * 2

        # Try with two notes
        pin = MockBuzzerPin()
        melody = Melody(pin, [(100, 1), (200, 1)], tempo=tempo)
        start = time.monotonic_ns()
        while melody.playing and len(pin.frequencies) < 6:  # Stop as soon as the 6th note is played
            melody.update()

        duration = time.monotonic_ns() - start
        expected_duration = nanoseconds_per_beat * (6 - 1)  # we stop as soon as the 6th note is played
        assert_duration_within_tolerance(duration, expected_duration)

        assert pin.frequency == 200
        assert pin.frequencies == [100, 200, 100, 200, 100, 200]
        assert pin.play_count == 6
        assert pin.off_count == 6 * 2

        # Try with three notes
        pin = MockBuzzerPin()
        melody = Melody(pin, [(100, 1), (200, 1), (300, 1)], tempo=tempo)
        start = time.monotonic_ns()
        while melody.playing and len(pin.frequencies) < 6:  # Stop as soon as the 6th note is played
            melody.update()

        duration = time.monotonic_ns() - start
        expected_duration = nanoseconds_per_beat * (6 - 1)  # we stop as soon as the 6th note is played
        assert_duration_within_tolerance(duration, expected_duration)

        assert pin.frequency == 300
        assert pin.frequencies == [100, 200, 300, 100, 200, 300]
        assert pin.play_count == 6
        assert pin.off_count == 6 * 2

    def test_pause_and_resume(self) -> None:
        """
        Validates that pausing and resuming a song plays for the correct duration..
        """
        tempo = 480  # 8 beats per second.
        beats_per_second = tempo / 60
        nanoseconds_per_beat = NS_PER_SECOND / beats_per_second

        pin = MockBuzzerPin()
        melody = Melody(pin, [(100, 1), (200, 1), (300, 1), (300, 1)], tempo=tempo)
        start = time.monotonic_ns()
        while melody.playing and len(pin.frequencies) < 2:  # Stop as soon as the 2nd note is played
            melody.update()

        melody.pause()
        melody.update()

        duration = time.monotonic_ns() - start
        expected_duration = nanoseconds_per_beat * (2 - 1)  # we stop as soon as the 2nd note is played
        assert_duration_within_tolerance(duration, expected_duration)
        assert_duration_within_tolerance(melody._time_left_at_pause, nanoseconds_per_beat)

        assert pin.frequencies == [100, 200]

        # Build in a sleep where nothing is playing.
        for i in range(30):
            melody.update()
            time.sleep(0.01)

        assert pin.frequencies == [100, 200]

        expected_finish = time.monotonic_ns() + melody._time_left_at_pause
        melody.resume()
        while melody.playing and len(pin.frequencies) < 3:  # Stop as soon as the 3rd note is played
            melody.update()

        assert_duration_within_tolerance(time.monotonic_ns(), expected_finish)
        assert melody._time_left_at_pause == 0

    def test_reset_during_play(self) -> None:
        """
        Validates that reset restarts the melody to the beginning.
        """
        tempo = 480  # 8 beats per second.
        beats_per_second = tempo / 60
        nanoseconds_per_beat = NS_PER_SECOND / beats_per_second

        pin = MockBuzzerPin()
        melody = Melody(pin, [(100, 1), (200, 1), (300, 1)], tempo=tempo)
        start = time.monotonic_ns()
        while melody.playing and len(pin.frequencies) < 2:  # Stop as soon as the 2nd note is played
            melody.update()

        assert_duration_within_tolerance(melody._next_update, time.monotonic_ns() + nanoseconds_per_beat)
        assert melody._index == 2
        assert pin.frequency == 200
        assert pin.frequencies == [100, 200]

        # Reset and allow to play for a few more notes, we should get
        melody.reset()
        assert_duration_within_tolerance(melody._next_update, time.monotonic_ns() + nanoseconds_per_beat)
        assert melody._index == 0

        while melody.playing and len(pin.frequencies) < 4:  # Stop as soon as the 4th note is played
            melody.update()

        duration = time.monotonic_ns() - start
        expected_duration = nanoseconds_per_beat * (4 - 1)  # we stop as soon as the 4th note is played
        assert_duration_within_tolerance(duration, expected_duration)

        assert pin.frequency == 200
        assert pin.frequencies == [100, 200, 100, 200]
        assert pin.play_count == 4
        assert pin.off_count == (4 * 2) + 1  # Additional off for the reset

    def test_reset_when_paused(self) -> None:
        """
        Validates that reset restarts the melody to the beginning.
        """
        tempo = 480  # 8 beats per second.
        beats_per_second = tempo / 60
        nanoseconds_per_beat = NS_PER_SECOND / beats_per_second

        pin = MockBuzzerPin()
        melody = Melody(pin, [(100, 1), (200, 1), (300, 1)], tempo=480)
        while melody.playing and len(pin.frequencies) < 2:  # Stop as soon as the 2nd note is played
            melody.update()

        assert_duration_within_tolerance(melody._next_update, time.monotonic_ns() + nanoseconds_per_beat)
        assert melody._index == 2
        assert pin.frequencies == [100, 200]

        # Reset and allow to play for a few more notes, we should get
        melody.pause()
        assert melody._index == 2
        assert_duration_within_tolerance(melody._time_left_at_pause, nanoseconds_per_beat)

        melody.reset()
        assert melody._index == 1
        assert melody._time_left_at_pause == 0

        # Resume and ensure the first note is played.
        melody.resume()

        while melody.playing and len(pin.frequencies) < 4:  # Stop as soon as the 4th note is played
            melody.update()

        assert pin.frequencies == [100, 200, 100, 200]

    def test_tempo(self) -> None:
        """
        Validates that changing the tempo plays the song faster.
        """
        tempo = 480  # 8 beats per second.
        beats_per_second = tempo / 60
        nanoseconds_per_beat = NS_PER_SECOND / beats_per_second

        # Play a single note.
        pin = MockBuzzerPin()
        melody = Melody(pin, [(100, 1)], loop=False, tempo=tempo)
        start = time.monotonic_ns()
        while melody.playing:
            melody.update()

        duration = time.monotonic_ns() - start
        assert_duration_within_tolerance(duration, nanoseconds_per_beat)

        assert melody.tempo == tempo

        # Halve the original tempo
        melody.tempo = tempo / 2
        melody.resume()
        start = time.monotonic_ns()
        while melody.playing:
            melody.update()

        duration = time.monotonic_ns() - start
        assert_duration_within_tolerance(duration, nanoseconds_per_beat * 2)
        assert melody.tempo == tempo / 2

        # Play original tempo
        melody.tempo = tempo
        melody.resume()
        start = time.monotonic_ns()
        while melody.playing:
            melody.update()

        duration = time.monotonic_ns() - start
        assert_duration_within_tolerance(duration, nanoseconds_per_beat)
        assert melody.tempo == tempo

    def test_changing_tempo_during_song(self) -> None:
        """Validates that a tempo change durng a song takes effect."""
        tempo = 480  # 8 beats per second.
        beats_per_second = tempo / 60
        nanoseconds_per_beat = NS_PER_SECOND / beats_per_second

        pin = MockBuzzerPin()
        melody = Melody(pin, [(100, 1), (200, 1), (300, 1), (400, 1)], tempo=tempo)
        start = time.monotonic_ns()
        while melody.playing and len(pin.frequencies) < 3:  # Stop as soon as the 3rd note is played
            melody.update()

        duration = time.monotonic_ns() - start
        expected_duration = nanoseconds_per_beat * (3 - 1)  # we stop as soon as the 3rd note is played
        assert_duration_within_tolerance(duration, expected_duration)

        assert pin.frequency == 300
        assert pin.frequencies == [100, 200, 300]

        # Change the tempo which will apply at the start of the 4th note
        melody.tempo = tempo / 2

        while melody.playing and len(pin.frequencies) < 6:  # Stop as soon as the 6th note is played
            melody.update()

        duration = time.monotonic_ns() - start
        expected_duration = (nanoseconds_per_beat * 3) + (
                nanoseconds_per_beat * 4)  # 3 notes at original tempo, 4th and 5th at new (slower) tempo
        assert_duration_within_tolerance(duration, expected_duration)

        assert pin.frequency == 200
        assert pin.frequencies == [100, 200, 300, 400, 100, 200]


class MockMelody(Melody):
    def __init__(self, pin, notes: int, loop=True):
        super().__init__(pin, [(i + 1, 1) for i in range(notes)], loop=loop)
        # Override duration
        self._beat_duration_ns = 0


class TestMelodySequence:

    def test_constructor(self) -> None:
        """
        Validates that a MelodySequence is constructed with the correct parameters.
        """
        with pytest.raises(ValueError):
            MelodySequence()

        with pytest.raises(ValueError):
            MelodySequence(loop=False)

        with pytest.raises(ValueError):
            MelodySequence(None)

        with pytest.raises(AttributeError):
            MelodySequence("string")

        with pytest.raises(AttributeError):
            MelodySequence(0)

        with pytest.raises(AttributeError):
            MelodySequence("string", 0, loop=False)

        empty_melody = Melody(MockBuzzerPin(), [])
        melody_1 = Melody(MockBuzzerPin(), [(100, 1), (200, 1)])
        melody_2 = Melody(MockBuzzerPin(), [(300, 1), (400, 1)])
        melody_3 = Melody(MockBuzzerPin(), [(100, 1), (200, 1), (300, 1), (400, 1)])

        MelodySequence(empty_melody)
        MelodySequence(melody_1)
        MelodySequence(melody_2, melody_3, loop=False)
        MelodySequence(melody_1, empty_melody, melody_2, melody_3, loop=False)

    def test_update_with_non_looping_sequence(self) -> None:
        """
        Validates that non looping MelodySequences iterate through all songs
        once and once only.
        """

        # Test with a single melody that has no notes.
        pin = MockBuzzerPin()
        empty_melody = MockMelody(pin, notes=0)
        sequence = MelodySequence(empty_melody, loop=False)
        while sequence.playing:
            sequence.update()

        assert pin.frequencies == []
        assert pin.play_count == 0

        # Play a single Melody with 5 notes.
        pin = MockBuzzerPin()
        melody = MockMelody(pin, notes=5)
        sequence = MelodySequence(melody, loop=False)
        while sequence.playing:
            sequence.update()

        assert pin.frequencies == [1, 2, 3, 4, 5]

        # Play multiple Melodies with multiple notes.
        pin = MockBuzzerPin()
        empty_melody = MockMelody(pin, notes=0)
        melody_1 = MockMelody(pin, notes=7)
        melody_2 = MockMelody(pin, notes=3)
        melody_3 = MockMelody(pin, notes=4)
        sequence = MelodySequence(melody_1, empty_melody, melody_2, melody_3, loop=False)
        while sequence.playing:
            sequence.update()

        assert pin.frequencies == [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 1, 2, 3, 4]

    def test_update_with_looping_sequence(self) -> None:
        """
        Validates that looping MelodySequences iterate through all songs
        once and then repeat.
        """

        # Test with a single melody that has no notes.
        pin = MockBuzzerPin()
        empty_melody = MockMelody(pin, notes=0)
        sequence = MelodySequence(empty_melody)
        loop_count = 0
        while sequence.playing and loop_count < 10:
            loop_count += 1
            sequence.update()

        assert sequence.playing
        assert pin.frequencies == []
        assert pin.play_count == 0

        # Play a single Melody with 3 notes.
        pin = MockBuzzerPin()
        melody = MockMelody(pin, notes=5)
        sequence = MelodySequence(melody)
        while sequence.playing and pin.play_count < 8:
            sequence.update()

        assert sequence.playing
        assert pin.frequencies == [1, 2, 3, 4, 5, 1, 2, 3]
        assert pin.play_count == 8

        # Play multiple Melodies with multiple notes.
        pin = MockBuzzerPin()
        empty_melody = MockMelody(pin, notes=0)
        melody_1 = MockMelody(pin, notes=7)
        melody_2 = MockMelody(pin, notes=3)
        melody_3 = MockMelody(pin, notes=4)
        sequence = MelodySequence(melody_1, empty_melody, melody_2, melody_3)
        while sequence.playing and pin.play_count < 22:
            sequence.update()

        assert sequence.playing
        assert pin.frequencies == [1, 2, 3, 4, 5, 6, 7, 1, 2, 3, 1, 2, 3, 4, 1, 2, 3, 4, 5, 6, 7, 1]
        assert pin.play_count == 22

    # TODO: Select song to play via active()
    # TODO: Previous and next().


class TestDecodeMelody:

    def test_empty_song(self) -> None:
        """Validates that None and an empty list returns an empty list."""
        # noinspection PyTypeChecker
        assert decode_melody(None) == list()
        assert decode_melody(list()) == list()

    def test_single_note(self) -> None:
        """
        Validates a range of single notes
        """
        assert decode_melody(["P:1"]) == [(0, 1)]
        assert decode_melody(["R1:2"]) == [(0, 2)]
        assert decode_melody(["C0:3"]) == [(16, 3)]
        assert decode_melody(["C#1:3"]) == [(35, 3)]
        assert decode_melody(["DB2:3"]) == [(69, 3)]
        assert decode_melody(["D2:4"]) == [(73, 4)]
        assert decode_melody(["DS2:5"]) == [(78, 5)]
        assert decode_melody(["EF4:3"]) == [(311, 3)]
        assert decode_melody(["E4:3"]) == [(330, 3)]
        assert decode_melody(["F4:3"]) == [(349, 3)]
        assert decode_melody(["G5:3"]) == [(784, 3)]
        assert decode_melody(["G#5:3"]) == [(831, 3)]
        assert decode_melody(["AB5:3"]) == [(831, 3)]
        assert decode_melody(["A6:3"]) == [(1760, 3)]
        assert decode_melody(["AS6:3"]) == [(1865, 3)]
        assert decode_melody(["BF7:3"]) == [(3729, 3)]
        assert decode_melody(["B7:3"]) == [(3951, 3)]
        assert decode_melody(["C8:23"]) == [(4186, 23)]

    def test_single_note_no_octave(self) -> None:
        """Validates the default behaviour if no octave is specified."""
        assert decode_melody(["C:3"]) == [(262, 3)]

    def test_invalid_single_note(self) -> None:
        """
        Validates a range of single notes that do not conform.
        """
        with pytest.raises(ValueError):
            decode_melody([""])

        with pytest.raises(ValueError):
            decode_melody(["C:"])

        with pytest.raises(ValueError):
            decode_melody(["C:-1"])

        with pytest.raises(ValueError):
            decode_melody(["C:A"])

        with pytest.raises(ValueError):
            decode_melody(["CC:1"])

        with pytest.raises(ValueError):
            decode_melody(["4:3"])

        with pytest.raises(ValueError):
            decode_melody(["W4:1"])

        with pytest.raises(ValueError):
            # noinspection PyTypeChecker
            decode_melody("C14:1")

    def test_multiple_notes(self) -> None:
        """Validates when multiple notes are specified."""

        # These will all be Octave 4
        assert decode_melody(["C:1", "D:2", "E:3"]) == [(262, 1), (294, 2), (330, 3)]

        # The first note sets the octave and the others follow
        assert decode_melody(["C0:1", "D:2", "E:3"]) == [(16, 1), (18, 2), (21, 3)]

        # Different octaves
        assert decode_melody(["E4:3", "C0:1", "G5:3"]) == [(330, 3), (16, 1), (784, 3)]

    def test_multiple_notes_some_invalid(self) -> None:
        with pytest.raises(ValueError):
            decode_melody(["W:1", "D:2", "E:3"])

        with pytest.raises(ValueError):
            decode_melody(["C0:1", "D:", "E:3"])

        with pytest.raises(ValueError):
            decode_melody(["E4:3", "C0:1", "GA5:3"])


class TestStandardiseNote:
    def test_error_cases(self) -> None:
        with pytest.raises(ValueError):
            standardise_note("")

        with pytest.raises(ValueError):
            standardise_note("aaa")

        with pytest.raises(ValueError):
            standardise_note("aaaaa")

        with pytest.raises(ValueError):
            standardise_note("N")

        with pytest.raises(ValueError):
            standardise_note("cc")

    def test_pause(self) -> None:
        assert standardise_note("R") == "R"
        assert standardise_note("r") == "R"
        assert standardise_note("P") == "R"
        assert standardise_note("p") == "R"

    def test_case_sensitivity(self) -> None:
        assert standardise_note("C") == "C"
        assert standardise_note("C") == "C"
        assert standardise_note("a") == "A"
        assert standardise_note("B") == "B"
        assert standardise_note("cS") == "C#"
        assert standardise_note("c#") == "C#"
        assert standardise_note("DF") == "C#"
        assert standardise_note("Gf") == "F#"
        assert standardise_note("Bb") == "A#"

    def test_normals(self) -> None:
        assert standardise_note("a") == "A"
        assert standardise_note("b") == "B"
        assert standardise_note("c") == "C"
        assert standardise_note("d") == "D"
        assert standardise_note("e") == "E"
        assert standardise_note("f") == "F"
        assert standardise_note("g") == "G"

    def test_sharps(self) -> None:
        assert standardise_note("aS") == "A#"
        assert standardise_note("cs") == "C#"
        assert standardise_note("ds") == "D#"
        assert standardise_note("fS") == "F#"
        assert standardise_note("gs") == "G#"

        assert standardise_note("a#") == "A#"
        assert standardise_note("c#") == "C#"
        assert standardise_note("d#") == "D#"
        assert standardise_note("f#") == "F#"
        assert standardise_note("g#") == "G#"

    def test_flats(self) -> None:
        assert standardise_note("bf") == "A#"
        assert standardise_note("df") == "C#"
        assert standardise_note("ef") == "D#"
        assert standardise_note("gf") == "F#"
        assert standardise_note("af") == "G#"

        assert standardise_note("bb") == "A#"
        assert standardise_note("db") == "C#"
        assert standardise_note("eb") == "D#"
        assert standardise_note("gb") == "F#"
        assert standardise_note("ab") == "G#"


class TestNoteToFrequency:
    # This uses the following table as the test reference:
    # https://mixbutton.com/music-tools/frequency-and-pitch/music-note-to-frequency-chart

    def test_error_cases(self) -> None:
        with pytest.raises(ValueError):
            note_to_frequency("", 0)

        with pytest.raises(ValueError):
            note_to_frequency("aaa", 1)

        with pytest.raises(ValueError):
            note_to_frequency("aaaaa", 2)

        with pytest.raises(ValueError):
            note_to_frequency("N", 0)

        with pytest.raises(ValueError):
            note_to_frequency("cc", 1)

    def test_pause(self) -> None:
        assert note_to_frequency("R", 0) == 0
        assert note_to_frequency("r", 0) == 0
        assert note_to_frequency("P", 0) == 0
        assert note_to_frequency("p", 0) == 0

        assert note_to_frequency("R", 1) == 0
        assert note_to_frequency("r", 2) == 0
        assert note_to_frequency("P", 3) == 0
        assert note_to_frequency("p", 4) == 0

        assert note_to_frequency("R", 5) == 0
        assert note_to_frequency("r", 6) == 0
        assert note_to_frequency("P", 7) == 0
        assert note_to_frequency("p", 8) == 0

    def test_case_sensitivity(self) -> None:
        assert note_to_frequency("C", 0) == 16
        assert note_to_frequency("C", 1) == 33
        assert note_to_frequency("C", 2) == 65
        assert note_to_frequency("C", 3) == 131
        assert note_to_frequency("C", 4) == 262
        assert note_to_frequency("C", 5) == 523
        assert note_to_frequency("C", 6) == 1047
        assert note_to_frequency("C", 7) == 2093
        assert note_to_frequency("C", 8) == 4186

        assert note_to_frequency("c", 0) == 16
        assert note_to_frequency("c", 1) == 33
        assert note_to_frequency("c", 2) == 65
        assert note_to_frequency("c", 3) == 131
        assert note_to_frequency("c", 4) == 262
        assert note_to_frequency("c", 5) == 523
        assert note_to_frequency("c", 6) == 1047
        assert note_to_frequency("c", 7) == 2093
        assert note_to_frequency("c", 8) == 4186

    def test_sharps_and_flats(self) -> None:
        assert note_to_frequency("CS", 0) == 17
        assert note_to_frequency("cs", 0) == 17
        assert note_to_frequency("Cs", 0) == 17
        assert note_to_frequency("cS", 0) == 17
        assert note_to_frequency("C#", 0) == 17
        assert note_to_frequency("c#", 0) == 17

        assert note_to_frequency("DF", 0) == 17
        assert note_to_frequency("df", 0) == 17
        assert note_to_frequency("Df", 0) == 17
        assert note_to_frequency("dF", 0) == 17
        assert note_to_frequency("Db", 0) == 17
        assert note_to_frequency("db", 0) == 17

    def test_octave_0(self) -> None:
        assert note_to_frequency("C", 0) == 16
        assert note_to_frequency("C#", 0) == 17
        assert note_to_frequency("Db", 0) == 17
        assert note_to_frequency("D", 0) == 18
        assert note_to_frequency("D#", 0) == 19
        assert note_to_frequency("Eb", 0) == 19
        assert note_to_frequency("E", 0) == 21
        assert note_to_frequency("F", 0) == 22
        assert note_to_frequency("F#", 0) == 23
        assert note_to_frequency("Gb", 0) == 23
        assert note_to_frequency("G", 0) == 24
        assert note_to_frequency("G#", 0) == 26
        assert note_to_frequency("Ab", 0) == 26
        assert note_to_frequency("A", 0) == 28
        assert note_to_frequency("A#", 0) == 29
        assert note_to_frequency("Bb", 0) == 29
        assert note_to_frequency("B", 0) == 31

    def test_octave_1(self) -> None:
        assert note_to_frequency("C", 1) == 33
        assert note_to_frequency("C#", 1) == 35
        assert note_to_frequency("Db", 1) == 35
        assert note_to_frequency("D", 1) == 37
        assert note_to_frequency("D#", 1) == 39
        assert note_to_frequency("Eb", 1) == 39
        assert note_to_frequency("E", 1) == 41
        assert note_to_frequency("F", 1) == 44
        assert note_to_frequency("F#", 1) == 46
        assert note_to_frequency("Gb", 1) == 46
        assert note_to_frequency("G", 1) == 49
        assert note_to_frequency("G#", 1) == 52
        assert note_to_frequency("Ab", 1) == 52
        assert note_to_frequency("A", 1) == 55
        assert note_to_frequency("A#", 1) == 58
        assert note_to_frequency("Bb", 1) == 58
        assert note_to_frequency("B", 1) == 62

    def test_octave_2(self) -> None:
        assert note_to_frequency("C", 2) == 65
        assert note_to_frequency("C#", 2) == 69
        assert note_to_frequency("Db", 2) == 69
        assert note_to_frequency("D", 2) == 73
        assert note_to_frequency("D#", 2) == 78
        assert note_to_frequency("Eb", 2) == 78
        assert note_to_frequency("E", 2) == 82
        assert note_to_frequency("F", 2) == 87
        assert note_to_frequency("F#", 2) == 92
        assert note_to_frequency("Gb", 2) == 92
        assert note_to_frequency("G", 2) == 98
        assert note_to_frequency("G#", 2) == 104
        assert note_to_frequency("Ab", 2) == 104
        assert note_to_frequency("A", 2) == 110
        assert note_to_frequency("A#", 2) == 117
        assert note_to_frequency("Bb", 2) == 117
        assert note_to_frequency("B", 2) == 123

    def test_octave_3(self) -> None:
        assert note_to_frequency("C", 3) == 131
        assert note_to_frequency("C#", 3) == 139
        assert note_to_frequency("Db", 3) == 139
        assert note_to_frequency("D", 3) == 147
        assert note_to_frequency("D#", 3) == 156
        assert note_to_frequency("Eb", 3) == 156
        assert note_to_frequency("E", 3) == 165
        assert note_to_frequency("F", 3) == 175
        assert note_to_frequency("F#", 3) == 185
        assert note_to_frequency("Gb", 3) == 185
        assert note_to_frequency("G", 3) == 196
        assert note_to_frequency("G#", 3) == 208
        assert note_to_frequency("Ab", 3) == 208
        assert note_to_frequency("A", 3) == 220
        assert note_to_frequency("A#", 3) == 233
        assert note_to_frequency("Bb", 3) == 233
        assert note_to_frequency("B", 3) == 247

    def test_octave_4(self) -> None:
        assert note_to_frequency("C", 4) == 262
        assert note_to_frequency("C#", 4) == 277
        assert note_to_frequency("Db", 4) == 277
        assert note_to_frequency("D", 4) == 294
        assert note_to_frequency("D#", 4) == 311
        assert note_to_frequency("Eb", 4) == 311
        assert note_to_frequency("E", 4) == 330
        assert note_to_frequency("F", 4) == 349
        assert note_to_frequency("F#", 4) == 370
        assert note_to_frequency("Gb", 4) == 370
        assert note_to_frequency("G", 4) == 392
        assert note_to_frequency("G#", 4) == 415
        assert note_to_frequency("Ab", 4) == 415
        assert note_to_frequency("A", 4) == 440
        assert note_to_frequency("A#", 4) == 466
        assert note_to_frequency("Bb", 4) == 466
        assert note_to_frequency("B", 4) == 494

    def test_octave_5(self) -> None:
        assert note_to_frequency("C", 5) == 523
        assert note_to_frequency("C#", 5) == 554
        assert note_to_frequency("Db", 5) == 554
        assert note_to_frequency("D", 5) == 587
        assert note_to_frequency("D#", 5) == 622
        assert note_to_frequency("Eb", 5) == 622
        assert note_to_frequency("E", 5) == 659
        assert note_to_frequency("F", 5) == 698
        assert note_to_frequency("F#", 5) == 740
        assert note_to_frequency("Gb", 5) == 740
        assert note_to_frequency("G", 5) == 784
        assert note_to_frequency("G#", 5) == 831
        assert note_to_frequency("Ab", 5) == 831
        assert note_to_frequency("A", 5) == 880
        assert note_to_frequency("A#", 5) == 932
        assert note_to_frequency("Bb", 5) == 932
        assert note_to_frequency("B", 5) == 988

    def test_octave_6(self) -> None:
        assert note_to_frequency("C", 6) == 1047
        assert note_to_frequency("C#", 6) == 1109
        assert note_to_frequency("Db", 6) == 1109
        assert note_to_frequency("D", 6) == 1175
        assert note_to_frequency("D#", 6) == 1245
        assert note_to_frequency("Eb", 6) == 1245
        assert note_to_frequency("E", 6) == 1319
        assert note_to_frequency("F", 6) == 1397
        assert note_to_frequency("F#", 6) == 1480
        assert note_to_frequency("Gb", 6) == 1480
        assert note_to_frequency("G", 6) == 1568
        assert note_to_frequency("G#", 6) == 1661
        assert note_to_frequency("Ab", 6) == 1661
        assert note_to_frequency("A", 6) == 1760
        assert note_to_frequency("A#", 6) == 1865
        assert note_to_frequency("Bb", 6) == 1865
        assert note_to_frequency("B", 6) == 1976

    def test_octave_7(self) -> None:
        assert note_to_frequency("C", 7) == 2093
        assert note_to_frequency("C#", 7) == 2217
        assert note_to_frequency("Db", 7) == 2217
        assert note_to_frequency("D", 7) == 2349
        assert note_to_frequency("D#", 7) == 2489
        assert note_to_frequency("Eb", 7) == 2489
        assert note_to_frequency("E", 7) == 2637
        assert note_to_frequency("F", 7) == 2794
        assert note_to_frequency("F#", 7) == 2960
        assert note_to_frequency("Gb", 7) == 2960
        assert note_to_frequency("G", 7) == 3136
        assert note_to_frequency("G#", 7) == 3322
        assert note_to_frequency("Ab", 7) == 3322
        assert note_to_frequency("A", 7) == 3520
        assert note_to_frequency("A#", 7) == 3729
        assert note_to_frequency("Bb", 7) == 3729
        assert note_to_frequency("B", 7) == 3951

    def test_octave_8(self) -> None:
        assert note_to_frequency("C", 8) == 4186
        assert note_to_frequency("C#", 8) == 4435
        assert note_to_frequency("Db", 8) == 4435
        assert note_to_frequency("D", 8) == 4699
        assert note_to_frequency("D#", 8) == 4978
        assert note_to_frequency("Eb", 8) == 4978
        assert note_to_frequency("E", 8) == 5274
        assert note_to_frequency("F", 8) == 5588
        assert note_to_frequency("F#", 8) == 5920
        assert note_to_frequency("Gb", 8) == 5920
        assert note_to_frequency("G", 8) == 6272
        assert note_to_frequency("G#", 8) == 6645
        assert note_to_frequency("Ab", 8) == 6645
        assert note_to_frequency("A", 8) == 7040
        assert note_to_frequency("A#", 8) == 7459
        assert note_to_frequency("Bb", 8) == 7459
        assert note_to_frequency("B", 8) == 7902
