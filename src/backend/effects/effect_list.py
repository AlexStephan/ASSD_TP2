from enum import Enum
from typing import List
import numpy as np

samples_per_sec = 44100
Ts = 1 / samples_per_sec


class EFFECT(Enum):
    # NOTA: el contenido actual es solo un placeholder
    # cambiar cuando se cuenten con instrumentos ya programados
    DELAY = 0
    REVERBERATION = 1
    FLANGER = 2


class Effect():
    def __init__(self):
        return

    def eco(self, in_Arr: List, in_i, out_Arr: List, out_i, length, delay, a):
        # y(n) = x(n) + a*x(n-delay)
        delay *= samples_per_sec
        for i in range(in_i, length + 1, 1):
            if in_i + i < delay:
                out_Arr[out_i + i] = in_Arr[in_i + i]
            else:
                out_Arr[out_i + i] = in_Arr[in_i + i] + a * in_Arr[in_i + i - delay]
        return

    def simple_reverb(self, in_Arr: List, in_i, out_Arr: List, out_i, length, delay, a):
        # y(n) = x(n) + a*x(n-delay)
        delay *= samples_per_sec
        for i in range(in_i, length + 1, 1):
            if out_i + i < delay:
                out_Arr[out_i + i] = in_Arr[in_i + i]
            else:
                out_Arr[out_i + i] = in_Arr[in_i + i] + a * out_Arr[out_i + i - delay]
        return

    def flanger(self, in_Arr: List, in_i, out_Arr: List, out_i, length, f0=1, k=0.002):
        # y(n) = BL*x(n) + FF*x(n-M(n)) + FB*y(n-M(n))
        BL = 0.7
        FF = 0.7
        FB = 0.7
        for i in range(in_i, length + 1, 1):
            Mn = np.floor(k * np.sin(2 * np.pi * f0 * in_i + i))  # cambiara si en vez de in_i pongo out_i?
            if in_i + i < Mn and out_i + i < Mn:
                out_Arr[out_i + i] = BL * in_Arr[in_i + i]
            elif in_i + i < Mn:
                out_Arr[out_i + i] = BL * in_Arr[in_i + i] + FB * out_Arr[out_i + i - Mn]
            elif out_i + i < Mn:
                out_Arr[out_i + i] = BL * in_Arr[in_i + i] + FF * in_Arr[in_i + i - Mn]
            else:
                out_Arr[out_i + i] = BL * in_Arr[in_i + i] + FF * in_Arr[in_i + i - Mn] + FB * out_Arr[out_i + i - Mn]

        return
