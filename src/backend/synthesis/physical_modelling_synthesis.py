from src.backend.instruments.instrument_list import INSTRUMENT
from src.backend.tracks.track import Track
from src.backend.audio_tracks.audio_track import AudioTrack
from src.backend.synthesis.synthesis_template import SynthesisTemplate, STATE
from src.backend.midi2tracks import Midi2Tracks
from src.backend.saver.audio_saver import AudioSaver
import numpy as np
import itertools as iter

fs = 44100

class PhysicalModellingSynthesis(SynthesisTemplate):
    def __init__(self):
        super().__init__()
        self.counter = 0

    def synthesize_audio_track(self, track: Track, instrument: INSTRUMENT):
        super().synthesize_audio_track(track, instrument)
        self.audio_track.content = [0]*len(self.track)
        aux = [0]*len(self.track)
        self.state = STATE.ERROR
        t_end = 0
        if instrument == INSTRUMENT.GUITAR:
            for i in range(len(self.track)):
                aux[i] = self.__karplus_guitar(i)
                if t_end < track[i].end : t_end = track[i].end
            self.state = STATE.LOADED

            final = [0] * fs * int(t_end)
            for i in range(len(aux)):
                N_start = int(track[i].start*fs)
                note = np.pad(aux[i],(N_start,0))
                final = [x + y for x, y in iter.zip_longest(final, note, fillvalue=0)]
            self.audio_track.content = final

        elif instrument == INSTRUMENT.DRUM:
            for i in range(len(self.track)):
                aux[i] = self.__karplus_drum(i, 0.5, 2)
                if t_end < track[i].end: t_end = track[i].end
            self.state = STATE.LOADED

            final = [0] * fs * int(t_end)
            for i in range(len(aux)):
                N_start = int(track[i].start * fs)
                note = np.pad(aux[i], (N_start, 0))
                final = [x + y for x, y in iter.zip_longest(final, note, fillvalue=0)]
            self.audio_track.content = final

    def __karplus_guitar(self,i):
        length = self.track[i].end-self.track[i].start
        n = np.linspace(0, length, int(fs*length))
        l = int(fs/self.track[i].frequency-0.5)
        buff = (2 * np.random.randint(0, 2, l+2) - 1).astype(float)

        buff = self.__sound_box(l, buff) #Sound box
        #buff = self.__DC_block(l,buff,self.track[i].frequency) #DC Block

        y1 = self.__timbre_control(l,buff,8,180) #Timbre Control


        beta = fs/self.track[i].frequency - 0.5 - l
        rl = 0.9999**l
        a = 1/(1+beta)
        y = []
        for k in range(n.size):
            if k < l:
                sample_k = 0.5 * a * y1[k] + 0.5 * rl * (a+1) * y1[k + 1] + 0.5 * a * y1[k+2]
            else:
                sample_k = 0.5 * rl * y[k-l-2] + 0.5 * rl * (a+1) * y[k-l-1] + 0.5 * a * rl * y[k-l] - a * y[k-1]
            y.append(sample_k)
        return y


    def __karplus_drum(self,i,b,s):
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


    def __timbre_control(self, l, buff, times=5, fo=200):
        t = 1/abs(2*np.cos(2*np.pi*fo)+1)
        y1=[]
        for k in range(l+2):
            if k == 0:
                sample_k = t*buff[k]
            elif k == 1:
                sample_k = t * (buff[k] + buff[k-1])
            else:
                sample_k = t * (buff[k] + buff[k-1]+buff[k-2])
            y1.append(sample_k)

        if self.counter < times:
            self.counter += 1
            loop = self.__timbre_control(l,y1,times)
        else:
            loop = y1
        self.counter = 0
        return loop

    def __DC_block(self, l, buff,fo):
        a0 = 1/(1+((np.pi*fo)/10))
        a1 = -a0
        b1 = a0*(1-(np.pi*fo)/10)
        y0 = []
        for k in range(l+2):
            if k < 1:
                sample_k = a0*buff[k]
            else:
                sample_k = a0*buff[k] + a1*buff[k-1]+b1*y0[k-1]
            y0.append(sample_k)
        return y0

    def __sound_box(self,l, y,fo=180):
        df = 20
        R = 1 - (df * np.pi) / fs
        a1 = 2 * R * np.cos(2 * np.pi * fo / fs)
        a2 = R ** 2
        box=[]
        G = (np.sqrt(1 - 2 * R + R ** 2) * np.sqrt(1 - 2 * R * np.cos(8 * np.pi * fo / fs) + R ** 2)) / (
                    2 * np.sqrt(2 - 2 * np.cos(4 * np.pi * fo / fs)))
        for k in range(len(y)):
            if k < l:
                sample_k = G * y[k] - G * y[k + 2]
            else:
                sample_k = a1 * box[k - 1] - a2 * box[k - 2]
            box.append(sample_k)
        return box


if __name__ == '__main__':
    midi = Midi2Tracks()
    midi.load_midi_file("..\\..\\..\\resources\\midi_files\\simple_chord.mid")
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
    guitar.synthesize_audio_track(tracks[0], INSTRUMENT.DRUM)
    aux = guitar.audio_track
    m = abs(max(max(aux.content), min(aux.content),key=abs))
    norm = (2**15)/m
    aux_norm = AudioTrack
    aux_norm.content = [x * norm for x in aux.content]

    file = AudioSaver()
    file.save_wav_file(aux_norm,"Chord2.wav")