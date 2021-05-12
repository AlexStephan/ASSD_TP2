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
from src.backend.midi2tracks import Midi2Tracks
from src.backend.audio_tracks.audio_track import AudioTrack

from resources.testing_code.audio_loader import AudioLoader
from src.backend.saver.audio_saver import AudioSaver
#from resources.testing_code.player_test import callback_sound_test

global test_audio_track
global position_in_audio


class SynthesisTool(QWidget,Ui_Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("TP GRUPAL 1 - Sampleo - ASSD")
        self.setWindowIcon(QtGui.QIcon('py.png'))

        self.__init_objects()

        self.synthesis_timer = QTimer()
        self.synthesis_timer.timeout.connect(self.__CB_synthesis_timer_step)

        self.pushButton_synthesize_play_pause.clicked.connect(self.__CB_synthesis_timer_play_pause)
        self.pushButton_synthesize_stop.clicked.connect(self.__CB_synthesis_timer_stop)

        self.audio_loader = AudioLoader()
        self.audio_saver = AudioSaver()
        global test_audio_track
        test_audio_track = AudioTrack()
        self.output_stream = sd.OutputStream(channels=2,callback=self.__callback_sound_test,blocksize=1024,dtype='int16')#1024)
        global position_in_audio
        position_in_audio = 0
        self.pushButton_synthesize_loadFile.clicked.connect(self.__CB_open_midi_file)
        self.pushButton_spectrogram_plot.clicked.connect(self.test)

        self.testingvar = 0

        self.initIcons()

        self.__setCallbacks()

    def __init_objects(self):
        self.midi2tracks = Midi2Tracks()

        self.errorBox = QtWidgets.QMessageBox()

    def __setCallbacks(self):
        self.radioButton_singleNotes_selectNoteByFrequency.clicked.connect(self.__CB_radioButton_selectNoteByFrequency)
        self.__CB_radioButton_selectNoteByFrequency()

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

    def create_synthesis_track_box(self,newFrameName,numberOfTrack):
        new_frame = QtWidgets.QFrame(self.tab_synthesis)
        new_frame.setMinimumSize(QtCore.QSize(200,100))
        new_frame.setMaximumSize(QtCore.QSize(200,100))
        new_frame.setFrameShape(QtWidgets.QFrame.Box)
        new_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        new_frame.setObjectName(newFrameName)

        new_VLayout = QtWidgets.QVBoxLayout(new_frame)
        new_VLayout.setObjectName("VLayout_"+newFrameName)

        new_HLayout = QtWidgets.QHBoxLayout()
        new_HLayout.setObjectName("HLayout_"+newFrameName)

        new_label = QtWidgets.QLabel(new_frame)
        new_label.setObjectName("Label_"+newFrameName)
        new_label.setText("Track {0}".format(numberOfTrack))
        new_HLayout.addWidget(new_label)

        new_button = QtWidgets.QPushButton(new_frame)
        new_button.setObjectName("Button_"+newFrameName)
        new_button.setText("Select")
        new_HLayout.addWidget(new_button)

        new_radioButton = QtWidgets.QRadioButton(new_frame)
        new_radioButton.setObjectName("RadioButton_"+newFrameName)
        new_radioButton.setText("Mute")
        new_HLayout.addWidget(new_radioButton)

        new_VLayout.addLayout(new_HLayout)

        new_HSlider = QtWidgets.QSlider(new_frame)
        new_HSlider.setOrientation(QtCore.Qt.Horizontal)
        new_HSlider.setObjectName("Slider_"+newFrameName)
        new_HSlider.setRange(0,99)
        new_HSlider.setValue(99)
        new_VLayout.addWidget(new_HSlider)

        new_comboBox = QtWidgets.QComboBox(new_frame)
        new_comboBox.setObjectName("ComboBox_"+newFrameName)
        new_comboBox.addItem("")
        new_comboBox.addItem("")
        new_comboBox.addItem("")
        new_VLayout.addWidget(new_comboBox)

        self.verticalLayout_synthesis_trackList.addWidget(new_frame)

    def create_synthesis_effect_box(self,newFrameName,newEffectName,newExtraData):
        new_frame = QtWidgets.QFrame(self.tab_synthesis)
        #new_frame.setMinimumSize(QtCore.QSize(200,100))
        new_frame.setMaximumSize(QtCore.QSize(16777215,90))
        new_frame.setFrameShape(QtWidgets.QFrame.Box)
        new_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        new_frame.setObjectName(newFrameName)

        new_VLayout = QtWidgets.QVBoxLayout(new_frame)
        new_VLayout.setObjectName("VLayout_" + newFrameName)

        new_HLayout = QtWidgets.QHBoxLayout()
        new_HLayout.setObjectName("HLayout_" + newFrameName)

        new_Xbutton = QtWidgets.QPushButton(new_frame)
        new_Xbutton.setMinimumSize(QtCore.QSize(24,24))
        new_Xbutton.setMaximumSize(QtCore.QSize(24, 24))
        new_Xbutton.setObjectName("XButton_" + newFrameName)
        new_Xbutton.setText("X")
        new_HLayout.addWidget(new_Xbutton)

        new_label = QtWidgets.QLabel(new_frame)
        new_label.setObjectName("Label_" + newFrameName)
        new_label.setText(newEffectName)
        new_HLayout.addWidget(new_label)

        new_button = QtWidgets.QPushButton(new_frame)
        new_Xbutton.setMaximumSize(QtCore.QSize(60, 16777215))
        new_button.setObjectName("Button_" + newFrameName)
        new_button.setText("Select")
        new_HLayout.addWidget(new_button)

        new_VLayout.addLayout(new_HLayout)

        new_extralabel = QtWidgets.QLabel(new_frame)
        new_extralabel.setObjectName("ExtraLabel_" + newFrameName)
        new_extralabel.setText(newExtraData)
        new_VLayout.addWidget(new_extralabel)

        self.verticalLayout_synthesis_effectList.addWidget(new_frame)

    def create_spectrogram_track_box(self,newFrameName,numberOfTrack):
        new_frame = QtWidgets.QFrame(self.scrollAreaWidgetContents_5)
        new_frame.setMaximumSize(QtCore.QSize(16777215, 45))
        new_frame.setFrameShape(QtWidgets.QFrame.Box)
        new_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        new_frame.setObjectName(newFrameName)
        new_HLayout = QtWidgets.QHBoxLayout(new_frame)
        new_HLayout.setObjectName("HLayout_"+newFrameName)
        new_label = QtWidgets.QLabel(new_frame)
        new_label.setObjectName("Label_"+newFrameName)
        new_label.setText("Track {0}".format(numberOfTrack))
        new_HLayout.addWidget(new_label)
        new_radioButton = QtWidgets.QRadioButton(new_frame)
        new_radioButton.setMaximumSize(QtCore.QSize(16, 16))
        new_radioButton.setText("")
        new_radioButton.setObjectName("RadioButton_"+newFrameName)
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
        if filename[0]!= "":
            self.Midi2Tracks.load_midi_file(filename[0])

            if:

            else:
                self.__error_message("Couldn't open file!")


    def __error_message(self, description:str):
        self.errorBox.setWindowTitle("Error")
        self.errorBox.setIcon(self.errorBox.Information)
        self.errorBox.setText(description)
        self.errorBox.exec()
