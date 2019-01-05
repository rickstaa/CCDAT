'''Script used to run the gui directly from the command line.'''

### Import package ###
from .cgdat import DataAnalyserGUI
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, os

### Get relative script path ###
dirname = os.path.dirname(os.path.abspath(__file__))

#####################################################################
#### Script settings                                             ####
#####################################################################
def start_gui():

    ### Create QT app ###
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ### Create Main window ###
    ui = DataAnalyserGUI()
    ui.setupUi(MainWindow)

    ### Set icon ###
    CGDAT_icon = os.path.join(dirname, '..', r'media\cgdat_new.png')
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(CGDAT_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    MainWindow.setWindowIcon(icon)

    ### Show main window ###
    MainWindow.showMaximized()
    sys.exit(app.exec_())