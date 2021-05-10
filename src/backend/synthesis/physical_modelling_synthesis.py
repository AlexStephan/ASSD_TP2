from src.backend.instruments.instrument_list import INSTRUMENT
from src.backend.tracks.track import Track
from src.backend.audio_tracks.audio_track import AudioTrack
from src.backend.synthesis.synthesis_template import SynthesisTemplate, STATE


class PhysicalModellingSynthesis(SynthesisTemplate):
    def __init__(self):
        super().__init__()

    def synthesize_audio_track(self, track: Track, instrument: INSTRUMENT):
        super().synthesize_audio_track(track, instrument)
        # Analizar si el instrumento escogido es compatible con este sintetizador
        # y generar el audio track
        # si no pudo hacerlo:
        #   self.state = STATE.ERROR
        # de lo contrario
        self.state = STATE.LOADED
