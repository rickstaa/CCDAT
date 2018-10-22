# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\ricks\OneDrive\Work\Wesley\qt\about.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_about(object):
    def setupUi(self, about):
        about.setObjectName("about")
        about.resize(400, 288)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(about.sizePolicy().hasHeightForWidth())
        about.setSizePolicy(sizePolicy)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(about)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(about)
        self.label.setStyleSheet("QLabel{background-color: white;padding: 5px 10px 15px 10px;}\n"
"QFrame{border: 1px solid rgb(179, 179, 179);border-radius: 2px;}\n"
"")
        self.label.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.label.setFrameShadow(QtWidgets.QFrame.Plain)
        self.label.setLineWidth(1)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)

        self.retranslateUi(about)
        QtCore.QMetaObject.connectSlotsByName(about)

    def retranslateUi(self, about):
        _translate = QtCore.QCoreApplication.translate
        about.setWindowTitle(_translate("about", "Dialog"))
        self.label.setText(_translate("about", "<html><head/><body><p><span style=\" font-size:12pt; text-decoration: underline;\">Description:</span></p><p><span style=\" font-size:12pt;\">This tool was created to aid in a more streamlined <br/>game data analysation process. For questions or<br/>surgestions mail </span><a href=\"mail:wbosman@fittestbody.nl\"><span style=\" font-size:12pt; text-decoration: underline; color:#0000ff;\">wbosman@fittestbody.nl</span></a><span style=\" font-size:12pt;\">.</span></p><p><br/><span style=\" font-size:12pt; text-decoration: underline;\">Other info:</span></p><p><span style=\" font-size:12pt; font-weight:600;\">Create By: </span><span style=\" font-size:12pt;\">Rick Staa</span></p><p><span style=\" font-size:12pt; font-weight:600;\">Maintained by: </span><span style=\" font-size:12pt;\">Wesley Bosman</span><br/></p><p><span style=\" font-size:12pt;\">Copyright 2018 </span><span style=\" font-size:12pt; font-weight:600;\">© </span><a href=\"http://www.fittestbody.nl\"><span style=\" text-decoration: underline; color:#0000ff;\">fittestbody.nl</span></a></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    about = QtWidgets.QDialog()
    ui = Ui_about()
    ui.setupUi(about)
    about.show()
    sys.exit(app.exec_())

