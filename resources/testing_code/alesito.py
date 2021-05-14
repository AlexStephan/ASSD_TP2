from resources.testing_code.audio_loader import load_wav_file
from src.backend.saver.audio_saver import AudioSaver
from src.backend.audio_tracks.audio_track import AudioTrack
import numpy as np

from src.backend.effects.effect_list import eco,simple_reverb,flanger

valid,fs,original = load_wav_file("..\\wav_files\\Level Music 1.wav")
saver = AudioSaver()
final = AudioTrack()



input_array = np.array(original[:,0])
output_array = [0]*np.zeros(len(input_array))

c_input_array = input_array.tolist()

final.content = output_array

length = 1024
delay = 0.5
a = 0.25

i = 0

while i < len(input_array)-1:
    real_length = min(length,len(input_array)-i-1)
    eco(c_input_array,i,output_array,i,real_length,delay,a)
    i = i + real_length

saver.save_wav_file(final,"..\\wav_files\\Alesito.wav")