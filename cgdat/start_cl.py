'''This script is used to strat the cgdat gui out of the command line'''

### Import modules ###
from PyQt5 import QtCore, QtGui, QtWidgets
import os, sys

### Import package modules ###
from cgdat import DataAnalyserGUI

### Get relative script path ###
dirname = os.path.dirname(os.path.abspath(__file__))

##############################################################
#### Main execution function                              ####
##############################################################
def main():

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

main()