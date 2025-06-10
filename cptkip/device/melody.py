import time

import cptkip.core.control as control
from cptkip.pin.buzzer_pin import BuzzerPin


class Melody:
    """
    Melody is used to play a song which is a list of tuples of two integers representing the
    frequency and number of beats of each note in the song. The length of the beats is determined
    by the tempo which defaults to 120 beats per minute.

    By default, a Melody will automatically loop. A melody can also be given an optional name
    which is useful when grouping multiple melodies in a Melody Sequence.
    """

    def __init__(self, buzzer: BuzzerPin, song: list[tuple[int, int]], tempo=120, loop=True, paused=False, name=None):
        """
        Constructs a new Melody. The parameters are self-explanatory. Creating a melody is simple as the
        following two identical examples demonstrate:

        melody = Melody(pin, [(262, 1), (294, 1), (330, 1), (349, 1), (392, 1), (440, 1), (494, 1), (523, 1)])
        while True:
            melody.update()

        Or:

        melody = Melody(pin, decode_melody(["C4:1", "D:1", "E:1", "F:1", "G:1", "A:1", "B:1", "C5:1"]))
        while True:
            melody.update()

        :param buzzer: This must be a buzzer pin.
        :param song:   A list of tuples of two integers representing the frequency and number of beats.
        :param tempo:  The number of beast per minute for the song.
        :param loop:   If true, the song will automatically loop. If not, once finished the song will
                       pause back at the start.
        :param paused: If true, the song will start paused.
        :param name:   An optional name for the Melody; used by MelodySequence.
        """
        if buzzer is None:
            raise ValueError("buzzer cannot be None")

        if not isinstance(buzzer, BuzzerPin):
            raise ValueError("buzzer must be of type BuzzerPin")

        # Plain properties.
        self.loop = loop
        self.name = name
        self._buzzer = buzzer

        # Pause properties
        self._time_left_at_pause = 0  # How much time left until the next update when paused.
        self._paused = paused

        # Tempo properties
        self._beat_duration_ns = 0  # set by tempo.
        self._tempo = tempo
        self.tempo = tempo  # sets _beat_duration_ns

        # Song properties
        self._song = song
        self._song_length = len(song)
        self._index = 0  # The next note to play.
        self._next_update = time.monotonic_ns()  # The next note is due to play now.

    def update(self):
        """
        Call update() repeatedly to keep the melody playing. If paused, calling update() will
        do nothing. If playing and the next note is due, update() will play the note.
        """
        now = time.monotonic_ns()
        if now < self._next_update or self.paused:
            return

        if self._index >= self._song_length:
            self._index = 0
            if not self.loop:
                self.pause()
                return

            if self._song_length <= 0:
                return

        frequency, beats = self._song[self._index]
        self._index += 1

        # This call to off() is required to ensure a brief pause between notes of the same frequency
        self._buzzer.off()
        self._buzzer.play(frequency)

        self._next_update = now + (self._beat_duration_ns * beats)

    @property
    def playing(self) -> bool:
        """
        Returned if the song is playing.
        """
        return not self._paused

    @property
    def paused(self) -> bool:
        """
        Returns if the song is paused.
        """
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
        Resumes the music if it has been paused. Also use resume to restart the melody
        if the song has completed and looping is disabled.
        """
        if not self.paused:
            return

        self._next_update = time.monotonic_ns() + self._time_left_at_pause
        self._time_left_at_pause = 0
        self._paused = False

        # Cope with zero length songs.
        if self._song_length <= 0:
            self._index = 0
            return

        # As index points to the next note to play, we need the previous note.
        index = self._index - 1
        if index < 0:
            index = self._song_length - 1

        frequency, _ = self._song[index]
        self._buzzer.play(frequency)

    @property
    def tempo(self) -> float:
        """
        The tempo in beats per minute.
        """
        return self._tempo

    @tempo.setter
    def tempo(self, tempo) -> None:
        self._tempo = tempo
        self._beat_duration_ns = int(control.NS_PER_SECOND / (tempo / 60))

    def reset(self) -> None:
        """
        Resets the music back to the beginning of the song.
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
            member.loop = False

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

    def update(self):
        """
        Plays the current melody or goes to the next melody.
        """
        if not self.paused and self.melody.paused:
            self.next()

        if not self.paused:
            return self.melody.update()

        return False

    @property
    def melody(self) -> Melody:
        """
        Returns the current melody in the sequence.
        """
        return self._members[self._current]

    @property
    def playing(self):
        return not self._paused

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
    """
    if song is None:
        return list()

    if not isinstance(song, list):
        raise ValueError("encoded_song must be of type List")

    octave = 4

    result = []
    for encoded_note in song:

        if not encoded_note or len(encoded_note) < 3:
            raise ValueError("encoded_note must be of length 3")

        # The encoded note can be one of:
        #   <note>:<duration>
        #   <note><octave>:<duration>
        parts = encoded_note.split(":")
        note = parts[0]
        duration = int(parts[1])

        # The note can optionally contain an octave indicator so look to split that out here.
        for i, char in enumerate(note):
            if char.isdigit():
                octave = int(note[i])
                note = note[:i]
                break

        if duration < 0:
            raise ValueError("duration cannot be negative")

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
