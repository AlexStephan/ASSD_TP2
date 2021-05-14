from enum import Enum
from typing import List
import numpy as np

samples_per_sec = 44100
Ts = 1 / samples_per_sec


class EFFECT(Enum):
    # NOTA: el contenido actual es solo un placeholder1234
    # cambiar cuando se cuenten con instrumentos ya programados
    DELAY = 0
    REVERBERATION = 1
    FLANGER = 2


def eco(in_Arr: List, in_i, out_Arr: List, out_i, length, delay, a):
    # y(n) = x(n) + a*x(n-delay)
    delay = int(np.floor(delay*samples_per_sec))
    #delay *= samples_per_sec
    for i in range(in_i, in_i+length + 1, 1):
        if i < delay:
            out_Arr[i] = in_Arr[i]
        else:
            out_Arr[i] = in_Arr[i] + a * in_Arr[i - delay]
    return


def simple_reverb(in_Arr: List, in_i, out_Arr: List, out_i, length, delay, a):
    # y(n) = x(n) + a*x(n-delay)
    delay *= int(samples_per_sec*delay)
    for i in range(in_i, in_i + length + 1, 1):
        if i < delay:
            out_Arr[i] = in_Arr[i]
        else:
            out_Arr[i] = in_Arr[i] + a * out_Arr[i - delay]
    return


def flanger(in_Arr: List, in_i, out_Arr: List, out_i, length, f0=1, k=0.002):
    # y(n) = BL*x(n) + FF*x(n-M(n)) + FB*y(n-M(n))
    BL = 0.7
    FF = 0.7
    FB = 0.7
    for i in range(in_i, in_i + length + 1, 1):
        Mn = np.floor(k * np.sin(2 * np.pi * f0 * i))  # cambiara si en vez de in_i pongo out_i?
        if in_i + i < Mn and out_i + i < Mn:
            out_Arr[i] = BL * in_Arr[i]
        elif in_i + i < Mn:
            out_Arr[i] = BL * in_Arr[i] + FB * out_Arr[i - Mn]
        elif out_i + i < Mn:
            out_Arr[i] = BL * in_Arr[i] + FF * in_Arr[i - Mn]
        else:
            out_Arr[i] = BL * in_Arr[i] + FF * in_Arr[i - Mn] + FB * out_Arr[i - Mn]

    return


#class Effect():
#    def __init__(self):
#        return
