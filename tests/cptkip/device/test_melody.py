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


def equals(actual: float, expected: float) -> bool:
    """Compares if the two floats are equal within tolerable bounds."""
    diff = actual - expected
    return -0.1 <= diff <= 0.1


class TestNoteToFrequency:
    # This uses the following table as the test reference:
    # https://mixbutton.com/music-tools/frequency-and-pitch/music-note-to-frequency-chart

    def test_pause(self) -> None:
        assert equals(note_to_frequency("R", 0), 0.0)
        assert equals(note_to_frequency("r", 0), 0.0)
        assert equals(note_to_frequency("P", 0), 0.0)
        assert equals(note_to_frequency("p", 0), 0.0)

        assert equals(note_to_frequency("R", 1), 0.0)
        assert equals(note_to_frequency("r", 2), 0.0)
        assert equals(note_to_frequency("P", 3), 0.0)
        assert equals(note_to_frequency("p", 4), 0.0)

        assert equals(note_to_frequency("R", 5), 0.0)
        assert equals(note_to_frequency("r", 6), 0.0)
        assert equals(note_to_frequency("P", 7), 0.0)
        assert equals(note_to_frequency("p", 8), 0.0)

    def test_case_sensitivity(self) -> None:
        assert equals(note_to_frequency("C", 0), 16.35)
        assert equals(note_to_frequency("C", 1), 32.70)
        assert equals(note_to_frequency("C", 2), 65.41)
        assert equals(note_to_frequency("C", 3), 130.81)
        assert equals(note_to_frequency("C", 4), 261.63)
        assert equals(note_to_frequency("C", 5), 523.25)
        assert equals(note_to_frequency("C", 6), 1046.50)
        assert equals(note_to_frequency("C", 7), 2093.00)
        assert equals(note_to_frequency("C", 8), 4186.01)

        assert equals(note_to_frequency("c", 0), 16.35)
        assert equals(note_to_frequency("c", 1), 32.70)
        assert equals(note_to_frequency("c", 2), 65.41)
        assert equals(note_to_frequency("c", 3), 130.81)
        assert equals(note_to_frequency("c", 4), 261.63)
        assert equals(note_to_frequency("c", 5), 523.25)
        assert equals(note_to_frequency("c", 6), 1046.50)
        assert equals(note_to_frequency("c", 7), 2093.00)
        assert equals(note_to_frequency("c", 8), 4186.01)

    def test_sharps_and_flats(self) -> None:
        assert equals(note_to_frequency("CS", 0), 17.32)
        assert equals(note_to_frequency("cs", 0), 17.32)
        assert equals(note_to_frequency("Cs", 0), 17.32)
        assert equals(note_to_frequency("cS", 0), 17.32)
        assert equals(note_to_frequency("C#", 0), 17.32)
        assert equals(note_to_frequency("c#", 0), 17.32)

        assert equals(note_to_frequency("DF", 0), 17.32)
        assert equals(note_to_frequency("df", 0), 17.32)
        assert equals(note_to_frequency("Df", 0), 17.32)
        assert equals(note_to_frequency("dF", 0), 17.32)
        assert equals(note_to_frequency("Db", 0), 17.32)
        assert equals(note_to_frequency("db", 0), 17.32)

    def test_octave_0(self) -> None:
        assert equals(note_to_frequency("C", 0), 16.35)
        assert equals(note_to_frequency("C#", 0), 17.32)
        assert equals(note_to_frequency("Db", 0), 17.32)
        assert equals(note_to_frequency("D", 0), 18.35)
        assert equals(note_to_frequency("D#", 0), 19.45)
        assert equals(note_to_frequency("Eb", 0), 19.45)
        assert equals(note_to_frequency("E", 0), 20.60)
        assert equals(note_to_frequency("F", 0), 21.83)
        assert equals(note_to_frequency("F#", 0), 23.12)
        assert equals(note_to_frequency("Gb", 0), 23.12)
        assert equals(note_to_frequency("G", 0), 24.50)
        assert equals(note_to_frequency("G#", 0), 25.96)
        assert equals(note_to_frequency("Ab", 0), 25.96)
        assert equals(note_to_frequency("A", 0), 27.50)
        assert equals(note_to_frequency("A#", 0), 29.14)
        assert equals(note_to_frequency("Bb", 0), 29.14)
        assert equals(note_to_frequency("B", 0), 30.87)

    def test_octave_1(self) -> None:
        assert equals(note_to_frequency("C", 1), 32.70)
        assert equals(note_to_frequency("C#", 1), 34.65)
        assert equals(note_to_frequency("Db", 1), 34.65)
        assert equals(note_to_frequency("D", 1), 36.71)
        assert equals(note_to_frequency("D#", 1), 38.89)
        assert equals(note_to_frequency("Eb", 1), 38.89)
        assert equals(note_to_frequency("E", 1), 41.20)
        assert equals(note_to_frequency("F", 1), 43.65)
        assert equals(note_to_frequency("F#", 1), 46.25)
        assert equals(note_to_frequency("Gb", 1), 46.25)
        assert equals(note_to_frequency("G", 1), 49.00)
        assert equals(note_to_frequency("G#", 1), 51.91)
        assert equals(note_to_frequency("Ab", 1), 51.91)
        assert equals(note_to_frequency("A", 1), 55.00)
        assert equals(note_to_frequency("A#", 1), 58.27)
        assert equals(note_to_frequency("Bb", 1), 58.27)
        assert equals(note_to_frequency("B", 1), 61.74)

    def test_octave_2(self) -> None:
        assert equals(note_to_frequency("C", 2), 65.41)
        assert equals(note_to_frequency("C#", 2), 69.30)
        assert equals(note_to_frequency("Db", 2), 69.30)
        assert equals(note_to_frequency("D", 2), 73.42)
        assert equals(note_to_frequency("D#", 2), 77.78)
        assert equals(note_to_frequency("Eb", 2), 77.78)
        assert equals(note_to_frequency("E", 2), 82.41)
        assert equals(note_to_frequency("F", 2), 87.31)
        assert equals(note_to_frequency("F#", 2), 92.50)
        assert equals(note_to_frequency("Gb", 2), 92.50)
        assert equals(note_to_frequency("G", 2), 98.00)
        assert equals(note_to_frequency("G#", 2), 103.83)
        assert equals(note_to_frequency("Ab", 2), 103.83)
        assert equals(note_to_frequency("A", 2), 110.00)
        assert equals(note_to_frequency("A#", 2), 116.54)
        assert equals(note_to_frequency("Bb", 2), 116.54)
        assert equals(note_to_frequency("B", 2), 123.47)

    def test_octave_3(self) -> None:
        assert equals(note_to_frequency("C", 3), 130.81)
        assert equals(note_to_frequency("C#", 3), 138.59)
        assert equals(note_to_frequency("Db", 3), 138.59)
        assert equals(note_to_frequency("D", 3), 146.83)
        assert equals(note_to_frequency("D#", 3), 155.56)
        assert equals(note_to_frequency("Eb", 3), 155.56)
        assert equals(note_to_frequency("E", 3), 164.81)
        assert equals(note_to_frequency("F", 3), 174.61)
        assert equals(note_to_frequency("F#", 3), 185.00)
        assert equals(note_to_frequency("Gb", 3), 185.00)
        assert equals(note_to_frequency("G", 3), 196.00)
        assert equals(note_to_frequency("G#", 3), 207.65)
        assert equals(note_to_frequency("Ab", 3), 207.65)
        assert equals(note_to_frequency("A", 3), 220)
        assert equals(note_to_frequency("A#", 3), 233.08)
        assert equals(note_to_frequency("Bb", 3), 233.08)
        assert equals(note_to_frequency("B", 3), 246.94)

    def test_octave_4(self) -> None:
        assert equals(note_to_frequency("C", 4), 261.63)
        assert equals(note_to_frequency("C#", 4), 277.18)
        assert equals(note_to_frequency("Db", 4), 277.18)
        assert equals(note_to_frequency("D", 4), 293.66)
        assert equals(note_to_frequency("D#", 4), 311.13)
        assert equals(note_to_frequency("Eb", 4), 311.13)
        assert equals(note_to_frequency("E", 4), 329.63)
        assert equals(note_to_frequency("F", 4), 349.23)
        assert equals(note_to_frequency("F#", 4), 369.99)
        assert equals(note_to_frequency("Gb", 4), 369.99)
        assert equals(note_to_frequency("G", 4), 392.00)
        assert equals(note_to_frequency("G#", 4), 415.30)
        assert equals(note_to_frequency("Ab", 4), 415.30)
        assert equals(note_to_frequency("A", 4), 440.00)
        assert equals(note_to_frequency("A#", 4), 466.16)
        assert equals(note_to_frequency("Bb", 4), 466.16)
        assert equals(note_to_frequency("B", 4), 493.88)

    def test_octave_5(self) -> None:
        assert equals(note_to_frequency("C", 5), 523.25)
        assert equals(note_to_frequency("C#", 5), 554.37)
        assert equals(note_to_frequency("Db", 5), 554.37)
        assert equals(note_to_frequency("D", 5), 587.33)
        assert equals(note_to_frequency("D#", 5), 622.25)
        assert equals(note_to_frequency("Eb", 5), 622.25)
        assert equals(note_to_frequency("E", 5), 659.25)
        assert equals(note_to_frequency("F", 5), 698.46)
        assert equals(note_to_frequency("F#", 5), 739.99)
        assert equals(note_to_frequency("Gb", 5), 739.99)
        assert equals(note_to_frequency("G", 5), 783.99)
        assert equals(note_to_frequency("G#", 5), 830.61)
        assert equals(note_to_frequency("Ab", 5), 830.61)
        assert equals(note_to_frequency("A", 5), 880.00)
        assert equals(note_to_frequency("A#", 5), 932.33)
        assert equals(note_to_frequency("Bb", 5), 932.33)
        assert equals(note_to_frequency("B", 5), 987.77)

    def test_octave_6(self) -> None:
        assert equals(note_to_frequency("C", 6), 1046.50)
        assert equals(note_to_frequency("C#", 6), 1108.73)
        assert equals(note_to_frequency("Db", 6), 1108.73)
        assert equals(note_to_frequency("D", 6), 1174.66)
        assert equals(note_to_frequency("D#", 6), 1244.51)
        assert equals(note_to_frequency("Eb", 6), 1244.515)
        assert equals(note_to_frequency("E", 6), 1318.51)
        assert equals(note_to_frequency("F", 6), 1396.91)
        assert equals(note_to_frequency("F#", 6), 1479.98)
        assert equals(note_to_frequency("Gb", 6), 1479.98)
        assert equals(note_to_frequency("G", 6), 1567.98)
        assert equals(note_to_frequency("G#", 6), 1661.22)
        assert equals(note_to_frequency("Ab", 6), 1661.22)
        assert equals(note_to_frequency("A", 6), 1760.00)
        assert equals(note_to_frequency("A#", 6), 1864.66)
        assert equals(note_to_frequency("Bb", 6), 1864.66)
        assert equals(note_to_frequency("B", 6), 1975.53)

    def test_octave_7(self) -> None:
        assert equals(note_to_frequency("C", 7), 2093.00)
        assert equals(note_to_frequency("C#", 7), 2217.46)
        assert equals(note_to_frequency("Db", 7), 2217.46)
        assert equals(note_to_frequency("D", 7), 2349.32)
        assert equals(note_to_frequency("D#", 7), 2489.02)
        assert equals(note_to_frequency("Eb", 7), 2489.02)
        assert equals(note_to_frequency("E", 7), 2637.02)
        assert equals(note_to_frequency("F", 7), 2793.83)
        assert equals(note_to_frequency("F#", 7), 2959.96)
        assert equals(note_to_frequency("Gb", 7), 2959.96)
        assert equals(note_to_frequency("G", 7), 3135.96)
        assert equals(note_to_frequency("G#", 7), 3322.44)
        assert equals(note_to_frequency("Ab", 7), 3322.44)
        assert equals(note_to_frequency("A", 7), 3520.00)
        assert equals(note_to_frequency("A#", 7), 3729.31)
        assert equals(note_to_frequency("Bb", 7), 3729.31)
        assert equals(note_to_frequency("B", 7), 3951.07)

    def test_octave_8(self) -> None:
        assert equals(note_to_frequency("C", 8), 4186.01)
        assert equals(note_to_frequency("C#", 8), 4434.92)
        assert equals(note_to_frequency("Db", 8), 4434.92)
        assert equals(note_to_frequency("D", 8), 4698.63)
        assert equals(note_to_frequency("D#", 8), 4978.03)
        assert equals(note_to_frequency("Eb", 8), 4978.03)
        assert equals(note_to_frequency("E", 8), 5274.04)
        assert equals(note_to_frequency("F", 8), 5587.65)
        assert equals(note_to_frequency("F#", 8), 5919.91)
        assert equals(note_to_frequency("Gb", 8), 5919.91)
        assert equals(note_to_frequency("G", 8), 6271.93)
        assert equals(note_to_frequency("G#", 8), 6644.88)
        assert equals(note_to_frequency("Ab", 8), 6644.88)
        assert equals(note_to_frequency("A", 8), 7040.00)
        assert equals(note_to_frequency("A#", 8), 7458.62)
        assert equals(note_to_frequency("Bb", 8), 7458.62)
        assert equals(note_to_frequency("B", 8), 7902.13)
