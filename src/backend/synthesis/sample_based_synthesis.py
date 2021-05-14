from src.backend.instruments.instrument_list import INSTRUMENT
from src.backend.tracks.track import Track
from src.backend.audio_tracks.audio_track import AudioTrack
from src.backend.synthesis.synthesis_template import SynthesisTemplate, STATE
import numpy as np
import pytsmod
from scipy.io.wavfile import read

class SampleBasedSynthesis(SynthesisTemplate):
    def __init__(self):
        super().__init__()
        self.instrument = ""
        self.track_len = 0
        self.track_pos = 0
        self.note_freq = 0
        self.note_start = 0
        self.note_end = 0
        self.note_vel = 0
        self.synth_track = []

        #Fixed
        self.sample_array = []
        self.instruments_array = ["Piano"]
        self.sample_freq = {"Piano": 440}

    def synthesize_audio_track(self, track: Track, instrument: INSTRUMENT):
        super().synthesize_audio_track(track, instrument)
        local_instrument = self.global_instrument_to_local_instrument(instrument)
        self.state = STATE.LOADED
        if local_instrument not in self.instruments_array:
            self.state = STATE.ERROR
        else:
            self.instrument = local_instrument
        self.track_len = len(track)
        while self.track_pos != self.track_len:
            self.note_freq = self.get_note_freq()
            self.note_start = int(self.get_note_start() * 44100)
            self.note_end = int(self.get_note_end() * 44100)
            self.note_vel = self.get_note_vel()
            self.synthesize()

            for n in range(self.note_end - self.note_start):
                self.audio_track[self.note_start + n] += self.synth_track[n]
                n += 1
            self.track_pos += 1

    def time_scale(self):
        duration_ratio = (self.note_end - self.note_start) / self.get_sample_duration()
        if duration_ratio == 1:
            return self.synth_track
        return np.transpose(pytsmod.phase_vocoder(self.sample_array, duration_ratio))

    def pitch_shift(self):
        note_freq = self.note_freq
        shift_factor = note_freq / self.get_sample_freq()
        if shift_factor == 1:
            return self.synth_track
        return self.speedx(np.transpose(pytsmod.phase_vocoder(self.sample_array, shift_factor)), shift_factor)

    def speedx(self, sound_array, factor):                                # http://zulko.github.io/blog/2014/03/29/soundstretching-and-pitch-shifting-in-python/
        """ Multiplies the sound's speed by some `factor` """
        indices = np.round(np.arange(0, len(sound_array), factor))
        indices = indices[indices < len(sound_array)].astype(int)
        return sound_array[indices.astype(int)]

    def get_note_freq(self):
        return self.track[self.track_pos].frequency

    def get_note_start(self):
        return self.track[self.track_pos].start

    def get_note_end(self):
        return self.track[self.track_pos].end

    def get_note_vel(self):
        return self.track[self.track_pos].velocity

    def synthesize(self):
        self.synth_track = self.pitch_shift()
        self.synth_track = self.time_scale()

    def set_sample_array(self):
        fs,  self.sample_array = read('resources\\wav_files\\' + self.instrument +" 440Hz" + '.wav', mmap=False)

    def get_sample_freq(self):
        return self.sample_freq[self.instrument]

    def get_sample_duration(self):
        return len(self.sample_array)

    def global_instrument_to_local_instrument(self,GLOBAL_INST:INSTRUMENT)->str:
        if GLOBAL_INST == INSTRUMENT.PIANO_2:
            return "Piano"
        else:
            return ""
