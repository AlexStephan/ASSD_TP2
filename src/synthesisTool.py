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
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

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

# !!!
import sounddevice as sd

# my modules!!!
from src.backend.tracks.track import Track,TrackGroup

from src.backend.midi2tracks import Midi2Tracks
from src.backend.audio_tracks.audio_track import AudioTrack

from resources.testing_code.audio_loader import AudioLoader
from src.backend.saver.audio_saver import AudioSaver
#from resources.testing_code.player_test import callback_sound_test

from src.backend.instruments.instrument_list import INSTRUMENT
from src.backend.synthesis.synthesis_template import SynthesisTemplate
from src.backend.synthesis.physical_modelling_synthesis import PhysicalModellingSynthesis
from src.backend.synthesis.additive_synthesis import AdditiveSynthesis

global test_audio_track
global position_in_audio


class STATE_SYNTH(Enum):
    EMPTY = 0
    LOADED = 1
    SYNTHESIZED = 2
    ERROR = 3


class SynthesisTool(QWidget,Ui_Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("TP GRUPAL 1 - Sampleo - ASSD")
        self.setWindowIcon(QtGui.QIcon('py.png'))

        self.__init_objects()
        self.__setCallbacks()

        self.synthesis_timer = QTimer()
        self.synthesis_timer.timeout.connect(self.__CB_synthesis_timer_step)

        self.pushButton_synthesize_play_pause.clicked.connect(self.__CB_synthesis_timer_play_pause)
        self.pushButton_synthesize_stop.clicked.connect(self.__CB_synthesis_timer_stop)

        self.audio_loader = AudioLoader()
        #self.audio_saver = AudioSaver()
        global test_audio_track
        test_audio_track = AudioTrack()
        self.output_stream = sd.OutputStream(channels=2,callback=self.__callback_sound_test,blocksize=1024,dtype='int16')#1024)
        global position_in_audio
        position_in_audio = 0

        self.pushButton_spectrogram_plot.clicked.connect(self.test)

        self.testingvar = 0

        self.initIcons()

    def __init_objects(self):
        self.midi2tracks = Midi2Tracks()
        self.trackgroup = []
        self.errorBox = QtWidgets.QMessageBox()

        self.track_frames = []

        self.additive_synth = AdditiveSynthesis()
        self.physical_synth = PhysicalModellingSynthesis()

        self.audiotrackgroup = []

        self.__change_state_synth(STATE_SYNTH.EMPTY)

        self.audio_saver = AudioSaver()

    def __setCallbacks(self):
        self.radioButton_singleNotes_selectNoteByFrequency.clicked.connect(self.__CB_radioButton_selectNoteByFrequency)
        self.__CB_radioButton_selectNoteByFrequency()

        self.pushButton_synthesize_loadFile.clicked.connect(self.__CB_open_midi_file)
        self.pushButton_synthesize_synthesize.clicked.connect(self.__CB_synthesize)
        self.pushButton_synthesize_save.clicked.connect(self.__CB_save)

    def __CB_synthesis_timer_step(self):
        print("Synthesis timer step!")

    def __CB_synthesis_timer_play_pause(self):
        print("Synthesis timer play pause!")

    def __CB_synthesis_timer_stop(self):
        print("Synthesis timer stop")

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
        is_ok,samplerate,audio_track_group=self.audio_loader.load_wav_file(".\\resources\\wav_files\\Level Music 1.wav")

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

    def __callback_sound_test(self,outdata: np.ndarray, frames: int, time, status):
        global position_in_audio
        global test_audio_track
        outdata[:] = test_audio_track.content[position_in_audio:(position_in_audio+frames)]
        position_in_audio = position_in_audio+frames
        print(f"frames = {frames}")

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
        self.track_frames = []

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
        return

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
        self.state_synth = state
        loaded = (self.state_synth == STATE_SYNTH.LOADED or self.state_synth == STATE_SYNTH.SYNTHESIZED)
        synthesized = self.state_synth == STATE_SYNTH.SYNTHESIZED

        self.pushButton_synthesize_synthesize.setDisabled(not loaded)
        self.pushButton_synthesize_save.setDisabled(not synthesized)

    def __CB_synthesize(self):
        if self.state_synth == STATE_SYNTH.LOADED or self.state_synth == STATE_SYNTH.SYNTHESIZED:
            self.audiotrackgroup = []
            for i,track in enumerate(self.trackgroup):
                self.audiotrackgroup.append(self.__synthesize_handler(track,self.__get_instrument_selected(i)))
                self.__change_state_synth(STATE_SYNTH.SYNTHESIZED)
        else:
            self.__error_message("Synthesize is not currently available")

    def __CB_save(self):
        if self.state_synth == STATE_SYNTH.SYNTHESIZED:
            filename = QFileDialog.getSaveFileName(self,"Save WAV file",'c:\\',"WAV file (*.wav)")
            try:
                mix = self.__get_unfiltered_mix()
                self.audio_saver.save_wav_file(mix,filename)
            except:
                self.__error_message("Coudln't save file!")
        else:
            self.__error_message("Save is not currently available")

    def __synthesize_handler(self,track:Track,instrument:INSTRUMENT) -> AudioTrack:
        print("__synthesize_handler")
        print(instrument.name)
        if instrument == INSTRUMENT.PIANO or instrument == INSTRUMENT.DRUM:
            self.physical_synth.synthesize_audio_track(track,instrument)
            return self.physical_synth.get_audio_track()
        elif instrument == INSTRUMENT.GUITAR:
            self.additive_synth.synthesize_audio_track(track,instrument)
            return self.additive_synth.get_audio_track()
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
        for i,audiotrack in self.audiotrackgroup:
            partial = np.pad(audiotrack.content,(0,max_lenght-len(audiotrack.content)))
            weighted = np.multiply(partial,self.__get_velocity_selected(i)/127)
            mix = mix + weighted
        return mix

    def __get_velocity_selected(self,index:int) -> int:
        try:
            velocity = 0
            if not self.track_frames[index][5].isChecked():
                velocity = self.track_frames[index][6].value()
            return velocity
        except:
            self.__error_message("Invalid track index specified!")
            return 0
