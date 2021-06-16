import pytsmod
from scipy.io.wavfile import read, write
import numpy as np

def pitch_shift(wav_array, note_freq):
    note_sample = 440
    shift_factor = note_freq / note_sample
    y = pytsmod.phase_vocoder(wav_array, shift_factor, phase_lock=
                              True)
    y = np.transpose(y)
    return speedx(y, shift_factor)

def speedx(sound_array, factor):                                    #http://zulko.github.io/blog/2014/03/29/soundstretching-and-pitch-shifting-in-python/
    """ Multiplies the sound's speed by some `factor` """
    indices = np.round( np.arange(0, len(sound_array), factor) )
    indices = indices[indices < len(sound_array)].astype(int)
    return sound_array[ indices.astype(int) ]

fs, x = read('..\\wav_files\\Piano 440Hz.wav', mmap=False)
y = pitch_shift(x, 550)
#y = pytsmod.phase_vocoder(x, 2)
#y = np.transpose(y)
write('..\\wav_files\\bokita.wav', fs, np.int16(y))