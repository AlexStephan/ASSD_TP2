from src.backend.instruments.instrument_list import INSTRUMENT
from src.backend.tracks.track import Track
from src.backend.audio_tracks.audio_track import AudioTrack
from src.backend.synthesis.synthesis_template import SynthesisTemplate, STATE

import numpy as np
import scipy as sp
import librosa


def butter_bandpass(lowcut, highcut, Fs, order=10):
    sos = sp.signal.butter(order, [lowcut, highcut], btype='band', analog=False, output='sos', fs=Fs)
    return sos


def butter_bandpass_filter(data, lowcut, highcut, Fs, order=10):
    sos = butter_bandpass(lowcut, highcut, Fs, order=order)
    y = sp.signal.sosfilt(sos, data)
    return y


def compute_adsr(x, len_A, len_D, len_S, len_R, A0, kA0, alpha):
    """Computation of idealized linear ADSR model
    Args:
        len_A (int): Length (samples) of A phase
        len_D (int): Length (samples) of D phase
        len_S (int): Length (samples) of S phase
        len_R (int): Length (samples) of R phase
        A0 (float): Height of S phase
        kA0 (float): Height of A phase
        alpha (float): S phase decay

    Returns:
        curve_ADSR (np.ndarray): ADSR model
    """
    curve_A = np.arange(len_A) * kA0 / len_A  # El ataque es una linea recta desde 0 hasta kA0
    curve_D = kA0 - np.arange(len_D) * (kA0 - A0) / len_D  # El decay es una linea recta desde kA0 hasta A0
    curve_S = A0 - alpha * np.arange(len_S)  # El sustain es una linea con pendiente alpha que comienza en A0
    curve_R = (A0 - alpha * len_S) * (
                1 - np.arange(1, len_R + 1) / len_R)  # El release es una linea recta que llega a 0
    curve_ADSR = np.concatenate((curve_A, curve_D, curve_S, curve_R))  # Uno las curvas
    curve_ADSR = np.hstack([curve_ADSR, np.zeros(x.size - curve_ADSR.size)]) # Relleno con ceros luego del release
    return curve_ADSR


def compute_envelope(x, win_len_sec, Fs):
    """Computation of a signal's envelopes
    Args:
        x (np.ndarray): Signal (waveform) to be analyzed
        win_len_sec (float): Length (seconds) of the window
        Fs (scalar): Sampling rate

    Returns:
        env (np.ndarray): Magnitude envelope
        env_upper (np.ndarray): Upper envelope
        env_lower (np.ndarray): Lower envelope
    """
    win_len_half = round(win_len_sec * Fs * 0.5)  # Guardo la mitad del largo de ventana para poder moverla
    N = x.shape[0]  # Guardo el largo de la dimension tiempo de la señal ingresada
    env = np.zeros(N)  # Creo un ndarray con ceros para la envolvente en amplitud
    for i in range(N):
        i_start = max(0, i - win_len_half)  # Comienzo de la ventana
        i_end = min(N, i + win_len_half)  # Fin de la ventana
        env[i] = np.amax(np.abs(x)[i_start:i_end])  # Obtengo el maximo del modulo de la señal en la ventana
    return env


# EXAMPLE: Fs=44100, musicPath="C:\Users\Tobi\OneDrive\Desktop\ITBA\2021 1Q\ASSD\music.wav", win_len_sec=0.01
# x,Fs = librosa.load(musicPath, sr=Fs)
# compute_envelope(x, win_len_sec, Fs)


def extract_partial(x, n_of_partial, Fs, fundFreq):
    """Extraction and Isolation of a signal's partial
    Args:
        x (np.ndarray): Signal (waveform) to be analyzed
        n_of_partial (int): Harmonic multiplier of fundamental frequency
        Fs (scalar): Sampling rate
        fundFreq (float): Fundamental frequency of note

    Returns:
        partial (np.ndarray): Partial signal (waveform)
    """
    partialFreq = fundFreq * n_of_partial
    lowcut = partialFreq - 10 * n_of_partial
    highcut = partialFreq + 10 * n_of_partial
    partial = butter_bandpass_filter(x, lowcut, highcut, Fs)
    return partial


class AdditiveSynthesis(SynthesisTemplate):
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
