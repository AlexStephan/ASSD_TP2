from Lib.random import random, seed

# Qt Modules
from PyQt5.QtCore import Qt
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

class SynthesisTool(QWidget,Ui_Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.setWindowTitle("TP GRUPAL 1 - Sampleo - ASSD")
        self.setWindowIcon(QtGui.QIcon('py.png'))

        self.pushButton_synthesize_loadFile.clicked.connect(self.test)

        self.testingvar = 0

        self.initIcons()

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

    def test(self):
        print("test")

        if self.testingvar == 0:
            self.testingvar = 1
            self.frame__1 = QtWidgets.QFrame(self.tab_synthesis)
            self.frame__1.setMinimumSize(QtCore.QSize(100,100))
            self.frame__1.setMaximumSize(QtCore.QSize(100,100))
            self.frame__1.setFrameShape(QtWidgets.QFrame.Box)
            self.frame__1.setFrameShadow(QtWidgets.QFrame.Raised)
            self.frame__1.setObjectName("frame__1")
            self.horizontalLayout_synthesis_trackList.addWidget(self.frame__1)

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

            print("")
            self.verticalLayout__1.removeWidget(self.pushButton__1)
            self.pushButton__1.deleteLater()
            self.pushButton__1 = None
            self.verticalLayout__1.removeWidget(self.pushButton__2)
            self.pushButton__2.deleteLater()
            self.pushButton__2 = None

            self.verticalLayout__1.deleteLater()
            self.verticalLayout__1 = None

            self.horizontalLayout_synthesis_trackList.removeWidget(self.frame__1)
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

