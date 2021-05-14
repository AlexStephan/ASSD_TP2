from scipy.io.wavfile import read
import numpy as np


def load_wav_file(filename: str) -> list:
    print("AudioLoader: load_wav_file")
    try:
        rate,audio_track_group = read(filename)
    except:
        print("ERROR!!! AudioLoader coudn't open wav file!!!")
        return [False,None,[]]
    return [True,rate,audio_track_group]


#class AudioLoader(object):
#    def __init__(self):
#        print("AudioLoader created!")
