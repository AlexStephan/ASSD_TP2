from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

from matplotlib.mlab import window_hanning,window_none
import numpy as np
import scipy.signal as ss

from src.backend.audio_tracks.audio_track import AudioTrack
from typing import Callable


def blackman(a: list) -> list:
    return np.multiply(a,np.blackman(len(a)))


def bartlett(a: list) -> list:
    return np.multiply(a,np.bartlett(len(a)))


def hamming(a: list) -> list:
    return np.multiply(a,np.hamming(len(a)))


def blackmanharris(a: list) -> list:
    return np.multiply(a,ss.blackmanharris(len(a)))


class AudioTrack2Spectrum(object):
    def __init__(self):
        print("AudioTrack2Spectrum created!")

    def draw_spectrum(self, audio_track: AudioTrack, Fs: float, NFFT:int, noverlap: int, window: Callable, axis):
        print("AudioTrack2Spectrum draw_spectrum")
        Pxx,freqs,bins,im = axis.specgram(audio_track.content,NFFT=NFFT,Fs=Fs,noverlap=noverlap,window=window)
