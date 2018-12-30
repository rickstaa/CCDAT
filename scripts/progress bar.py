from PyQt5 import QtGui, QtCore, QWidgets
import os
import time

class MyBar(QWidgets):
    i = 0
    style =''' 
    QProgressBar
    {
        border: 2px solid grey;
        border-radius: 5px;
        text-align: center;
    }
    '''
    def __init__(self):
        super(MyBar, self).__init__()
        grid = QtGui.QGridLayout()

        self.bar = QtGui.QProgressBar()
        self.bar.setMaximum(1)
        self.bar.setMinimum(0)

        self.bar.setStyleSheet(self.style)

        self.bar.setRange(0,0)

        self.label=QtGui.QLabel("Nudge")
        self.label.setStyleSheet("QLabel { font-size: 20px }")
        self.label.setAlignment(QtCore.Qt.AlignCenter)


        grid.addWidget(self.bar, 0,0)
        grid.addWidget(self.label, 0,0)
        self.setLayout(grid)

class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.bar = MyBar()

        self.setCentralWidget(self.bar)


if __name__ == '__main__':
    app = QtGui.QApplication([])
    win = MainWindow()
    win.show();
    QtGui.QApplication.instance().exec_()