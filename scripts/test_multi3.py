from PyQt5 import QtGui, QtCore, QtWidgets

def isChecked():
    """ Prints selected menu labels. """
    [print(action.text()) for action in menu.actions() if action.isChecked()]

app = QtWidgets.QApplication([])
w = QtWidgets.QMainWindow()
menu = QtWidgets.QMenu("menu", w)
menu.addAction(QtWidgets.QAction('50%', menu, checkable=True))
menu.addAction(QtWidgets.QAction('100%', menu, checkable=True))
menu.addAction(QtWidgets.QAction('200%', menu, checkable=True))
menu.addAction(QtWidgets.QAction('400%', menu, checkable=True))
menu.triggered.connect(isChecked)
# menu.setPopupMode(QtWidgets.QToolButton.InstantPopup)

w.menuBar().addMenu(menu)
w.show()
app.exec_()