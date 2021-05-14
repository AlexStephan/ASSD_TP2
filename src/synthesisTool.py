from Lib.random import random, seed

# Qt Modules
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog,QWidget, QGridLayout,QPushButton, QApplication, QLabel, QCheckBox,QFileDialog
from src.ui.gui import Ui_Form

# Matplotlib Modules
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
#from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

# Python Modules
import numpy as np
import scipy.signal as ss
from scipy import signal as ssignal
from scipy import special
from enum import Enum
import array as arr
import csv

# SymPy modules

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
from sympy import I

# ?
import math
import os
from typing import Callable,List
from matplotlib.mlab import window_hanning,window_none

# !!!
import sounddevice as sd
import functools

# my modules!!!
from src.backend.tracks.track import Track,TrackGroup

from src.backend.midi2tracks import Midi2Tracks
from src.backend.audio_tracks.audio_track import AudioTrack

from resources.testing_code.audio_loader import load_wav_file
from src.backend.saver.audio_saver import AudioSaver
#from resources.testing_code.player_test import callback_sound_test

from src.backend.instruments.instrument_list import INSTRUMENT
from src.backend.synthesis.synthesis_template import SynthesisTemplate
from src.backend.synthesis.physical_modelling_synthesis import PhysicalModellingSynthesis
from src.backend.synthesis.additive_synthesis import AdditiveSynthesis
from src.backend.synthesis.sample_based_synthesis import SampleBasedSynthesis

from src.backend.spectrum.audiotrack2spectrum import blackman,bartlett,hamming,blackmanharris

from src.backend.audio_tracks.audio_constants import sample_rate

#global test_audio_track
#global position_in_audio

from src.backend.effects.effect_list import eco,simple_reverb,flanger

class STATE_SYNTH(Enum):
    EMPTY = 0
    LOADED = 1
    SYNTHESIZED = 2
    PLAYING = 3
    ERROR = 4

class WINDOW_SELECT(Enum):
    NONE = 0
    BARTLETT = 1
    HANNING = 2
    HAMMING = 3
    BLACKMAN = 4
    BLACKMAN_HARRIS = 5


class EffectData(object):
    def __init__(self,fun:Callable = None,var1:list = None,var2:list = None):
        self.fun = fun
        self.var1 = var1
        self.var2 = var2


EffectsFromTrack = List[EffectData]


AllEffects = List[EffectsFromTrack]


class SynthesisTool(QWidget,Ui_Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("TP GRUPAL 1 - Sampleo - ASSD")
        self.setWindowIcon(QtGui.QIcon('py.png'))

        self.__init_objects()
        self.__setCallbacks()

        #self.synthesis_timer = QTimer()
        #self.synthesis_timer.timeout.connect(self.__CB_synthesis_timer_step)
        #self.audio_loader = AudioLoader()
        #self.audio_saver = AudioSaver()
        #global test_audio_track
        #test_audio_track = AudioTrack()
        #self.output_stream = sd.OutputStream(channels=2,callback=self.__callback_sound_test,blocksize=1024,dtype='int16')#1024)
        #global position_in_audio
        #position_in_audio = 0

        #self.pushButton_spectrogram_plot.clicked.connect(self.test)

        self.testingvar = 0

        self.initIcons()

    def __init_objects(self):
        self.midi2tracks = Midi2Tracks()
        self.trackgroup = []
        self.errorBox = QtWidgets.QMessageBox()

        self.track_frames = []
        self.track_frames_spectrogram = []

        self.additive_synth = AdditiveSynthesis()
        self.physical_synth = PhysicalModellingSynthesis()
        self.sample_synth = SampleBasedSynthesis()

        self.audiotrackgroup = []

        self.__change_state_synth(STATE_SYNTH.EMPTY)

        self.audio_saver = AudioSaver()

        self.__init_graphs()

        self.output_stream = sd.OutputStream(channels=1, callback=self.__callback_sound_player, blocksize=1024,
                                             dtype='int16')

        self.unfiltered_mix = np.array([])
        self.current_position = 0

        self.aux_index = 0

        self.all_effects = []
        self.current_visible_effects = []

        self.selected_track = 0

    def __init_graphs(self):
        self.figure_spectrum = Figure()
        self.canvas_spectrum = FigureCanvas(self.figure_spectrum)
        self.index_spectrum = self.stackedWidget_spectrogram.addWidget(self.canvas_spectrum)
        self.stackedWidget_spectrogram.setCurrentIndex(self.index_spectrum)
        self.toolbar_spectrum = NavigationToolbar(self.canvas_spectrum,self)
        self.horizontalLayout_spectrogram_plotSettings.addWidget(self.toolbar_spectrum)
        self.axis_spectrum = self.figure_spectrum.add_subplot()

    def __setCallbacks(self):
        self.radioButton_singleNotes_selectNoteByFrequency.clicked.connect(self.__CB_radioButton_selectNoteByFrequency)
        self.__CB_radioButton_selectNoteByFrequency()

        self.pushButton_synthesize_loadFile.clicked.connect(self.__CB_open_midi_file)
        self.pushButton_synthesize_synthesize.clicked.connect(self.__CB_synthesize)
        self.pushButton_synthesize_save.clicked.connect(self.__CB_save)

        self.pushButton_spectrogram_selectAll.clicked.connect(self.__CB_select_all_spectrogram)
        self.pushButton_spectrogram_deselectAll.clicked.connect(self.__CB_deselect_all_spectrogram)

        self.pushButton_spectrogram_plot.clicked.connect(self.__CB_plot_spectrogram)

        self.pushButton_synthesize_play_pause.clicked.connect(self.__CB_synthesis_timer_play_pause)
        self.pushButton_synthesize_stop.clicked.connect(self.__CB_synthesis_timer_stop)
        self.pushButton_synthesize_back.clicked.connect(self.__CB_replay_back)
        self.pushButton_synthesize_foward.clicked.connect(self.__CB_replay_forward)

        self.comboBox_synthesize_selectEffectType.currentIndexChanged.connect(self.__CB_changed_effect_creator_selection)
        self.pushButton_synthesize_addEffect.clicked.connect(self.__CB_add_effect)

    #def __CB_synthesis_timer_step(self):
    #    print("Synthesis timer step!")

    def __CB_replay_forward(self):
        if self.state_synth == STATE_SYNTH.SYNTHESIZED or self.state_synth == STATE_SYNTH.PLAYING:
            if len(self.unfiltered_mix) >0:
                self.current_position = self.current_position+sample_rate*5
                if self.current_position > len(self.unfiltered_mix):
                    self.current_position = len(self.unfiltered_mix)
        else:
            self.__error_message("Replay back and forward only available once synthesized")


    def __CB_replay_back(self):
        if self.state_synth == STATE_SYNTH.SYNTHESIZED or self.state_synth == STATE_SYNTH.PLAYING:
            if len(self.unfiltered_mix) >0:
                self.current_position = self.current_position-sample_rate*5
                if self.current_position < 0:
                    self.current_position = 0
        else:
            self.__error_message("Replay back and forward only available once synthesized")

    def __CB_add_effect(self):
        print("ADD EFFECT")
        if self.comboBox_synthesize_selectEffectType.currentIndex() == 1:
            fun = eco
        elif self.comboBox_synthesize_selectEffectType.currentIndex() == 2:
            fun = simple_reverb
        elif self.comboBox_synthesize_selectEffectType.currentIndex() == 3:
            fun = flanger
        else:
            self.__error_message("Invalid index at Add effect")
            return
        var1 = [0]
        var2 = [0]
        new_effect = EffectData(fun,var1,var2)
        self.all_effects[self.selected_track].append(new_effect)
        self.__CB_select_track_to_see_effects(self.selected_track)

    def __CB_synthesis_timer_play_pause(self):
        print("Synthesis timer play pause!")
        if self.state_synth == STATE_SYNTH.SYNTHESIZED:
            unfiltered_mix = self.__get_unfiltered_mix().content
            max = np.amax(np.abs(unfiltered_mix))
            streaming_mix = np.multiply(unfiltered_mix, ((2 ** 15) - 1) / max)

            self.unfiltered_mix = np.array(streaming_mix)
            self.output_stream.start()
            self.__change_state_synth(STATE_SYNTH.PLAYING)
        elif self.state_synth == STATE_SYNTH.PLAYING:
            self.__change_state_synth(STATE_SYNTH.SYNTHESIZED)
            self.output_stream.stop()
        else:
            self.__error_message("Playing/Pausing not available until synthesization")

    def __CB_changed_effect_creator_selection(self):
        if self.comboBox_synthesize_selectEffectType.currentIndex() > 0:
            self.pushButton_synthesize_addEffect.setDisabled(False)
        else:
            self.pushButton_synthesize_addEffect.setDisabled(True)


    def __CB_synthesis_timer_stop(self):
        print("Synthesis timer stop")
        self.__change_state_synth(STATE_SYNTH.SYNTHESIZED)
        self.output_stream.stop()
        self.current_position = 0

    def __CB_radioButton_selectNoteByFrequency(self):
        checked = self.radioButton_singleNotes_selectNoteByFrequency.isChecked()
        self.label_singleNotes_frequency.setVisible(checked)
        self.doubleSpinBox_singleNotes_frequency.setVisible(checked)
        self.label_singleNotes_note.setVisible(not checked)
        self.comboBox_singleNotes_note.setVisible(not checked)
        self.label_singleNotes_octave.setVisible(not checked)
        self.comboBox_singleNotes_octave.setVisible(not checked)

    def initIcons(self):
        scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.pushButton_synthesize_play_pause.setIcon(QtGui.QIcon(scriptDir+os.path.sep+"..\\resources\\icons\\symbol-play.png"))
        self.pushButton_synthesize_stop.setIcon(QtGui.QIcon(scriptDir+os.path.sep+"..\\resources\\icons\\symbol-stop.png"))
        self.pushButton_synthesize_back.setIcon(QtGui.QIcon(scriptDir+os.path.sep+"..\\resources\\icons\\symbol-back.png"))
        self.pushButton_synthesize_foward.setIcon(QtGui.QIcon(scriptDir+os.path.sep+"..\\resources\\icons\\symbol-foward.png"))

        self.pushButton_synthesize_loadFile.setIcon(QtGui.QIcon(scriptDir + os.path.sep + "..\\resources\\icons\\symbol-file.png"))

        self.pushButton_singleNotes_play.setIcon(QtGui.QIcon(scriptDir + os.path.sep + "..\\resources\\icons\\symbol-play.png"))
        self.pushButton_singleNotes_trashcan.setIcon(QtGui.QIcon(scriptDir + os.path.sep + "..\\resources\\icons\\symbol-trashcan.png"))

        #self.pushButton_synthesize_foward.setDisabled(True)

    def create_synthesis_track_box(self,new_frame_name,numberOfTrack):
        new_frame = QtWidgets.QFrame(self.tab_synthesis)
        new_frame.setMinimumSize(QtCore.QSize(200,100))
        new_frame.setMaximumSize(QtCore.QSize(200,100))
        new_frame.setFrameShape(QtWidgets.QFrame.Box)
        new_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        new_frame.setObjectName(new_frame_name)

        new_VLayout = QtWidgets.QVBoxLayout(new_frame)
        new_VLayout.setObjectName("VLayout_"+new_frame_name)

        new_HLayout = QtWidgets.QHBoxLayout()
        new_HLayout.setObjectName("HLayout_"+new_frame_name)

        new_label = QtWidgets.QLabel(new_frame)
        new_label.setObjectName("Label_"+new_frame_name)
        new_label.setText("Track {0}".format(numberOfTrack))
        new_HLayout.addWidget(new_label)

        new_button = QtWidgets.QPushButton(new_frame)
        new_button.setObjectName("Button_"+new_frame_name)
        new_button.setText("Select")
        new_HLayout.addWidget(new_button)

        new_radioButton = QtWidgets.QRadioButton(new_frame)
        new_radioButton.setObjectName("RadioButton_"+new_frame_name)
        new_radioButton.setText("Mute")
        new_HLayout.addWidget(new_radioButton)

        new_VLayout.addLayout(new_HLayout)

        new_HSlider = QtWidgets.QSlider(new_frame)
        new_HSlider.setOrientation(QtCore.Qt.Horizontal)
        new_HSlider.setObjectName("Slider_"+new_frame_name)
        new_HSlider.setRange(0,99)
        new_HSlider.setValue(99)
        new_VLayout.addWidget(new_HSlider)

        new_comboBox = QtWidgets.QComboBox(new_frame)
        new_comboBox.setObjectName("ComboBox_"+new_frame_name)
        new_comboBox.addItem("")
        new_comboBox.addItem("")
        new_comboBox.addItem("")
        new_VLayout.addWidget(new_comboBox)

        self.verticalLayout_synthesis_trackList.addWidget(new_frame)

    def create_synthesis_effect_box(self,new_frame_name,newEffectName,newExtraData):
        new_frame = QtWidgets.QFrame(self.tab_synthesis)
        #new_frame.setMinimumSize(QtCore.QSize(200,100))
        new_frame.setMaximumSize(QtCore.QSize(16777215,90))
        new_frame.setFrameShape(QtWidgets.QFrame.Box)
        new_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        new_frame.setObjectName(new_frame_name)

        new_VLayout = QtWidgets.QVBoxLayout(new_frame)
        new_VLayout.setObjectName("VLayout_" + new_frame_name)

        new_HLayout = QtWidgets.QHBoxLayout()
        new_HLayout.setObjectName("HLayout_" + new_frame_name)

        new_Xbutton = QtWidgets.QPushButton(new_frame)
        new_Xbutton.setMinimumSize(QtCore.QSize(24,24))
        new_Xbutton.setMaximumSize(QtCore.QSize(24, 24))
        new_Xbutton.setObjectName("XButton_" + new_frame_name)
        new_Xbutton.setText("X")
        new_HLayout.addWidget(new_Xbutton)

        new_label = QtWidgets.QLabel(new_frame)
        new_label.setObjectName("Label_" + new_frame_name)
        new_label.setText(newEffectName)
        new_HLayout.addWidget(new_label)

        new_button = QtWidgets.QPushButton(new_frame)
        new_Xbutton.setMaximumSize(QtCore.QSize(60, 16777215))
        new_button.setObjectName("Button_" + new_frame_name)
        new_button.setText("Select")
        new_HLayout.addWidget(new_button)

        new_VLayout.addLayout(new_HLayout)

        new_extralabel = QtWidgets.QLabel(new_frame)
        new_extralabel.setObjectName("ExtraLabel_" + new_frame_name)
        new_extralabel.setText(newExtraData)
        new_VLayout.addWidget(new_extralabel)

        self.verticalLayout_synthesis_effectList.addWidget(new_frame)

    def create_spectrogram_track_box(self,new_frame_name,numberOfTrack):
        new_frame = QtWidgets.QFrame(self.scrollAreaWidgetContents_5)
        new_frame.setMaximumSize(QtCore.QSize(16777215, 45))
        new_frame.setFrameShape(QtWidgets.QFrame.Box)
        new_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        new_frame.setObjectName(new_frame_name)
        new_HLayout = QtWidgets.QHBoxLayout(new_frame)
        new_HLayout.setObjectName("HLayout_"+new_frame_name)
        new_label = QtWidgets.QLabel(new_frame)
        new_label.setObjectName("Label_"+new_frame_name)
        new_label.setText("Track {0}".format(numberOfTrack))
        new_HLayout.addWidget(new_label)
        new_radioButton = QtWidgets.QRadioButton(new_frame)
        new_radioButton.setMaximumSize(QtCore.QSize(16, 16))
        new_radioButton.setText("")
        new_radioButton.setObjectName("RadioButton_"+new_frame_name)
        new_HLayout.addWidget(new_radioButton)
        self.verticalLayout_spectrogram_trackList.addWidget(new_frame)

    def test_sound(self):
        global test_audio_track
        global position_in_audio
        self.output_stream.stop()

        position_in_audio = 0
        is_ok,samplerate,audio_track_group= load_wav_file(".\\resources\\wav_files\\Level Music 1.wav")

        print("is_ok = {}".format(is_ok))
        print("samplerate = {}".format(samplerate))
        print("number of channels = {}".format(audio_track_group.shape[1]))
        print("length = {} samples, or {} secs".format(audio_track_group.shape[0],(audio_track_group.shape[0])/samplerate))
        test_audio_track = AudioTrack()
        test_audio_track.content = audio_track_group
        #test_audio_track.content.reshape(audio_track_group.shape[0])
        print(test_audio_track)

        self.audio_saver.save_wav_file(test_audio_track, ".\\resources\\wav_files\\Level Music 1_copied.wav")
        self.output_stream.start()

    def test_midi(self):
        self.midi2tracks.load_midi_file("resources\\midi_files\\Concierto-De-Aranjuez.mid")
        valid = self.midi2tracks.is_valid()
        print(valid)
        if valid:
            tracks = self.midi2tracks.get_array_of_tracks()
            for n,channel in enumerate(tracks):
                print("\n\n\nCHANNEL {}\n".format(n))
                for note in channel:
                    print("Note:")
                    print("Start = {}".format(note.start))
                    print("End = {}".format(note.end))
                    print("Velocity = {}".format(note.velocity))
                    print("Number = {}".format(note.number))
                    print("Frequency = {}".format(note.frequency))
                    print("")
        return

    def test(self):
        print("test")
        if self.testingvar == 0:
            self.create_synthesis_track_box("nombre",99)
            self.create_synthesis_effect_box("framename","Echo","Extra data goes here")
            self.create_spectrogram_track_box("nombrecito",999)

        elif self.testingvar == 2:
            self.testingvar = 1 #!!!
            self.frame__1 = QtWidgets.QFrame(self.tab_synthesis)
            self.frame__1.setMinimumSize(QtCore.QSize(100,100))
            self.frame__1.setMaximumSize(QtCore.QSize(100,100))
            self.frame__1.setFrameShape(QtWidgets.QFrame.Box)
            self.frame__1.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame__1.setObjectName("frame__1")
            self.verticalLayout_synthesis_trackList.addWidget(self.frame__1)

            self.verticalLayout__1=QtWidgets.QVBoxLayout(self.frame__1)
            self.verticalLayout__1.setObjectName("verticalLayout__1")

            self.pushButton__1 = QtWidgets.QPushButton(self.tab_synthesis)
            self.pushButton__1.setMinimumSize(QtCore.QSize(40,40))
            self.pushButton__1.setMaximumSize(QtCore.QSize(40, 40))
            self.pushButton__1.setText("")
            self.pushButton__1.setObjectName("pushButton__1")
            self.verticalLayout__1.addWidget(self.pushButton__1)

            self.pushButton__2 = QtWidgets.QPushButton(self.tab_synthesis)
            self.pushButton__2.setMinimumSize(QtCore.QSize(40,40))
            self.pushButton__2.setMaximumSize(QtCore.QSize(40, 40))
            self.pushButton__2.setText("")
            self.pushButton__2.setObjectName("pushButton__2")
            self.verticalLayout__1.addWidget(self.pushButton__2)
        else:
            self.testingvar = 0

            self.verticalLayout__1.removeWidget(self.pushButton__1)
            self.pushButton__1.deleteLater()
            self.pushButton__1 = None
            self.verticalLayout__1.removeWidget(self.pushButton__2)
            self.pushButton__2.deleteLater()
            self.pushButton__2 = None

            self.verticalLayout__1.deleteLater()
            self.verticalLayout__1 = None

            self.verticalLayout_synthesis_trackList.removeWidget(self.frame__1)
            self.frame__1.deleteLater()
            self.frame__1 = None


        # if self.testingvar == 0:
        #
        #     self.pushButton_test = QtWidgets.QPushButton(self.tab_synthesis)
        #     self.pushButton_test.setMinimumSize(QtCore.QSize(40,40))
        #     self.pushButton_test.setMaximumSize(QtCore.QSize(40,40))
        #     self.pushButton_test.setText("TEST!")
        #     self.pushButton_test.setObjectName("pushButton_test")
        #     self.horizontalLayout_synthesis_trackList.addWidget(self.pushButton_test)
        #
        #     self.testingvar += 1
        # elif self.testingvar == 1:
        #     self.horizontalLayout_synthesis_trackList.removeWidget(self.pushButton_test)
        #     self.pushButton_test.deleteLater()
        #     self.pushButton_test = None
        #     self.testingvar += 1
        #
        #     self.pushButton_test = QtWidgets.QPushButton(self.tab_synthesis)
        #     self.pushButton_test.setMinimumSize(QtCore.QSize(40,40))
        #     self.pushButton_test.setMaximumSize(QtCore.QSize(40,40))
        #     self.pushButton_test.setText("T2!")
        #     self.pushButton_test.setObjectName("pushButton_test")
        #     self.horizontalLayout_synthesis_trackList.addWidget(self.pushButton_test)
        #
        #     self.pushButton_test2 = QtWidgets.QPushButton(self.tab_synthesis)
        #     self.pushButton_test2.setMinimumSize(QtCore.QSize(40,40))
        #     self.pushButton_test2.setMaximumSize(QtCore.QSize(40,40))
        #     self.pushButton_test2.setText("T2!")
        #     self.pushButton_test2.setObjectName("pushButton_test2")
        #     self.horizontalLayout_synthesis_trackList.addWidget(self.pushButton_test2)
        # else:
        #     self.testingvar = 0
        #     self.horizontalLayout_synthesis_trackList.removeWidget(self.pushButton_test)
        #     self.pushButton_test.deleteLater()
        #     self.pushButton_test = None
        #     self.horizontalLayout_synthesis_trackList.removeWidget(self.pushButton_test2)
        #     self.pushButton_test2.deleteLater()
        #     self.pushButton_test2 = None

    def __callback_sound_player(self,outdata: np.ndarray, frames: int, time, status):
        #global position_in_audio
        #global test_audio_track

        #outdata[:] = test_audio_track.content[position_in_audio:(position_in_audio+frames)]
        #position_in_audio = position_in_audio+frames
        #print(f"frames = {frames}")
        if self.current_position >= len(self.unfiltered_mix):
            #self.output_stream.close()
            print("STOPPED!")
            self.__CB_synthesis_timer_stop()
        elif self.current_position + frames - 1 >= len(self.unfiltered_mix):
            outdata[:] = np.int16(np.reshape(np.pad(self.unfiltered_mix[self.current_position:],
                                (0,self.current_position + frames-len(self.unfiltered_mix))),(frames,1)))
            self.current_position = len(self.unfiltered_mix)
        else:
            outdata[:] = np.int16(np.reshape(self.unfiltered_mix[self.current_position:self.current_position+frames],(frames,1)))
            self.current_position = self.current_position + frames

    def __CB_plot_spectrogram(self):
        selected = []
        for i,trackframe in enumerate(self.track_frames_spectrogram):
            if trackframe[3].isChecked():
                selected.append(i)
        if len(selected) == 0:
            self.__error_message("Select at least 1 track to plot")
        else:
            lengths = []
            for i in selected:
                lengths.append(len(self.audiotrackgroup[i].content))
            max_lenght = max(lengths)

            mix = np.zeros(max_lenght)
            for i in selected:
                audiotrack = self.audiotrackgroup[i]
                partial = np.pad(audiotrack.content,(0,max_lenght-len(audiotrack.content)))
                normalized = np.divide(partial, np.amax(np.abs(partial)))
                weighted = np.multiply(normalized,self.__get_velocity_selected(i)/127)
                mix = mix + weighted

            NFFT,Fs,noverlap,window = self._get_spectrum_data()
            self.__clear_spectrogram()

            beggining = self.doubleSpinBox_spectrogram_intTime.value()*sample_rate
            if self.doubleSpinBox_spectrogram_duration.value() == 0:
                finalmix = np.array(mix[beggining:])
            else:
                end = beggining + self.doubleSpinBox_spectrogram_duration.value()*sample_rate
                finalmix = np.array(mix[beggining:end])

            Pxx,freqs,bins,im = self.axis_spectrum.specgram(finalmix,NFFT=NFFT,Fs=Fs,noverlap=noverlap,window=window)

            #f, t, Sxx =ssignal.spectrogram(mix,sample_rate)
            #self.axis_spectrum.pcolormesh(t,f,Sxx)
            #self.axis_spectrum.set_ylabel('Frequency [Hz]')
            #self.axis_spectrum.set_xlabel('Time [s]')

            self.canvas_spectrum.draw()

    def _get_spectrum_data(self):
        NFFT = self.spinBox_spectrogram_NFFT.value()
        overlap = self.spinBox_spectrogram_overlap.value()
        Fs = sample_rate
        window_index = self.comboBox_spectrogram_window.currentIndex()
        if window_index == WINDOW_SELECT.NONE.value:
            window = window_none
        elif window_index == WINDOW_SELECT.BARTLETT.value:
            window = bartlett
        elif window_index == WINDOW_SELECT.HANNING.value:
            window = window_hanning
        elif window_index == WINDOW_SELECT.HAMMING.value:
            window = hamming
        elif window_index == WINDOW_SELECT.BLACKMAN.value:
            window = blackman
        elif window_index == WINDOW_SELECT.BLACKMAN_HARRIS.value:
            window = blackmanharris

        return [NFFT,Fs,overlap,window]

    def __clear_spectrogram(self):
        self.axis_spectrum.clear()
        self.axis_spectrum.grid()
        self.canvas_spectrum.draw()
        self.axis_spectrum.set_title("Spectrum Analysis")
        self.axis_spectrum.set_xlabel("Time [s]")
        self.axis_spectrum.set_ylabel("Frequency [Hz]")

    def __CB_select_all_spectrogram(self):
        for trackframe in self.track_frames_spectrogram:
            trackframe[3].setChecked(True)

    def __CB_deselect_all_spectrogram(self):
        for trackframe in self.track_frames_spectrogram:
            trackframe[3].setChecked(False)

    def __CB_open_midi_file(self):
        filename = QFileDialog.getOpenFileName(self,"Select MIDI file",'c:\\',"MIDI file (*.mid);;MIDI file (*.midi)")
        print(filename)
        if filename[0] != "":
            if self.midi2tracks.load_midi_file(filename[0]):
                self.__delete_old_tracks_frames()
                self.__create_new_tracks_frames()
                self.__change_state_synth(STATE_SYNTH.LOADED)
            else:
                self.__error_message("Couldn't open file!")
                self.__change_state_synth(STATE_SYNTH.ERROR)

    def __delete_old_tracks_frames(self):
        for trackframe in self.track_frames:
            self.__delete_single_track_frame_in_synthesis(trackframe)
        for trackframe in self.track_frames_spectrogram:
            self.__delete_single_track_frame_in_spectrogram(trackframe)
        self.track_frames = []
        self.track_frames_spectrogram = []

    def __delete_single_track_frame_in_spectrogram(self,trackframe:list):
        [old_frame, old_HLayout, old_label, old_radioButton] = trackframe

        old_HLayout.removeWidget(old_radioButton)
        old_radioButton.deleteLater()

        old_HLayout.removeWidget(old_label)
        old_label.deleteLater()

        old_HLayout.deleteLater()

        self.verticalLayout_spectrogram_trackList.removeWidget(old_frame)
        old_frame.deleteLater()

    def __delete_single_track_frame_in_synthesis(self,trackframe:list):
        [old_frame,old_VLayout,old_HLayout,
         old_label,old_button,old_radioButton,
         old_HSlider,old_comboBox] = trackframe

        old_VLayout.removeWidget(old_comboBox)
        old_comboBox.deleteLater()

        old_VLayout.removeWidget(old_HSlider)
        old_HSlider.deleteLater()

        old_HLayout.removeWidget(old_label)
        old_label.deleteLater()

        old_HLayout.removeWidget(old_button)
        old_button.deleteLater()

        old_HLayout.removeWidget(old_radioButton)
        old_radioButton.deleteLater()

        old_HLayout.deleteLater()

        old_VLayout.deleteLater()

        self.verticalLayout_synthesis_trackList.removeWidget(old_frame)
        old_frame.deleteLater()

    def __create_new_tracks_frames(self):
        self.trackgroup = self.midi2tracks.get_array_of_tracks()
        for track in range(len(self.trackgroup)):
            self.track_frames.append(self.__create_single_track_frame_in_synthesis(track+1))
            self.track_frames_spectrogram.append(self.__create_single_track_frame_in_spectrogram(track+1))
        return

    def __create_single_effect_frame(self, fun: Callable, value1, value2) -> list:
        new_frame_name = f"NewFrameEffect_{self.aux_index}"
        self.aux_index = self.aux_index +1

        new_frame = QtWidgets.QFrame(self.tab_synthesis)
        new_frame.setMaximumSize(QtCore.QSize(16777215, 200))
        new_frame.setFrameShape(QtWidgets.QFrame.Box)
        new_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        new_frame.setObjectName(new_frame_name)

        new_VLayout = QtWidgets.QVBoxLayout(new_frame)
        new_VLayout.setObjectName("V_"+new_frame_name)

        new_superiorHLayout = QtWidgets.QHBoxLayout()
        new_superiorHLayout.setObjectName("Hs_"+new_frame_name)
        new_VLayout.addLayout(new_superiorHLayout)

        new_button = QtWidgets.QPushButton(new_frame)
        new_button.setObjectName("Button_"+new_frame_name)
        new_button.setMaximumSize(QtCore.QSize(24,24))
        new_button.setMinimumSize(QtCore.QSize(24, 24))
        new_button.setText("X")
        new_superiorHLayout.addWidget(new_button)

        if fun == eco:
            label_text = "Eco"
            param1 = "Delay (usec)"
            range1 = [0,10000]
            param2 = "Intensity (%)"
            range2 = [0,100]
        elif fun == simple_reverb:
            label_text = "Simple Reverberation"
            param1 = "Delay (usec)"
            range1 = [0,10000]
            param2 = "Intensity (%)"
            range2 = [0,100]
        else:
            label_text = "Simple Reverberation"
            param1 = "f0 (Hz)"
            range1 = [0,10000]
            param2 = "k (%)"
            range2 = [0,100]

        new_label = QtWidgets.QLabel(new_frame)
        new_label.setObjectName("Label_"+new_frame_name)
        new_label.setText(label_text)
        new_superiorHLayout.addWidget(new_label)

        #
        #

        new_inferiorHLayout = QtWidgets.QHBoxLayout()
        new_inferiorHLayout.setObjectName("Hi_" + new_frame_name)
        new_VLayout.addLayout(new_inferiorHLayout)

        #

        new_leftVLayout = QtWidgets.QVBoxLayout()
        new_leftVLayout.setObjectName("Left"+new_frame_name)
        new_inferiorHLayout.addLayout(new_leftVLayout)

        new_labelL = QtWidgets.QLabel(new_frame)
        new_labelL.setObjectName("LabelL_"+new_frame_name)
        new_labelL.setText(param1)
        new_leftVLayout.addWidget(new_labelL)

        new_dialL = QtWidgets.QDial(new_frame)
        new_dialL.setObjectName("DialL"+new_frame_name)
        new_dialL.setRange(range1[0],range1[1])
        new_dialL.setValue(value1[0])
        new_dialL.valueChanged.connect(functools.partial(self.__CB_connection, value1, new_dialL.value()))
        new_leftVLayout.addWidget(new_dialL)

        new_lcdL = QtWidgets.QLCDNumber(new_frame)
        new_lcdL.setObjectName("LCDL"+new_frame_name)
        new_dialL.valueChanged.connect(functools.partial(self.__CB_dial_to_lcd,[new_lcdL],new_dialL.value()))
        new_leftVLayout.addWidget(new_lcdL)

        #

        new_rightVLayout = QtWidgets.QVBoxLayout()
        new_rightVLayout.setObjectName("Right"+new_frame_name)
        new_inferiorHLayout.addLayout(new_rightVLayout)

        new_labelR = QtWidgets.QLabel(new_frame)
        new_labelR.setObjectName("LabelR_"+new_frame_name)
        new_labelR.setText(param2)
        new_rightVLayout.addWidget(new_labelR)

        new_dialR = QtWidgets.QDial(new_frame)
        new_dialR.setObjectName("DialR"+new_frame_name)
        new_dialR.setRange(range2[0],range2[1])
        new_dialR.setValue(value2[0])
        new_dialR.valueChanged.connect(functools.partial(self.__CB_connection,value2,new_dialR.value()))
        new_rightVLayout.addWidget(new_dialR)

        new_lcdR = QtWidgets.QLCDNumber(new_frame)
        new_lcdR.setObjectName("LCDR"+new_frame_name)
        new_dialR.valueChanged.connect(functools.partial(self.__CB_dial_to_lcd,[new_lcdR], new_dialR.value()))
        new_rightVLayout.addWidget(new_lcdR)

        self.verticalLayout_synthesis_effectList.addWidget(new_frame)

        return [new_frame, new_VLayout, new_superiorHLayout, new_button, new_label,
                new_inferiorHLayout,
                new_leftVLayout,new_labelL,new_dialL,new_lcdL,
                new_rightVLayout,new_labelR,new_dialR,new_lcdR]

    def __create_single_track_frame_in_spectrogram(self, track_number: int) -> list:
        new_frame_name = f"NewFrame_{track_number}"

        new_frame = QtWidgets.QFrame(self.tab_synthesis)
        new_frame.setMaximumSize(QtCore.QSize(200,45))
        new_frame.setFrameShape(QtWidgets.QFrame.Box)
        new_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        new_frame.setObjectName(new_frame_name)

        new_HLayout = QtWidgets.QHBoxLayout(new_frame)
        new_HLayout.setObjectName("HLayout_"+new_frame_name)

        new_label = QtWidgets.QLabel(new_frame)
        new_label.setObjectName("Label_"+new_frame_name)
        new_label.setText("Track {0}".format(track_number))
        new_HLayout.addWidget(new_label)

        new_radioButton = QtWidgets.QRadioButton(new_frame)
        new_radioButton.setObjectName("RadioButton_"+new_frame_name)
        new_radioButton.setText("")
        new_HLayout.addWidget(new_radioButton)

        self.verticalLayout_spectrogram_trackList.addWidget(new_frame)

        return [new_frame,new_HLayout,new_label,new_radioButton]

    def __remove_single_effect_frame(self,trackframe:list):
        [new_frame, new_VLayout, new_superiorHLayout, new_button, new_label,
         new_inferiorHLayout,
         new_leftVLayout, new_labelL, new_dialL, new_lcdL,
         new_rightVLayout, new_labelR, new_dialR, new_lcdR] =trackframe

        new_rightVLayout.removeWidget(new_lcdR)
        new_lcdR.deleteLater()
        new_rightVLayout.removeWidget(new_dialR)
        new_dialR.deleteLater()
        new_rightVLayout.removeWidget(new_labelR)
        new_labelR.deleteLater()

        new_rightVLayout.deleteLater()

        new_leftVLayout.removeWidget(new_lcdL)
        new_lcdL.deleteLater()
        new_leftVLayout.removeWidget(new_dialL)
        new_dialL.deleteLater()
        new_leftVLayout.removeWidget(new_labelL)
        new_labelL.deleteLater()

        new_leftVLayout.deleteLater()

        new_inferiorHLayout.deleteLater()

        new_superiorHLayout.removeWidget(new_label)
        new_label.deleteLater()
        new_superiorHLayout.removeWidget(new_button)
        new_button.deleteLater()

        new_superiorHLayout.deleteLater()
        new_VLayout.deleteLater()

        self.verticalLayout_synthesis_effectList.removeWidget(new_frame)
        new_frame.deleteLater()

    def __create_single_track_frame_in_synthesis(self, track_number: int) -> list:
        new_frame_name = f"NewFrame_{track_number}"

        new_frame = QtWidgets.QFrame(self.tab_synthesis)
        new_frame.setMinimumSize(QtCore.QSize(200,100))
        new_frame.setMaximumSize(QtCore.QSize(200,100))
        new_frame.setFrameShape(QtWidgets.QFrame.Box)
        new_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        new_frame.setObjectName(new_frame_name)

        new_VLayout = QtWidgets.QVBoxLayout(new_frame)
        new_VLayout.setObjectName("VLayout_"+new_frame_name)

        new_HLayout = QtWidgets.QHBoxLayout()
        new_HLayout.setObjectName("HLayout_"+new_frame_name)

        new_label = QtWidgets.QLabel(new_frame)
        new_label.setObjectName("Label_"+new_frame_name)
        new_label.setText("Track {0}".format(track_number))
        new_HLayout.addWidget(new_label)

        new_button = QtWidgets.QPushButton(new_frame)
        new_button.setObjectName("Button_"+new_frame_name)
        new_button.setText("Select")
        new_HLayout.addWidget(new_button)
        new_button.clicked.connect(functools.partial(self.__CB_select_track_to_see_effects,track_number))
        new_button.setDisabled(True)

        new_radioButton = QtWidgets.QRadioButton(new_frame)
        new_radioButton.setObjectName("RadioButton_"+new_frame_name)
        new_radioButton.setText("Mute")
        new_HLayout.addWidget(new_radioButton)

        new_VLayout.addLayout(new_HLayout)

        new_HSlider = QtWidgets.QSlider(new_frame)
        new_HSlider.setOrientation(QtCore.Qt.Horizontal)
        new_HSlider.setObjectName("Slider_"+new_frame_name)
        new_HSlider.setRange(0,127)
        new_HSlider.setValue(127)
        new_VLayout.addWidget(new_HSlider)

        new_comboBox = QtWidgets.QComboBox(new_frame)
        new_comboBox.setObjectName("ComboBox_"+new_frame_name)
        new_comboBox.addItem("Select an instrument")
        for inst in range(len(INSTRUMENT)-1):
            new_comboBox.addItem(INSTRUMENT(inst+1).name)
        #new_comboBox.addItem("")
        #new_comboBox.addItem("")
        new_VLayout.addWidget(new_comboBox)

        self.verticalLayout_synthesis_trackList.addWidget(new_frame)

        return [new_frame,new_VLayout,new_HLayout,
                new_label,new_button,new_radioButton,
                new_HSlider,new_comboBox]

    def __error_message(self, description:str):
        self.errorBox.setWindowTitle("Error")
        self.errorBox.setIcon(self.errorBox.Information)
        self.errorBox.setText(description)
        self.errorBox.exec()

    def __change_state_synth(self,state: STATE_SYNTH):
        print(f"STATE {state.name}")
        self.state_synth = state
        loaded = (self.state_synth == STATE_SYNTH.LOADED or self.state_synth == STATE_SYNTH.SYNTHESIZED or
                  self.state_synth == STATE_SYNTH.PLAYING)
        synthesized = self.state_synth == STATE_SYNTH.SYNTHESIZED or self.state_synth == STATE_SYNTH.PLAYING
        playing = self.state_synth == STATE_SYNTH.PLAYING

        self.pushButton_synthesize_synthesize.setDisabled(not loaded)
        self.pushButton_synthesize_save.setDisabled(not synthesized)
        self.pushButton_spectrogram_selectAll.setDisabled(not synthesized)
        self.pushButton_spectrogram_deselectAll.setDisabled(not synthesized)
        self.pushButton_spectrogram_plot.setDisabled(not synthesized)

        self.pushButton_synthesize_play_pause.setDisabled(not synthesized)
        self.pushButton_synthesize_stop.setDisabled(not synthesized)
        self.pushButton_synthesize_back.setDisabled(not synthesized)
        self.pushButton_synthesize_foward.setDisabled(not synthesized)

        self.comboBox_synthesize_selectEffectType.setDisabled(not synthesized)

        scriptDir = os.path.dirname(os.path.realpath(__file__))
        if playing:
            self.pushButton_synthesize_play_pause.setIcon(
                QtGui.QIcon(scriptDir + os.path.sep + "..\\resources\\icons\\symbol-pause.png"))
        else:
            self.pushButton_synthesize_play_pause.setIcon(
                QtGui.QIcon(scriptDir + os.path.sep + "..\\resources\\icons\\symbol-play.png"))

        for track_frame in self.track_frames:
            track_frame[4].setDisabled(not synthesized)

    def __CB_select_track_to_see_effects(self,track_number:int):
        self.__clean_current_effect_frames() #
        self.__load_effect_frames(track_number) # 0 es principal!
        self.selected_track = track_number
        print(f"Selected Track {track_number}")

    def __load_effect_frames(self, track_number: int):
        for effect_data in self.all_effects[track_number]:
            self.current_visible_effects.append(self.__create_single_effect_frame(effect_data.fun,effect_data.var1,effect_data.var2))

    def __clean_current_effect_frames(self):
        for effect_frame in self.current_visible_effects:
            self.__remove_single_effect_frame(effect_frame)
        self.current_visible_effects = []

    def __CB_synthesize(self):
        if self.state_synth == STATE_SYNTH.LOADED or self.state_synth == STATE_SYNTH.SYNTHESIZED:
            self.selected_track = 0
            self.audiotrackgroup = []
            for i,track in enumerate(self.trackgroup):
                self.audiotrackgroup.append(self.__synthesize_handler(track,self.__get_instrument_selected(i)))
            self.__change_state_synth(STATE_SYNTH.SYNTHESIZED)
            self.all_effects = []
            for i in range(len(self.audiotrackgroup)+1):
                self.all_effects.append([])
        else:
            self.__error_message("Synthesize is not currently available")

    def __CB_save(self):
        if self.state_synth == STATE_SYNTH.SYNTHESIZED:
            filename = QFileDialog.getSaveFileName(self,"Save WAV file",'c:\\',"WAV file (*.wav)")
            try:
                mix = self.__get_unfiltered_mix()
                self.audio_saver.save_wav_file(mix,filename[0])
            except:
                self.__error_message("Coudln't save file!")
        else:
            self.__error_message("Save is not currently available")

    def __synthesize_handler(self,track:Track,instrument:INSTRUMENT) -> AudioTrack:
        print("__synthesize_handler")
        print(instrument.name)
        if instrument == INSTRUMENT.GUITAR or instrument == INSTRUMENT.DRUM:
            self.physical_synth.synthesize_audio_track(track,instrument)
            return self.physical_synth.get_audio_track()
        elif instrument == INSTRUMENT.PIANO:
            self.additive_synth.synthesize_audio_track(track,instrument)
            return self.additive_synth.get_audio_track()
        elif instrument == INSTRUMENT.PIANO_2:
            self.sample_synth.synthesize_audio_track(track,instrument)
            return self.sample_synth.get_audio_track()
        else:
            return AudioTrack()

    def __get_instrument_selected(self,index:int)->INSTRUMENT:
        try:
            return INSTRUMENT(self.track_frames[index][7].currentIndex())
        except:
            self.__error_message("Invalid track index specified!")
            return INSTRUMENT.NONE

    def __get_unfiltered_mix(self) -> AudioTrack:
        lenght = []
        for audiotrack in self.audiotrackgroup:
            lenght.append(len(audiotrack.content))
        max_lenght = np.amax(lenght)

        mix = np.zeros(max_lenght)
        for i,audiotrack in enumerate(self.audiotrackgroup):
            partial = np.pad(audiotrack.content,(0,max_lenght-len(audiotrack.content)))
            normalized = np.divide(partial,np.amax(np.abs(partial)))
            weighted = np.multiply(normalized,self.__get_velocity_selected(i)/127)
            mix = mix + weighted
        audio_mix = AudioTrack()
        audio_mix.content = mix
        return audio_mix

    def __get_velocity_selected(self,index:int) -> int:
        try:
            velocity = 0
            if not self.track_frames[index][5].isChecked():
                velocity = self.track_frames[index][6].value()
            return velocity
        except:
            self.__error_message("Invalid track index specified!")
            return 0

    def __CB_connection(self,variable:list,new_value):
        variable[0] = new_value

    def __CB_dial_to_lcd(self,lcd,variable):
        lcd[0].display(variable)
