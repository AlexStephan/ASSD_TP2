# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_final.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(867, 731)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_synthesis = QtWidgets.QWidget()
        self.tab_synthesis.setObjectName("tab_synthesis")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_synthesis)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_synthesize_loadFile = QtWidgets.QPushButton(self.tab_synthesis)
        self.pushButton_synthesize_loadFile.setMinimumSize(QtCore.QSize(24, 24))
        self.pushButton_synthesize_loadFile.setMaximumSize(QtCore.QSize(24, 24))
        self.pushButton_synthesize_loadFile.setText("")
        self.pushButton_synthesize_loadFile.setObjectName("pushButton_synthesize_loadFile")
        self.horizontalLayout_2.addWidget(self.pushButton_synthesize_loadFile)
        self.label_loadFile = QtWidgets.QLabel(self.tab_synthesis)
        self.label_loadFile.setMinimumSize(QtCore.QSize(0, 24))
        self.label_loadFile.setMaximumSize(QtCore.QSize(16777215, 24))
        self.label_loadFile.setObjectName("label_loadFile")
        self.horizontalLayout_2.addWidget(self.label_loadFile)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(self.tab_synthesis)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_2.addWidget(self.line)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.scrollArea_synthesis_trackList = QtWidgets.QScrollArea(self.tab_synthesis)
        self.scrollArea_synthesis_trackList.setMinimumSize(QtCore.QSize(250, 0))
        self.scrollArea_synthesis_trackList.setMaximumSize(QtCore.QSize(250, 16777215))
        self.scrollArea_synthesis_trackList.setWidgetResizable(True)
        self.scrollArea_synthesis_trackList.setObjectName("scrollArea_synthesis_trackList")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 246, 540))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.scrollAreaWidgetContents_3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_synthesis_trackList = QtWidgets.QVBoxLayout()
        self.verticalLayout_synthesis_trackList.setObjectName("verticalLayout_synthesis_trackList")
        self.horizontalLayout.addLayout(self.verticalLayout_synthesis_trackList)
        self.scrollArea_synthesis_trackList.setWidget(self.scrollAreaWidgetContents_3)
        self.verticalLayout_3.addWidget(self.scrollArea_synthesis_trackList)
        self.pushButton_synthesize_synthesize = QtWidgets.QPushButton(self.tab_synthesis)
        self.pushButton_synthesize_synthesize.setMaximumSize(QtCore.QSize(250, 16777215))
        self.pushButton_synthesize_synthesize.setObjectName("pushButton_synthesize_synthesize")
        self.verticalLayout_3.addWidget(self.pushButton_synthesize_synthesize)
        self.pushButton_synthesize_save = QtWidgets.QPushButton(self.tab_synthesis)
        self.pushButton_synthesize_save.setMaximumSize(QtCore.QSize(250, 16777215))
        self.pushButton_synthesize_save.setObjectName("pushButton_synthesize_save")
        self.verticalLayout_3.addWidget(self.pushButton_synthesize_save)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.line_2 = QtWidgets.QFrame(self.tab_synthesis)
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.horizontalLayout_3.addWidget(self.line_2)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.pushButton_synthesize_play_pause = QtWidgets.QPushButton(self.tab_synthesis)
        self.pushButton_synthesize_play_pause.setMinimumSize(QtCore.QSize(40, 40))
        self.pushButton_synthesize_play_pause.setMaximumSize(QtCore.QSize(40, 40))
        self.pushButton_synthesize_play_pause.setText("")
        self.pushButton_synthesize_play_pause.setObjectName("pushButton_synthesize_play_pause")
        self.horizontalLayout_4.addWidget(self.pushButton_synthesize_play_pause)
        self.pushButton_synthesize_stop = QtWidgets.QPushButton(self.tab_synthesis)
        self.pushButton_synthesize_stop.setMinimumSize(QtCore.QSize(40, 40))
        self.pushButton_synthesize_stop.setMaximumSize(QtCore.QSize(40, 40))
        self.pushButton_synthesize_stop.setText("")
        self.pushButton_synthesize_stop.setObjectName("pushButton_synthesize_stop")
        self.horizontalLayout_4.addWidget(self.pushButton_synthesize_stop)
        self.pushButton_synthesize_back = QtWidgets.QPushButton(self.tab_synthesis)
        self.pushButton_synthesize_back.setMinimumSize(QtCore.QSize(40, 40))
        self.pushButton_synthesize_back.setMaximumSize(QtCore.QSize(40, 40))
        self.pushButton_synthesize_back.setText("")
        self.pushButton_synthesize_back.setObjectName("pushButton_synthesize_back")
        self.horizontalLayout_4.addWidget(self.pushButton_synthesize_back)
        self.pushButton_synthesize_foward = QtWidgets.QPushButton(self.tab_synthesis)
        self.pushButton_synthesize_foward.setMinimumSize(QtCore.QSize(40, 40))
        self.pushButton_synthesize_foward.setMaximumSize(QtCore.QSize(40, 40))
        self.pushButton_synthesize_foward.setText("")
        self.pushButton_synthesize_foward.setObjectName("pushButton_synthesize_foward")
        self.horizontalLayout_4.addWidget(self.pushButton_synthesize_foward)
        self.verticalLayout_4.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.comboBox_synthesize_selectEffectType = QtWidgets.QComboBox(self.tab_synthesis)
        self.comboBox_synthesize_selectEffectType.setObjectName("comboBox_synthesize_selectEffectType")
        self.comboBox_synthesize_selectEffectType.addItem("")
        self.comboBox_synthesize_selectEffectType.addItem("")
        self.comboBox_synthesize_selectEffectType.addItem("")
        self.comboBox_synthesize_selectEffectType.addItem("")
        self.horizontalLayout_5.addWidget(self.comboBox_synthesize_selectEffectType)
        self.pushButton_synthesize_addEffect = QtWidgets.QPushButton(self.tab_synthesis)
        self.pushButton_synthesize_addEffect.setMaximumSize(QtCore.QSize(70, 16777215))
        self.pushButton_synthesize_addEffect.setObjectName("pushButton_synthesize_addEffect")
        self.horizontalLayout_5.addWidget(self.pushButton_synthesize_addEffect)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.scrollArea_synthesis_effectList = QtWidgets.QScrollArea(self.tab_synthesis)
        self.scrollArea_synthesis_effectList.setWidgetResizable(True)
        self.scrollArea_synthesis_effectList.setObjectName("scrollArea_synthesis_effectList")
        self.scrollAreaWidgetContents_4 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_4.setGeometry(QtCore.QRect(0, 0, 394, 524))
        self.scrollAreaWidgetContents_4.setObjectName("scrollAreaWidgetContents_4")
        self.verticalLayout_17 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_4)
        self.verticalLayout_17.setObjectName("verticalLayout_17")
        self.verticalLayout_synthesis_effectList = QtWidgets.QVBoxLayout()
        self.verticalLayout_synthesis_effectList.setObjectName("verticalLayout_synthesis_effectList")
        self.verticalLayout_17.addLayout(self.verticalLayout_synthesis_effectList)
        self.scrollArea_synthesis_effectList.setWidget(self.scrollAreaWidgetContents_4)
        self.verticalLayout_4.addWidget(self.scrollArea_synthesis_effectList)
        self.horizontalLayout_3.addLayout(self.verticalLayout_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab_synthesis, "")
        self.tab_spectrogram = QtWidgets.QWidget()
        self.tab_spectrogram.setObjectName("tab_spectrogram")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.tab_spectrogram)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.scrollArea_spectrogram_trackList = QtWidgets.QScrollArea(self.tab_spectrogram)
        self.scrollArea_spectrogram_trackList.setMaximumSize(QtCore.QSize(200, 16777215))
        self.scrollArea_spectrogram_trackList.setWidgetResizable(True)
        self.scrollArea_spectrogram_trackList.setObjectName("scrollArea_spectrogram_trackList")
        self.scrollAreaWidgetContents_5 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_5.setGeometry(QtCore.QRect(0, 0, 196, 387))
        self.scrollAreaWidgetContents_5.setObjectName("scrollAreaWidgetContents_5")
        self.verticalLayout_20 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_5)
        self.verticalLayout_20.setObjectName("verticalLayout_20")
        self.verticalLayout_spectrogram_trackList = QtWidgets.QVBoxLayout()
        self.verticalLayout_spectrogram_trackList.setObjectName("verticalLayout_spectrogram_trackList")
        self.verticalLayout_20.addLayout(self.verticalLayout_spectrogram_trackList)
        self.scrollArea_spectrogram_trackList.setWidget(self.scrollAreaWidgetContents_5)
        self.verticalLayout_8.addWidget(self.scrollArea_spectrogram_trackList)
        self.pushButton_spectrogram_selectAll = QtWidgets.QPushButton(self.tab_spectrogram)
        self.pushButton_spectrogram_selectAll.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pushButton_spectrogram_selectAll.setObjectName("pushButton_spectrogram_selectAll")
        self.verticalLayout_8.addWidget(self.pushButton_spectrogram_selectAll)
        self.pushButton_spectrogram_deselectAll = QtWidgets.QPushButton(self.tab_spectrogram)
        self.pushButton_spectrogram_deselectAll.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pushButton_spectrogram_deselectAll.setObjectName("pushButton_spectrogram_deselectAll")
        self.verticalLayout_8.addWidget(self.pushButton_spectrogram_deselectAll)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_spectrogram_intTime = QtWidgets.QLabel(self.tab_spectrogram)
        self.label_spectrogram_intTime.setMinimumSize(QtCore.QSize(60, 0))
        self.label_spectrogram_intTime.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_spectrogram_intTime.setObjectName("label_spectrogram_intTime")
        self.horizontalLayout_12.addWidget(self.label_spectrogram_intTime)
        self.doubleSpinBox_spectrogram_intTime = QtWidgets.QDoubleSpinBox(self.tab_spectrogram)
        self.doubleSpinBox_spectrogram_intTime.setMinimumSize(QtCore.QSize(115, 0))
        self.doubleSpinBox_spectrogram_intTime.setMaximumSize(QtCore.QSize(115, 16777215))
        self.doubleSpinBox_spectrogram_intTime.setObjectName("doubleSpinBox_spectrogram_intTime")
        self.horizontalLayout_12.addWidget(self.doubleSpinBox_spectrogram_intTime)
        self.verticalLayout_8.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_spectrogram_duration = QtWidgets.QLabel(self.tab_spectrogram)
        self.label_spectrogram_duration.setMinimumSize(QtCore.QSize(60, 0))
        self.label_spectrogram_duration.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_spectrogram_duration.setObjectName("label_spectrogram_duration")
        self.horizontalLayout_13.addWidget(self.label_spectrogram_duration)
        self.doubleSpinBox_spectrogram_duration = QtWidgets.QDoubleSpinBox(self.tab_spectrogram)
        self.doubleSpinBox_spectrogram_duration.setMinimumSize(QtCore.QSize(115, 0))
        self.doubleSpinBox_spectrogram_duration.setMaximumSize(QtCore.QSize(115, 16777215))
        self.doubleSpinBox_spectrogram_duration.setObjectName("doubleSpinBox_spectrogram_duration")
        self.horizontalLayout_13.addWidget(self.doubleSpinBox_spectrogram_duration)
        self.verticalLayout_8.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_24 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_24.setObjectName("horizontalLayout_24")
        self.label_spectrogram_intTime_2 = QtWidgets.QLabel(self.tab_spectrogram)
        self.label_spectrogram_intTime_2.setMinimumSize(QtCore.QSize(60, 0))
        self.label_spectrogram_intTime_2.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_spectrogram_intTime_2.setObjectName("label_spectrogram_intTime_2")
        self.horizontalLayout_24.addWidget(self.label_spectrogram_intTime_2)
        self.spinBox_spectrogram_NFFT = QtWidgets.QSpinBox(self.tab_spectrogram)
        self.spinBox_spectrogram_NFFT.setMinimumSize(QtCore.QSize(115, 0))
        self.spinBox_spectrogram_NFFT.setMaximumSize(QtCore.QSize(115, 16777215))
        self.spinBox_spectrogram_NFFT.setMinimum(1)
        self.spinBox_spectrogram_NFFT.setMaximum(999999999)
        self.spinBox_spectrogram_NFFT.setProperty("value", 1024)
        self.spinBox_spectrogram_NFFT.setObjectName("spinBox_spectrogram_NFFT")
        self.horizontalLayout_24.addWidget(self.spinBox_spectrogram_NFFT)
        self.verticalLayout_8.addLayout(self.horizontalLayout_24)
        self.horizontalLayout_25 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_25.setObjectName("horizontalLayout_25")
        self.label_spectrogram_intTime_3 = QtWidgets.QLabel(self.tab_spectrogram)
        self.label_spectrogram_intTime_3.setMinimumSize(QtCore.QSize(60, 0))
        self.label_spectrogram_intTime_3.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_spectrogram_intTime_3.setObjectName("label_spectrogram_intTime_3")
        self.horizontalLayout_25.addWidget(self.label_spectrogram_intTime_3)
        self.spinBox_spectrogram_overlap = QtWidgets.QSpinBox(self.tab_spectrogram)
        self.spinBox_spectrogram_overlap.setMinimumSize(QtCore.QSize(115, 0))
        self.spinBox_spectrogram_overlap.setMaximumSize(QtCore.QSize(115, 16777215))
        self.spinBox_spectrogram_overlap.setMinimum(0)
        self.spinBox_spectrogram_overlap.setMaximum(999999999)
        self.spinBox_spectrogram_overlap.setProperty("value", 512)
        self.spinBox_spectrogram_overlap.setObjectName("spinBox_spectrogram_overlap")
        self.horizontalLayout_25.addWidget(self.spinBox_spectrogram_overlap)
        self.verticalLayout_8.addLayout(self.horizontalLayout_25)
        self.horizontalLayout_26 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_26.setObjectName("horizontalLayout_26")
        self.label_spectrogram_intTime_4 = QtWidgets.QLabel(self.tab_spectrogram)
        self.label_spectrogram_intTime_4.setMinimumSize(QtCore.QSize(60, 0))
        self.label_spectrogram_intTime_4.setMaximumSize(QtCore.QSize(60, 16777215))
        self.label_spectrogram_intTime_4.setObjectName("label_spectrogram_intTime_4")
        self.horizontalLayout_26.addWidget(self.label_spectrogram_intTime_4)
        self.comboBox_spectrogram_window = QtWidgets.QComboBox(self.tab_spectrogram)
        self.comboBox_spectrogram_window.setMinimumSize(QtCore.QSize(115, 0))
        self.comboBox_spectrogram_window.setMaximumSize(QtCore.QSize(115, 16777215))
        self.comboBox_spectrogram_window.setObjectName("comboBox_spectrogram_window")
        self.comboBox_spectrogram_window.addItem("")
        self.comboBox_spectrogram_window.addItem("")
        self.comboBox_spectrogram_window.addItem("")
        self.comboBox_spectrogram_window.addItem("")
        self.comboBox_spectrogram_window.addItem("")
        self.comboBox_spectrogram_window.addItem("")
        self.horizontalLayout_26.addWidget(self.comboBox_spectrogram_window)
        self.verticalLayout_8.addLayout(self.horizontalLayout_26)
        self.pushButton_spectrogram_plot = QtWidgets.QPushButton(self.tab_spectrogram)
        self.pushButton_spectrogram_plot.setMaximumSize(QtCore.QSize(200, 16777215))
        self.pushButton_spectrogram_plot.setObjectName("pushButton_spectrogram_plot")
        self.verticalLayout_8.addWidget(self.pushButton_spectrogram_plot)
        self.horizontalLayout_9.addLayout(self.verticalLayout_8)
        self.line_3 = QtWidgets.QFrame(self.tab_spectrogram)
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.horizontalLayout_9.addWidget(self.line_3)
        self.verticalLayout_9 = QtWidgets.QVBoxLayout()
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.stackedWidget_spectrogram = QtWidgets.QStackedWidget(self.tab_spectrogram)
        self.stackedWidget_spectrogram.setObjectName("stackedWidget_spectrogram")
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        self.stackedWidget_spectrogram.addWidget(self.page)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.stackedWidget_spectrogram.addWidget(self.page_2)
        self.verticalLayout_9.addWidget(self.stackedWidget_spectrogram)
        self.frame = QtWidgets.QFrame(self.tab_spectrogram)
        self.frame.setMinimumSize(QtCore.QSize(0, 60))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.horizontalLayout_spectrogram_plotSettings = QtWidgets.QHBoxLayout()
        self.horizontalLayout_spectrogram_plotSettings.setObjectName("horizontalLayout_spectrogram_plotSettings")
        self.horizontalLayout_11.addLayout(self.horizontalLayout_spectrogram_plotSettings)
        self.verticalLayout_9.addWidget(self.frame)
        self.horizontalLayout_9.addLayout(self.verticalLayout_9)
        self.tabWidget.addTab(self.tab_spectrogram, "")
        self.verticalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        self.comboBox_spectrogram_window.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_loadFile.setText(_translate("Form", "Choose a MIDI file"))
        self.pushButton_synthesize_synthesize.setText(_translate("Form", "Synthesize"))
        self.pushButton_synthesize_save.setText(_translate("Form", "Save"))
        self.comboBox_synthesize_selectEffectType.setItemText(0, _translate("Form", "Add Effect - Track"))
        self.comboBox_synthesize_selectEffectType.setItemText(1, _translate("Form", "Eco"))
        self.comboBox_synthesize_selectEffectType.setItemText(2, _translate("Form", "Simple Reverb"))
        self.comboBox_synthesize_selectEffectType.setItemText(3, _translate("Form", "Flanger"))
        self.pushButton_synthesize_addEffect.setText(_translate("Form", "Add Effect"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_synthesis), _translate("Form", "Synthesis"))
        self.pushButton_spectrogram_selectAll.setText(_translate("Form", "Select All"))
        self.pushButton_spectrogram_deselectAll.setText(_translate("Form", "Deselect All"))
        self.label_spectrogram_intTime.setText(_translate("Form", "Int Time"))
        self.label_spectrogram_duration.setText(_translate("Form", "Duration"))
        self.label_spectrogram_intTime_2.setText(_translate("Form", "NFFT"))
        self.label_spectrogram_intTime_3.setText(_translate("Form", "Overlap"))
        self.label_spectrogram_intTime_4.setText(_translate("Form", "Window"))
        self.comboBox_spectrogram_window.setItemText(0, _translate("Form", "None"))
        self.comboBox_spectrogram_window.setItemText(1, _translate("Form", "Bartlett"))
        self.comboBox_spectrogram_window.setItemText(2, _translate("Form", "Hanning"))
        self.comboBox_spectrogram_window.setItemText(3, _translate("Form", "Hamming"))
        self.comboBox_spectrogram_window.setItemText(4, _translate("Form", "Blackman"))
        self.comboBox_spectrogram_window.setItemText(5, _translate("Form", "Blackman-Harris"))
        self.pushButton_spectrogram_plot.setText(_translate("Form", "Plot"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_spectrogram), _translate("Form", "Spectrogram"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())
