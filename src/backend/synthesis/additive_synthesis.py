from src.backend.instruments.instrument_list import INSTRUMENT
from src.backend.tracks.track import Track
from src.backend.audio_tracks.audio_track import AudioTrack
from src.backend.synthesis.synthesis_template import SynthesisTemplate, STATE

import numpy as np
import math
import scipy as sp
import librosa


def butter_bandpass(lowcut, highcut, Fs, order=10):
    """Gathering of SOS of bandpass filter
            Args:
                lowcut (float): lowest frequency at with bandpass gain is -3dB
                highcut (float): highest frequency at with bandpass gain is -3dB
                Fs (float): sampling frequency
            Returns:
                sos (ndarray): Second Order sections representations of the IIR filter
    """
    sos = sp.signal.butter(order, [lowcut, highcut], btype='band', analog=False, output='sos', fs=Fs)
    return sos


def butter_bandpass_filter(x, lowcut, highcut, Fs, order=10):
    """Application of bandpass filter on signal
                Args:
                    x (ndarray): Signal to bandpass
                    lowcut (float): lowest frequency at with bandpass gain is -3dB
                    highcut (float): highest frequency at with bandpass gain is -3dB
                    Fs (float): sampling frequency
                Returns:
                    y (ndarray): Signal after applying bandpass filter
        """
    sos = butter_bandpass(lowcut, highcut, Fs, order=order)
    y = sp.signal.sosfilt(sos, x)
    return y


def find_nearest(array, value):
    """Function to get closest value from array
                Args:
                    array (ndarray): array of values to analyze
                    value (float): value to find closest number in array
                Returns:
                    array[index] (int): Index of closest value found in array
    """
    array = np.asarray(array)
    index = (np.abs(array - value)).argmin()
    return array[index]


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


def extract_partial(x, nOfPartial, Fs, fundFreq):
    """Isolation of a signal's partial and Extraction of its Magnitude Envelope
    Args:
        x (np.ndarray): Signal (waveform) to be analyzed
        nOfPartial (int): Harmonic multiplier of Fundamental Frequency
        Fs (scalar): Sampling rate

    Returns:
        partial (np.ndarray): Partial signal (waveform)
    """
    partialFreq = fundFreq * nOfPartial
    print(nOfPartial)
    lowcut = partialFreq - partialFreq/20
    highcut = partialFreq + partialFreq/20
    if highcut < Fs/2:
        partial = butter_bandpass_filter(x, lowcut, highcut, Fs)
        analytic_partial = sp.signal.hilbert(partial)
        partial_envelope = np.abs(analytic_partial)
        np.save(str(int(round(fundFreq))) + 'PianoPartial' + str(nOfPartial) + '.npy', partial_envelope)
        return partial_envelope
    else:
        return


class AdditiveSynthesis(SynthesisTemplate):
    def __init__(self):
        super().__init__()
        self.Fs = 44100 # Frecuencia de sampleo
        self.note_frequencies = [65.41, 130.81, 261.63, 523.25, 1046.50] # Frecuencias de los parciales cargados
        self.note_frequencies_round = [65, 131, 262, 523, 1046] # Frecuencias redondeadas(para acceder al archivo)
        self.song = [] # Array representando la cancion

    def synthesize_note(self, note):
        """Synthetization of a Single Midi Note
        Args:
            note (Note): Note object to synthesize
        Returns:
            Nothing
        """
        freq_used = find_nearest(self.note_frequencies, note.frequency) # Agarro como frecuencia la mas cercana de las cargadas
        nearest_round = find_nearest(self.note_frequencies_round, freq_used) # Ademas agarro la redondeada para cargar los archivos
        partials_sum = 0 # Inicializo la variable de suma de parciales
        n_of_partials = 35 # Numero de parciales cargados en memoria
        if freq_used == 1046.5: # Si la frecuencia elegida fue C6, tengo menos parciales (limite por Fs=44100)
            n_of_partials = 20
        for i in range(n_of_partials): # Recorro todos los parciales
            partial_i = np.load(
                'src\\backend\\synthesis\\PianoPartialsNPY\\' + str(
                    nearest_round) + 'PianoPartial' + str(i + 1) + '.npy') # Cargo el parcial actual
            factor_of_stretch = ((note.end - note.start) * self.Fs) / len(partial_i) # Veo por cuanto lo debo estirar o comprimir (segun el tiempo de la nota)
            if factor_of_stretch == 0: # Si ocurre esto la nota no tiene duracion(para evitar errores)
                return
            partial_domain = np.linspace(0, 1, len(partial_i)) # Obtengo un dominio lineal del parcial cargado
            stretched_domain = np.linspace(0, 1, int(round(len(partial_i) * factor_of_stretch))) # Obtengo el dominio lineal equivalente del parcial estirado
            stretched_partial_i = np.interp(stretched_domain, partial_domain, partial_i) # Interpolo para realizar el estiramiento/la compresion
            time_domain = np.arange(len(stretched_partial_i)) / self.Fs # Paso del dominio discreto al continuo en el tiempo para los senos
            partials_sum = partials_sum + stretched_partial_i * np.sin(2 * (i + 1) * np.pi * freq_used * time_domain) # Multiplico la envolvente del parcial por su seno correspondiente

        n_of_semitones = math.log(note.frequency/freq_used, 2**(1/12)) # Calculo la distancia en semitonos de la nota a sintonizar y la nota cargada en memoria
        partials_sum = librosa.effects.pitch_shift(partials_sum, self.Fs, n_of_semitones) # Acerco la frecuencia de la nota cargada a la que se debe sintonizar

        for i in range(int(math.floor((note.end - note.start) * self.Fs))): # Recorro en la cancion el rango de la nota
            current_index = int(math.floor(note.start * self.Fs) + i) # Index para simplificar el recorrido
            self.song[current_index] = self.song[current_index] + note.velocity * partials_sum[i] # Sumo en las posiciones correspondientes el resultado de la suma de los parciales por la velocity de la nota
        return

    def synthesize_audio_track(self, track: Track, instrument: INSTRUMENT):
        """Synthetization of a Single Midi Note
                Args:
                    track (Track): Track object with the Notes to synthesize
                    instrument (INSTRUMENT): Instrument to synthesize (Only PIANO for now)
                Returns:
                    Nothing
                """
        super().synthesize_audio_track(track, instrument)
        if self.instrument != INSTRUMENT.PIANO: # Si no quiero sintetizar un piano da error
            self.state = STATE.ERROR
        else:
            song_end = 0 # Inicializo la variable que me indica el final de la cancion
            for i in track:
                if i.end > song_end: # Obtengo el final de la cancion viendo que nota finaliza ultima
                    song_end = i.end
            self.song = np.zeros(int(math.ceil(song_end * self.Fs))) # Inicializo el arreglo de la cancion con ceros

            for i in track: # Sintetizo todas las notas del track dado en la cancion
                self.synthesize_note(i)

            max_velocity = 0
            for i in range(len(self.song)): # Calculo el volumen maximo de la cancion en un instante
                if self.song[i] > max_velocity:
                    max_velocity = self.song[i]
            self.song = self.song/max_velocity # Normalizo la cancion segun su volumen maximo
            self.state = STATE.LOADED # Indico que termine la carga de la cancion