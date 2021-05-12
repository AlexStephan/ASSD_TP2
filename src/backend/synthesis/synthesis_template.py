from src.backend.instruments.instrument_list import INSTRUMENT
from src.backend.tracks.track import Track
from src.backend.audio_tracks.audio_track import AudioTrack

from enum import Enum


class STATE(Enum):
    EMPTY = 0
    LOADED = 1
    ERROR = 2


class SynthesisTemplate(object):
    def __init__(self):
        print("SynthesisTemplate created!")
        self.state = STATE.EMPTY
        self.track = []
        self.instrument = None
        self.audio_track = AudioTrack()

    def synthesize_audio_track(self, track: Track, instrument: INSTRUMENT):
        print("SynthesisTemplate: synthesize_audio_track")
        self.track = track
        self.instrument = instrument

    def get_audio_track(self) -> AudioTrack:
        if self.state == STATE.LOADED:
            return self.audio_track
        else:
            return AudioTrack()

    def is_valid(self) -> bool:
        return self.state == STATE.LOADED

