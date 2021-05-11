from scipy.io.wavfile import write
from src.backend.audio_tracks.audio_track import AudioTrack
from src.backend.audio_tracks.audio_constants import sample_rate
import numpy as np

class AudioSaver(object):
    def __init__(self):
        print("AudioSaver created!")

    def save_wav_file(self, audio_track: AudioTrack, filename: str) -> bool:
        print("AudioSaver: save_wav_file")
        # Intentar guardar el track de audio como .wav
        # Si salio bien, devolver True, sino, devolver False
        try:
            write(filename, sample_rate, audio_track.content.astype(np.int16))
        except:
            print("ERROR!!! AudioSaver coudn't save wav file!!!")
            return False

        return True
