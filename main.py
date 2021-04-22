from src.synthesisTool import SynthesisTool
from PyQt5.QtWidgets import QApplication
#from src.de_internet.latexManagement import testingLatexInMatPlotLib

#TESTINGLATEX = True

if __name__ == '__main__':
#    if TESTINGLATEX:
#        testingLatexInMatPlotLib()
#    else:
    app = QApplication([])
    window = SynthesisTool()
    window.show()
    app.exec()

