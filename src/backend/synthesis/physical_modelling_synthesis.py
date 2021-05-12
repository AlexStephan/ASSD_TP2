from src.backend.instruments.instrument_list import INSTRUMENT
from src.backend.tracks.track import Track
from src.backend.audio_tracks.audio_track import AudioTrack
from src.backend.synthesis.synthesis_template import SynthesisTemplate, STATE
from src.backend.midi2tracks import Midi2Tracks
from src.backend.saver.audio_saver import AudioSaver
import numpy as np

class PhysicalModellingSynthesis(SynthesisTemplate):
    def __init__(self):
        super().__init__()

    def synthesize_audio_track(self, track: Track, instrument: INSTRUMENT):
        super().synthesize_audio_track(track, instrument)
        self.audio_track.content = [0]*len(self.track)
        aux = [0]*len(self.track)
        self.state = STATE.ERROR
        if instrument == INSTRUMENT.GUITAR:
            for i in range(len(self.track)):
               aux[i] = self.__karplus_guitar(i)
            self.state = STATE.LOADED

        elif instrument == INSTRUMENT.DRUM:
            for i in range(len(self.track)):
                aux[i] = self.__karplus_drum(i, 0.5, 2)
            self.state = STATE.LOADED
        self.audio_track.content = [item for sublist in aux for item in sublist]

    def __karplus_guitar(self,i):
        fs = 8e3
        length = self.track[i].end-self.track[i].start
        n = np.linspace(0, length, int(fs * length))
        l = int(fs/self.track[i].frequency-0.5)
        beta = fs/self.track[i].frequency - 0.5 - l
        rl = 0.9999**l
        a = 1/(1+beta)
        buff = (2 * np.random.randint(0, 2, l+2) - 1).astype(float)
        y = []
        for k in range(n.size):
            if k < l:
                sample_k = 0.5 * a * buff[k] + 0.5 * rl * (a+1) * buff[k + 1] + 0.5 * a * buff[k+2]
            else:
                sample_k = 0.5 * rl * y[k-l-2] + 0.5 * rl * (a+1) * y[k-l-1] + 0.5 * a * rl * y[k-l] - a * y[k-1]
            y.append(sample_k)
        return y


    def __karplus_drum(self,i,b,s):
        fs = 20e3
        length = self.track[i].end-self.track[i].start
        n = np.linspace(0, length, int(fs * length))
        l = int(fs/self.track[i].frequency-0.5)
        rl = 0.9999**l
        buff = (2 * np.random.randint(0, 2, l+2) - 1).astype(float)
        y = []
        for k in range(n.size):
            prob = np.random.binomial(1, b)
            p = float(prob == 1) * 2 - 1
            r = np.random.binomial(1, 1 - (1 / s))
            if k < l:
                sample_k = 0.5 * (buff[k + 1] + buff[k])
            else:
                if r == 1:
                    sample_k = p * y[k - l]
                else:
                    sample_k = p * 0.5 * rl * (y[k - l] + y[k - l - 1])
            y.append(sample_k)
        return y

fs =44.1e3
midi = Midi2Tracks()
midi.load_midi_file("..\\..\\..\\resources\\midi_files\\Concierto-De-Aranjuez.mid")
tracks = midi.get_array_of_tracks()
for n, channel in enumerate(tracks):
    print("\n\n\nCHANNEL {}\n".format(n))
    for note in channel:
        print("Note:")
        print("Start = {}".format(note.start))
        print("End = {}".format(note.end))
        print("Velocity = {}".format(note.velocity))
        print("Number = {}".format(note.number))
        print("Frequency = {}".format(note.frequency))

guitar = PhysicalModellingSynthesis()
guitar.synthesize_audio_track(tracks[0], INSTRUMENT.GUITAR)
aux = guitar.audio_track
m = abs(max(max(aux.content), min(aux.content),key=abs))
norm = (2**15)/m
aux_norm = AudioTrack
aux_norm.content = [x * norm for x in aux.content]

file = AudioSaver()
file.save_wav_file(aux,"Test_Guitar")