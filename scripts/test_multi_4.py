from PyQt5 import QtGui, QtCore, QtWidgets
import sys, os


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    toolButton = QtWidgets.QToolButton()
    toolButton.setText('Select')
    toolMenu = QtWidgets.QMenu()
    for i in range(3):
        checkBox = QtWidgets.QCheckBox(str(i), toolMenu)
        checkableAction = QtWidgets.QWidgetAction(toolMenu)
        checkableAction.setDefaultWidget(checkBox)
        toolMenu.addAction(checkableAction)
    toolButton.setMenu(toolMenu)
    toolButton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
    toolButton.show()
    sys.exit(app.exec_())