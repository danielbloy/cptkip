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
