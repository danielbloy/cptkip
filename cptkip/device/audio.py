import cptkip.core.environment as environment

MP3Decoder = None
if environment.are_pins_available():
    try:
        # noinspection PyUnresolvedReferences
        from audiomp3 import MP3Decoder
    except ImportError:
        pass


def _placeholder_mp3() -> str:
    """
    Returns the path of the placeholder mp3.mp3 file that ships in the cptkip package
    directory. It is located relative to this module so it is found wherever cptkip is
    installed (drive root, /lib, or a desktop site-packages) rather than relative to the
    current working directory. CircuitPython has no os.path, so this is done by hand and
    copes with both forward and back slash separators.
    """
    path = __file__
    for _ in range(2):  # strip "device/audio.py"
        i = max(path.rfind("/"), path.rfind("\\"))
        path = path[:i] if i >= 0 else ""
    return path + "/mp3.mp3" if path else "mp3.mp3"


class Audio:
    """
    Audio wraps an MP3 Decoder to make it simpler to play music. It is a relatively
    light wrapper buts saves some boilerplate. It requires an audio_out to play the
    music such as an AudioOut or I2SOut.
    """

    def __init__(self, audio_out):
        self.audio_out = audio_out
        self.decoder = None
        self._file = None

        if environment.are_pins_available() and audio_out is None:
            raise ValueError("audio cannot be None")

        if audio_out is not None:
            if MP3Decoder is None:
                raise ValueError("audiomp3 (MP3 decoding) is not supported on this device.")

            # You have to specify some mp3 file when creating the decoder
            self._file = open(_placeholder_mp3(), "rb")
            self.decoder = MP3Decoder(self._file)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deinit()

    def deinit(self) -> None:
        """
        Releases the decoder and audio output. Safe to call multiple times.
        """
        if self.audio_out:
            self.decoder.deinit()
            self.audio_out.deinit()
            self.decoder = None
            self.audio_out = None

        self._close_file()

    def _close_file(self) -> None:
        if self._file:
            self._file.close()
            self._file = None

    def play(self, filename: str) -> None:
        """
        Plays the given MP3 file, interrupting anything currently playing.

        :param filename: The MP3 file to play.
        """
        if filename is None or len(filename) <= 0:
            raise ValueError("filename must be specified")

        if self.audio_out:
            # Stop first so the decoder is not reading the old file while it is swapped
            # out, then close the old file rather than leaving it for the GC; file
            # handles are a scarce resource on CircuitPython.
            self.audio_out.stop()
            new_file = open(filename, "rb")
            self.decoder.file = new_file
            self._close_file()
            self._file = new_file
            self.audio_out.play(self.decoder)

    @property
    def playing(self) -> bool:
        """
        Returns whether audio is currently playing.
        """
        return self.audio_out.playing if self.audio_out else False

    @property
    def paused(self) -> bool:
        """
        Returns whether playback is currently paused.
        """
        return self.audio_out.paused if self.audio_out else False

    def pause(self) -> None:
        """
        Pauses playback.
        """
        if self.audio_out:
            self.audio_out.pause()

    def resume(self) -> None:
        """
        Resumes playback after a pause.
        """
        if self.audio_out:
            self.audio_out.resume()

    def stop(self) -> None:
        """
        Stops playback.
        """
        if self.audio_out:
            self.audio_out.stop()


# See the following sources for reference:
#  * https://docs.circuitpython.org/en/latest/shared-bindings/audiopwmio/
#  * https://docs.circuitpython.org/en/latest/shared-bindings/audiomp3/
#  * https://learn.adafruit.com/circuitpython-essentials/circuitpython-audio-out
#  * https://learn.adafruit.com/circuitpython-essentials/circuitpython-mp3-audio
# noinspection pep8-naming
def PwmAudio(pin) -> Audio:
    """
    Returns an Audio that uses a single pin to play music via PWM.

    :param pin: The pin to output audio on.
    """
    if environment.are_pins_available() and pin is None:
        raise ValueError("pin cannot be None")

    audio_out = None

    if environment.are_pins_available():
        try:
            # noinspection PyPackageRequirements
            from audioio import AudioOut
        except ImportError:
            try:
                from audiopwmio import PWMAudioOut as AudioOut
            except ImportError:
                raise ValueError("audioio and audiopwmio are not supported on this device.")

        audio_out = AudioOut(pin)

    return Audio(audio_out)


# See the following sources for reference:
#  * https://docs.circuitpython.org/en/latest/shared-bindings/audiobusio/
#  * https://learn.adafruit.com/mp3-playback-rp2040/pico-i2s-mp3
#  * https://learn.adafruit.com/i2s-amplifier-bff/circuitpython
# noinspection pep8-naming
def I2sAudio(bit_clock, left_right_clock, data) -> Audio:
    """
    Returns an Audio that uses three pins to play music via I2S.
    """
    if environment.are_pins_available():
        if bit_clock is None:
            raise ValueError("bit_clock cannot be None")
        if left_right_clock is None:
            raise ValueError("left_right_clock cannot be None")
        if data is None:
            raise ValueError("data cannot be None")

    audio_out = None

    if environment.are_pins_available():
        # noinspection unresolved-references
        from audiobusio import I2SOut
        audio_out = I2SOut(bit_clock, left_right_clock, data)

    return Audio(audio_out)


class Queue:
    """
    Queue is used to play MP3 audio files in a sequence. Queue allows
    the MP3 files to be queued; these will then be picked up in turn and
    played through the Audio instance. Basic controls to pause, resume and
    stop are provided along with a cancel option which stops the music and
    clears the queue.
    """

    def __init__(self, audio: Audio):
        if audio is None:
            raise ValueError("audio cannot be None")

        if not isinstance(audio, Audio):
            raise ValueError("audio must be an Audio, such as one returned by PwmAudio or I2sAudio")

        self._audio = audio
        self._queue = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.deinit()

    def deinit(self) -> None:
        """
        Clears the queue and deinits() the audio.
        """
        self._audio.stop()
        self._queue.clear()
        self._audio.deinit()

    def queue(self, filename: str) -> None:
        """
        Adds an MP3 file to the queue to be picked up and played.

        :param filename: The MP3 file to add to the queue.
        """
        self._queue.append(filename)

    @property
    def playing(self) -> bool:
        """
        Returns whether the audio is playing or not.
        """
        return self._audio.playing

    @property
    def paused(self) -> bool:
        """
        Returns whether the audio is paused or not.
        """
        return self._audio.paused

    def pause(self) -> None:
        """
        Pauses the audio payback.
        """
        self._audio.pause()

    def resume(self) -> None:
        """
        Resumes the audio playback.
        """
        self._audio.resume()

    def stop(self) -> None:
        """
        Stops the audio playback.
        """
        self._audio.stop()

    def cancel(self) -> None:
        """
        Stops playing any music and empties the queue.
        """
        self._queue.clear()
        self._audio.stop()

    def update(self) -> None:
        """
        Checks for songs in the queue and plays them if nothing is playing.
        """
        if not self._audio.playing and len(self._queue) > 0:
            song = self._queue.pop(0)
            self._audio.play(song)
