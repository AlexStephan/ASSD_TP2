from src.backend.audio_tracks.audio_track import AudioTrack,AudioTrackGroup
from src.backend.audio_tracks.audio_block import AudioBlock
from src.backend.player.audio_block_player import AudioBlockPlayer

from src.backend.effects.effect_template import EffectTemplate,EffectConfig,EffectAndConfig,EffectsForTrack,AllEffects

from enum import Enum

# NOTA! la tool gui debera tener la lista real de los filtros y su config
# que sera enviada a esta clase


class STATE(Enum):
    EMPTY = 0
    PAUSED = 1
    PLAYING = 2
    FINISHED = 3
    ERROR = 4


class PlayerManager(object):
    def __init__(self):
        print("PlayerManager created!")
        self.audio_tracks = []
        self.state = STATE.EMPTY
        self.position = 0  # en bloques

        self.block_player = AudioBlockPlayer()

    def load_audio_tracks(self, audio_tracks: AudioTrackGroup):
        print("PlayerManager: load_audio_tracks")
        # Si no le gustó:
        #   self.state = STATE.ERROR
        # Si si le gustó:
        self.audio_tracks = audio_tracks
        self.state = STATE.PAUSED

    def continue_playing(self, effects: AllEffects):
        print("PlayerManager: continue_playing")
        if self.state == STATE.FINISHED:
            print("... from finished state")
            self.position = 0
        if self.state == STATE.PAUSED or self.state == STATE.PLAYING or self.state == STATE.FINISHED:
            self.state = STATE.PLAYING
            # Separa los bloques del grupo de audio_tracks correspondientes a la posicion self.position
            # Aplica a cada bloque los filtros correspondientes de filtros
            # Aplica a la mezcla los filtros correspondientes de filtros (los ultimos de la lista)
            # Al resultado, current_block lo hace pasar por el block player
            current_block = AudioBlock()
            self.block_player.play_audio_block(current_block)

    def stop(self):
        print("PlayerManager: stop")
        if self.state == STATE.PAUSED or self.state == STATE.PLAYING or self.state == STATE.FINISHED:
            self.state = STATE.PAUSED
            self.position = 0

    def pause(self):
        print("PlayerManager: stop")
        if self.state == STATE.PLAYING:
            self.state = STATE.PAUSED
