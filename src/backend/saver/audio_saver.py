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
            max = np.amax(np.abs(audio_track.content))
            #if max > (2**15)-1:
            audio_track.content = np.multiply(audio_track.content, ((2**15)-1)/max)
            write(filename, sample_rate, np.int16(audio_track.content))#.astype(np.int16))
        except:
            print("ERROR!!! AudioSaver coudn't save wav file!!!")
            return False

        return True
