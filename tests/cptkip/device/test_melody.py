import pytest

from cptkip.device.melody import note_to_frequency, standardise_note


class TestMelody:

    @pytest.mark.skip(reason="tests not implemented yet")
    def test_write_tests(self) -> None:
        assert False


class TestMelodySequence:

    @pytest.mark.skip(reason="tests not implemented yet")
    def test_write_tests(self) -> None:
        assert False


class TestParseEncodedNote:

    @pytest.mark.skip(reason="tests not implemented yet")
    def test_write_tests(self) -> None:
        assert False


class TestEncodedMelodyToTriplets:

    @pytest.mark.skip(reason="tests not implemented yet")
    def test_write_tests(self) -> None:
        assert False


class TestTripletsToTonesAndDurations:

    @pytest.mark.skip(reason="tests not implemented yet")
    def test_write_tests(self) -> None:
        assert False


class TestDecodeMelody:

    @pytest.mark.skip(reason="tests not implemented yet")
    def test_write_tests(self) -> None:
        assert False


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

    def test_pause(self) -> None:
        assert note_to_frequency("R", 0) == 0.0
        assert note_to_frequency("r", 0) == 0.0
        assert note_to_frequency("P", 0) == 0.0
        assert note_to_frequency("p", 0) == 0.0

        assert note_to_frequency("R", 1) == 0.0
        assert note_to_frequency("r", 2) == 0.0
        assert note_to_frequency("P", 3) == 0.0
        assert note_to_frequency("p", 4) == 0.0

        assert note_to_frequency("R", 5) == 0.0
        assert note_to_frequency("r", 6) == 0.0
        assert note_to_frequency("P", 7) == 0.0
        assert note_to_frequency("p", 8) == 0.0

    def test_case_sensitivity(self) -> None:
        assert note_to_frequency("C", 0) == 16.35
        assert note_to_frequency("C", 1) == 32.70
        assert note_to_frequency("C", 2) == 65.41
        assert note_to_frequency("C", 3) == 130.81
        assert note_to_frequency("C", 4) == 261.63
        assert note_to_frequency("C", 5) == 523.25
        assert note_to_frequency("C", 6) == 1046.50
        assert note_to_frequency("C", 7) == 2093.00
        assert note_to_frequency("C", 8) == 4186.01

        assert note_to_frequency("c", 0) == 16.35
        assert note_to_frequency("c", 1) == 32.70
        assert note_to_frequency("c", 2) == 65.41
        assert note_to_frequency("c", 3) == 130.81
        assert note_to_frequency("c", 4) == 261.63
        assert note_to_frequency("c", 5) == 523.25
        assert note_to_frequency("c", 6) == 1046.50
        assert note_to_frequency("c", 7) == 2093.00
        assert note_to_frequency("c", 8) == 4186.01

    def test_sharps_and_flats(self) -> None:
        assert note_to_frequency("CS", 0) == 17.32
        assert note_to_frequency("cs", 0) == 17.32
        assert note_to_frequency("Cs", 0) == 17.32
        assert note_to_frequency("cS", 0) == 17.32
        assert note_to_frequency("C#", 0) == 17.32
        assert note_to_frequency("c#", 0) == 17.32

        assert note_to_frequency("DF", 0) == 17.32
        assert note_to_frequency("df", 0) == 17.32
        assert note_to_frequency("Df", 0) == 17.32
        assert note_to_frequency("dF", 0) == 17.32
        assert note_to_frequency("Db", 0) == 17.32
        assert note_to_frequency("db", 0) == 17.32

    def test_octave_0(self) -> None:
        assert note_to_frequency("C", 0) == 16.35
        assert note_to_frequency("C#", 0) == 17.32
        assert note_to_frequency("Db", 0) == 17.32
        assert note_to_frequency("D", 0) == 18.35
        assert note_to_frequency("D#", 0) == 19.45
        assert note_to_frequency("Eb", 0) == 19.45
        assert note_to_frequency("E", 0) == 20.60
        assert note_to_frequency("F", 0) == 21.83
        assert note_to_frequency("F#", 0) == 23.12
        assert note_to_frequency("Gb", 0) == 23.12
        assert note_to_frequency("G", 0) == 24.50
        assert note_to_frequency("G#", 0) == 25.96
        assert note_to_frequency("Ab", 0) == 25.96
        assert note_to_frequency("A", 0) == 27.50
        assert note_to_frequency("A#", 0) == 29.14
        assert note_to_frequency("Bb", 0) == 29.14
        assert note_to_frequency("B", 0) == 30.87

    def test_octave_1(self) -> None:
        assert note_to_frequency("C", 1) == 32.70
        assert note_to_frequency("C#", 1) == 34.65
        assert note_to_frequency("Db", 1) == 34.65
        assert note_to_frequency("D", 1) == 36.71
        assert note_to_frequency("D#", 1) == 38.89
        assert note_to_frequency("Eb", 1) == 38.89
        assert note_to_frequency("E", 1) == 41.20
        assert note_to_frequency("F", 1) == 43.65
        assert note_to_frequency("F#", 1) == 46.25
        assert note_to_frequency("Gb", 1) == 46.25
        assert note_to_frequency("G", 1) == 49.00
        assert note_to_frequency("G#", 1) == 51.91
        assert note_to_frequency("Ab", 1) == 51.91
        assert note_to_frequency("A", 1) == 55.00
        assert note_to_frequency("A#", 1) == 58.27
        assert note_to_frequency("Bb", 1) == 58.27
        assert note_to_frequency("B", 1) == 61.74

    def test_octave_2(self) -> None:
        assert note_to_frequency("C", 2) == 65.41
        assert note_to_frequency("C#", 2) == 69.30
        assert note_to_frequency("Db", 2) == 69.30
        assert note_to_frequency("D", 2) == 73.42
        assert note_to_frequency("D#", 2) == 77.78
        assert note_to_frequency("Eb", 2) == 77.78
        assert note_to_frequency("E", 2) == 82.41
        assert note_to_frequency("F", 2) == 87.31
        assert note_to_frequency("F#", 2) == 92.50
        assert note_to_frequency("Gb", 2) == 92.50
        assert note_to_frequency("G", 2) == 98.00
        assert note_to_frequency("G#", 2) == 103.83
        assert note_to_frequency("Ab", 2) == 103.83
        assert note_to_frequency("A", 2) == 110.00
        assert note_to_frequency("A#", 2) == 116.54
        assert note_to_frequency("Bb", 2) == 116.54
        assert note_to_frequency("B", 2) == 123.47

    def test_octave_3(self) -> None:
        assert note_to_frequency("C", 3) == 130.81
        assert note_to_frequency("C#", 3) == 138.59
        assert note_to_frequency("Db", 3) == 138.59
        assert note_to_frequency("D", 3) == 146.83
        assert note_to_frequency("D#", 3) == 155.56
        assert note_to_frequency("Eb", 3) == 155.56
        assert note_to_frequency("E", 3) == 164.81
        assert note_to_frequency("F", 3) == 174.61
        assert note_to_frequency("F#", 3) == 185.00
        assert note_to_frequency("Gb", 3) == 185.00
        assert note_to_frequency("G", 3) == 196.00
        assert note_to_frequency("G#", 3) == 207.65
        assert note_to_frequency("Ab", 3) == 207.65
        assert note_to_frequency("A", 3) == 220
        assert note_to_frequency("A#", 3) == 233.08
        assert note_to_frequency("Bb", 3) == 233.08
        assert note_to_frequency("B", 3) == 246.94
