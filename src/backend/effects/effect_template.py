from src.backend.effects.effect_list import EFFECT
from src.backend.audio_tracks.audio_block import AudioBlock
from typing import List

# Por qué no le agregué estados esta vez, a diferencia de synthesis_template?
# no lo se. Supongo que quiero q la aplicacion de los efectos sea mas directa

# de momento, no test realizados sobre la señal. Capaz eventualmente


class EffectTemplate(object):
    def __init__(self):
        print("EffectTemplate created!")
        self.previous = AudioBlock()  # para emplear con overlap & save/add

    # alternativamente, se puede modificar directamente el campo
    # previous. Digo, yo no muerdo
    def set_previous(self, previous: AudioBlock):
        self.previous = previous

    def get_previous(self) -> AudioBlock:
        return self.previous

    def clean_previous(self):
        self.previous = AudioBlock()

    # sobreescribir en los objetos hijos esta clase sin mayor remordimiento
    # los datos van en config!
    def apply_effect(self, input_block: AudioBlock, config: list) -> AudioBlock:
        return AudioBlock()


EffectConfig = List
EffectAndConfig = List[EffectTemplate, EffectConfig]

EffectsForTrack = List[EffectAndConfig]
AllEffects = List[EffectsForTrack]
