from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
import sys, os

class multiSelectMenu(QMainWindow):

    def __init__(self):
        super(QMainWindow, self).__init__()
        myQWidget = QWidget()
        myBoxLayout = QVBoxLayout()
        myQWidget.setLayout(myBoxLayout)
        self.setCentralWidget(myQWidget)
        self.toolbutton = QToolButton(self)
        self.toolbutton.setText('Select Categories ')
        self.toolmenu = QMenu(self)
        for i in range(3):
            action = self.toolmenu.addAction("Category " + str(i))
            action.setCheckable(True)
        self.toolbutton.setMenu(self.toolmenu)
        self.toolbutton.setPopupMode(QToolButton.InstantPopup)
        myBoxLayout.addWidget(self.toolbutton)
        self.toolmenu.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() in [QtCore.QEvent.MouseButtonRelease]:
            if isinstance(obj, QMenu):
                if obj.activeAction():
                    if not obj.activeAction().menu(): #if the selected action does not have a submenu
                        #eat the event, but trigger the function
                        obj.activeAction().trigger()
                        return True
        return super(multiSelectMenu, self).eventFilter(obj, event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    dialog_1 = multiSelectMenu()
    dialog_1.show()
    dialog_1.resize(480,320)
    sys.exit(app.exec_())

