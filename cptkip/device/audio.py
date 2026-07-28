import cptkip.core.environment as environment

if environment.are_pins_available():
    try:
        # noinspection PyUnresolvedReferences
        from audiomp3 import MP3Decoder
    except ImportError:
        pass


class Audio:

    def __init__(self, audio):
        self.audio = audio
        self.decoder = None

        if environment.are_pins_available() and audio is None:
            raise ValueError("audio cannot be None")

        if audio is not None:
            # You have to specify some mp3 file when creating the decoder
            decoder = MP3Decoder(open("cptkip/mp3.mp3", "rb"))
            self.decoder = decoder

    def deinit(self) -> None:
        """
        Releases the decoder and audio output. Safe to call multiple times.
        """
        if self.audio:
            self.decoder.deinit()
            self.audio.deinit()
            self.decoder = None
            self.audio = None
            self.pin = None

    def play(self, filename: str) -> None:
        """
        Plays the given MP3 file, interrupting anything currently playing.

        :param filename: The MP3 file to play.
        """
        if filename is None or len(filename) <= 0:
            raise ValueError("filename must be specified")

        if self.audio:
            self.decoder.file = open(filename, "rb")
            self.audio.play(self.decoder)

    @property
    def playing(self) -> bool:
        """
        Returns whether audio is currently playing.
        """
        return self.audio.playing if self.audio else False

    @property
    def paused(self) -> bool:
        """
        Returns whether playback is currently paused.
        """
        return self.audio.paused if self.audio else False

    def pause(self) -> None:
        """
        Pauses playback.
        """
        if self.audio:
            self.audio.pause()

    def resume(self) -> None:
        """
        Resumes playback after a pause.
        """
        if self.audio:
            self.audio.resume()

    def stop(self) -> None:
        """
        Stops playback.
        """
        if self.audio:
            self.audio.stop()


# See the following sources for reference:
#  * https://docs.circuitpython.org/en/latest/shared-bindings/audiopwmio/
#  * https://docs.circuitpython.org/en/latest/shared-bindings/audiomp3/
#  * https://learn.adafruit.com/circuitpython-essentials/circuitpython-audio-out
#  * https://learn.adafruit.com/circuitpython-essentials/circuitpython-mp3-audio
class PwmAudio(Audio):
    """
    Audio wraps up AudioOut and an MP3 Decoder to make it simpler to play
    music. It is a relatively light wrapper buts saves some boilerplate.
    """

    def __init__(self, pin):
        """
        :param pin: The pin to output audio on.
        """
        if environment.are_pins_available() and pin is None:
            raise ValueError("pin cannot be None")

        audio = None

        if environment.are_pins_available():
            try:
                # noinspection PyPackageRequirements
                from audioio import AudioOut
            except ImportError:
                try:
                    # noinspection PyUnresolvedReferences
                    from audiopwmio import PWMAudioOut as AudioOut
                except ImportError:
                    pass  # not always supported by every board!

            audio = AudioOut(pin)

        super().__init__(audio)


# See the following sources for reference:
#  * https://docs.circuitpython.org/en/latest/shared-bindings/audiobusio/
#  * https://learn.adafruit.com/mp3-playback-rp2040/pico-i2s-mp3
#  * https://learn.adafruit.com/i2s-amplifier-bff/circuitpython
class I2sAudio(Audio):
    pass
    # TODO: Implement


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
            raise ValueError("audio must be of type PwmAudio or I2SAudio")

        self._audio = audio
        self._queue = []

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
        return self._audio.pause()

    def resume(self) -> None:
        """
        Resumes the audio playback.
        """
        return self._audio.resume()

    def stop(self) -> None:
        """
        Stops the audio playback.
        """
        return self._audio.stop()

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
