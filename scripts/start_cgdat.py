"""This script is used to start the cgdat gui out of the command line"""

# Import modules
import os, sys
import os.path
from PyQt5 import QtGui, QtWidgets

# Import package modules
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir))
)
from cgdat.cgdat_gui import DataAnalyserGUI

# Get relative script path
dirname = os.path.dirname(os.path.abspath(__file__))

##############################################################
#### Main execution function                              ####
##############################################################
def main():
    """Main function starting the gcdat gui."""

    # Create QT app
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    # Create Main window
    ui = DataAnalyserGUI()
    ui.setupUi(MainWindow)

    # Set icon
    CGDAT_icon = os.path.join(dirname, "..", r"cgdat\static\media\CGDAT.svg")
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(CGDAT_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    MainWindow.setWindowIcon(icon)

    # Show main window
    MainWindow.showMaximized()
    sys.exit(app.exec_())


##############################################################
#### Run if executed as main                              ####
##############################################################
if __name__ == "__main__":
    main()
