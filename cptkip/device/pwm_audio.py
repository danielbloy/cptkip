# See the following sources for reference:
#  * https://docs.circuitpython.org/en/latest/shared-bindings/audiopwmio/
#  * https://docs.circuitpython.org/en/latest/shared-bindings/audiomp3/
#  * https://learn.adafruit.com/circuitpython-essentials/circuitpython-audio-out
#  * https://learn.adafruit.com/circuitpython-essentials/circuitpython-mp3-audio
#
import cptkip.core.environment as environment

if environment.are_pins_available():
    try:
        from audiomp3 import MP3Decoder
    except ImportError:
        pass

    try:
        from audioio import AudioOut
    except ImportError:
        try:
            from audiopwmio import PWMAudioOut as AudioOut
        except ImportError:
            pass  # not always supported by every board!


    class Audio:

        def __init__(self, pin):
            self.audio = AudioOut(pin)
            # You have to specify some mp3 file when creating the decoder
            decoder = MP3Decoder(open("cptkip/mp3.mp3", "rb"))
            self.decoder = decoder

        def deinit(self) -> None:
            self.decoder.deinit()
            self.audio.deinit()

        def play(self, filename: str):
            if filename is None or len(filename) <= 0:
                raise ValueError("filename must be specified")

            self.decoder.file = open(filename, "rb")
            self.audio.play(self.decoder)

        @property
        def playing(self) -> bool:
            return self.audio.playing

        @property
        def paused(self) -> bool:
            return self.audio.paused

        def pause(self):
            return self.audio.pause()

        def resume(self):
            return self.audio.resume()

        def stop(self):
            return self.audio.stop()

else:

    class Audio:

        def __init__(self, pin):
            pass

        def deinit(self) -> None:
            pass

        def play(self, filename: str):
            if filename is None or len(filename) <= 0:
                raise ValueError("filename must be specified")

        @property
        def playing(self) -> bool:
            return False

        @property
        def paused(self) -> bool:
            return False

        def pause(self):
            pass

        def resume(self):
            pass

        def stop(self):
            pass


class Queue:
    """
    Queue is used to play MP3 audio files in a sequence. Queue allows
    the MP3 files to be queued; these will then be picked up in turn and
    played through the Audio instance. Basic controls to pause, resume and
    stop are provided along with a cancel option which stops the music and
    clears the queue.

    Instances of this class will need to register() with a Runner in order to work.
    """

    def __init__(self, audio: Audio):
        if audio is None:
            raise ValueError("audio cannot be None")

        if not isinstance(audio, Audio):
            raise ValueError("audio must be of type Audio")

        self.__audio = audio
        self.__queue = []

    def queue(self, filename: str):
        """
        Adds an MP3 file to the queue to be picked up and played.

        :param filename: The MP3 file to add to the queue.
        """
        self.__queue.append(filename)

    @property
    def playing(self) -> bool:
        """
        Returns whether the audio is playing or not.
        """
        return self.__audio.playing

    @property
    def paused(self) -> bool:
        """
        Returns whether the audio is paused or not.
        """
        return self.__audio.paused

    def pause(self):
        """
        Pauses the audio payback.
        """
        return self.__audio.pause()

    def resume(self):
        """
        Resumes the audio playback.
        """
        return self.__audio.resume()

    def stop(self):
        """
        Stops the audio playback.
        """
        return self.__audio.stop()

    def cancel(self):
        """
        Stops playing any music and empties the queue.
        """
        self.__queue.clear()
        self.__audio.stop()

    def update(self):
        """
        Checks for songs in the queue and plays them if nothing is playing.
        """
        if not self.__audio.playing and len(self.__queue) > 0:
            song = self.__queue.pop(0)
            self.__audio.play(song)
