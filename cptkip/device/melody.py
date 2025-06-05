import time

import cptkip.core.control as control
from cptkip.pin.buzzer_pin import BuzzerPin


# TODO: Comment this class
class Melody:
    def __init__(self, buzzer: BuzzerPin, song: list[tuple[int, int]], speed, loop=True, paused=False, name=None):

        self._buzzer = buzzer
        self._song = song
        self._index = 0  # The next note to play.
        self._loop = loop
        self._paused = paused
        self._speed_ns = 0
        self._next_update = time.monotonic_ns()
        self._time_left_at_pause = 0
        self.speed = speed  # sets _speed_ns
        self.name = name

    def play(self) -> bool:
        if self.paused:
            return False

        now = time.monotonic_ns()
        if now < self._next_update:
            return False

        frequency, duration = self._song[self._index]
        self._index += 1
        if self._index >= len(self._song):
            self._index = 0
            if not self._loop:
                self.pause()

        self._buzzer.off()
        self._buzzer.play(frequency)

        self._next_update = now + (self._speed_ns * duration)
        return True

    @property
    def paused(self) -> bool:
        return self._paused

    def pause(self):
        """
        Stops playing until resumed.
        """
        if self.paused:
            return

        self._paused = True
        self._time_left_at_pause = max(0, time.monotonic_ns() - self._next_update)

        self._buzzer.off()

    def resume(self) -> None:
        """
        Resumes the music if it has been paused.
        """
        if not self.paused:
            return

        self._next_update = time.monotonic_ns() + self._time_left_at_pause
        self._time_left_at_pause = 0
        self._paused = False

        frequency, duration = 0, 0
        if self._index > 0:
            frequency, duration = self._song[self._index]

        self._buzzer.play(frequency)

    @property
    def speed(self) -> float:
        """
        The speed in fractional seconds.
        """
        return self._speed_ns / control.NS_PER_SECOND

    @speed.setter
    def speed(self, seconds) -> None:
        self._speed_ns = int(seconds * control.NS_PER_SECOND)

    def reset(self) -> None:
        """
        Resets the music sequence back to the beginning.
        """
        self._buzzer.off()
        self._index = 0


# TODO: Comment this class
# TODO: Write tests for this class.
class MelodySequence:
    def __init__(self, *members: Melody, loop=True, name=None):
        self._members = members
        self._loop = loop
        self._current = 0
        self._paused = False
        self.name = name
        # Disable auto loop in the individual songs.
        for member in self._members:
            member._loop = False

    def activate(self, index):
        """
        Activates a specific melody.
        """
        self.melody.reset()
        self.melody.resume()
        if isinstance(index, str):
            self._current = [member.name for member in self._members].index(index)
        else:
            self._current = index

        self.melody.reset()
        self.melody.resume()

    def next(self):
        """
        Jump to the next melody.
        """
        current = self._current + 1
        if current >= len(self._members):
            if not self._loop:
                self.pause()

        self.activate(current % len(self._members))

    def previous(self):
        """
        Jump to the previous melody.
        """
        current = self._current - 1
        self.activate(current % len(self._members))

    def play(self):
        """
        Plays the current melody or goes to the next melody.
        """
        if not self.paused and self.melody.paused:
            self.next()

        if not self.paused:
            return self.melody.play()

        return False

    @property
    def melody(self) -> Melody:
        """
        Returns the current melody in the sequence.
        """
        return self._members[self._current]

    @property
    def paused(self):
        return self._paused

    def pause(self):
        """
        Pauses the current melody in the sequence.
        """
        if self.paused:
            return
        self._paused = True
        self.melody.pause()

    def resume(self):
        """
        Resume the current melody in the sequence, and resumes auto advance if enabled.
        """
        if not self.paused:
            return
        self._paused = False
        self.melody.resume()

    def reset(self):
        """
        Resets the current melody to the first song.
        """
        self.activate(0)


def decode_melody(song: list[str]) -> list[tuple[int, int]]:
    """
    Coverts a song of encoded notes into pairs of (tone, duration). The song
    is a list of strings with each string representing a note and it's duration
    separated by a comma. The Note can optionally also specify the Octave. If no
    octave is specified, then the octave will be the last octave set or 4 if it
    is the first note in the melody. The duration is the number of beats the note
    should last for. An example of a simple C scale:

    scale = [
        "C4:1", "D:1", "E:1", "F:1", "G:1", "A:1", "B:1", "C5:1",
        "B4:1", "A:1", "G:1", "F:1", "E:1", "D:1", "C:1"]

    Sharps and Flats can be specified using #, S, F or B respectively. For example:

    song = ["C#3:4", "FS7:2", "Eb3:1", "AF1:1"]

    The encoded note can be one of:
      <note>:<duration>
      <note><octave>:<duration>

    # TODO: Support decoding which is just a string and not just a list.
    """
    if song is None:
        return list()

    if not isinstance(song, list):
        raise ValueError("encoded_song must be of type List")

    current_octave = 4

    result = []
    for encoded_note in song:

        if not encoded_note or len(encoded_note) < 3:
            raise ValueError("encoded_note must be of length 3")

        # -1 means use the same octave as the previous note.
        octave = -1

        parts = encoded_note.split(":")
        # The first character of the first part is the note.
        note = parts[0][0]

        # If the first part has a second character, use it as the octave.
        if len(parts[0]) > 1:
            octave = int(parts[0][1])

        # The second part is the duration as an integer number.
        duration = int(parts[1])

        if octave < 0:
            octave = current_octave
        else:
            current_octave = octave

        result.append((note_to_frequency(note, octave), duration))

    return result


def standardise_note(note: str) -> str:
    """
    Converts the given note to a standardised code.
    The input note can be uppercase or lowercase.
    Sharps can be signified by #, s or S
    Flats can be signified by f, F, b or B.

    The returned code will be an uppercase letter A to G with optional sharp indicator.
    Sharps are always indicated by #. Any flats are switched to their equivalent sharps.

    Rests can be input as p, P, r or R and are converted to R.
    """
    length = len(note)
    if length == 0 or length > 2:
        raise ValueError("note has invalid length")

    note = note.upper().replace("P", "R")

    if length == 1:
        if note in __note_to_n or note == "R":
            return note

        raise ValueError("note is invalid")

    note = note[0] + note[-1].replace("S", "#").replace("F", "B")

    # Convert flats to sharps.
    if note[-1] == "B":
        if note[0] == "A":
            note = "G#"
        else:
            note = chr(ord(note[0]) - 1) + "#"

    if note in __note_to_n:
        return note

    raise ValueError("note is invalid")


# Maps a standardised note to it's n value representing a semi-tone from C.
__note_to_n = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}


def note_to_frequency(note: str, octave: int) -> int:
    """
    Returns the frequency of the given note in the given octave rounded to the nearest Hertz.

    Formula: Freq = note x 2^(N/12), from https://techlib.com/reference/musical_note_frequencies.htm

    Where:
     * N is the number of notes away from the starting note. N may be positive, negative or zero.
    """

    note = standardise_note(note)
    if note == "R":
        return 0

    n = __note_to_n[note]

    # Using A4 (note number 9, octave 4) as a reference as it is roughly in the middle
    N = ((octave - 4) * 12) + (n - 9)
    frequency = 440 * pow(2, (N / 12))
    return round(frequency)
