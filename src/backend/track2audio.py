from enum import Enum

from src.backend.tracks.track import Track
from src.backend.audio_tracks.audio_track import AudioTrack
from src.backend.instruments.instrument_list import INSTRUMENT

from src.backend.synthesis.additive_synthesis import AdditiveSynthesis
from src.backend.synthesis.fm_synthesis import FMSynthesis
from src.backend.synthesis.physical_modelling_synthesis import PhysicalModellingSynthesis
from src.backend.synthesis.sample_based_synthesis import SampleBasedSynthesis


class STATE(Enum):
    EMPTY = 0
    LOADED = 1
    ERROR = 2


class Track2Audio(object):
    def __init__(self):
        print("Track2Audio created!")
        self.state = STATE.EMPTY
        self.generated_audiotrack = AudioTrack()
        self.track = AudioTrack()
        self.instrument = None

        # me parecio que seria conveniente que se creen los sintetizadores
        # ahora, y no en el momento de usar. Nada, capaz no estan
        # de acuerdo. No cambia mucho el modificar esto

        self.additive_synth = AdditiveSynthesis()
        self.fm_synth = FMSynthesis()
        self.physical_synth = PhysicalModellingSynthesis()
        self.sample_synth = SampleBasedSynthesis()

    def generate_audio_track(self, track: Track, instrument: INSTRUMENT):
        print("Track2Audio: generate_audio_track")
        # Utilizando el Track y el intrumento, general el audiotrack
        # Deberá emplear las clases de la carpeta "synthesis"
        # Si no pudo realizarse:
        #   self.state = STATE.ERROR
        # de lo contrario
        self.state = STATE.LOADED
        self.track = track
        self.instrument = instrument

    def get_audio_track(self) -> AudioTrack:
        print("Track2Audio: get_audio_track")
        if self.state == STATE.LOADED:
            return self.generated_audiotrack
        else:
            return AudioTrack()

    def is_valid(self) -> bool:
        return self.state == STATE.LOADED
