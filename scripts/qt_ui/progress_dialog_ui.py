# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\ricks\OneDrive\Development\Tools\CGDAT\scripts\..\qt\progress_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProgressDialog(object):
    def setupUi(self, ProgressDialog):
        ProgressDialog.setObjectName("ProgressDialog")
        ProgressDialog.resize(471, 312)
        self.gridLayout = QtWidgets.QGridLayout(ProgressDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.buttonBox = QtWidgets.QDialogButtonBox(ProgressDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 1)
        self.progress_header = QtWidgets.QLabel(ProgressDialog)
        self.progress_header.setWordWrap(True)
        self.progress_header.setObjectName("progress_header")
        self.gridLayout.addWidget(self.progress_header, 0, 0, 1, 1)
        self.progress_bar = QtWidgets.QProgressBar(ProgressDialog)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setInvertedAppearance(False)
        self.progress_bar.setObjectName("progress_bar")
        self.gridLayout.addWidget(self.progress_bar, 2, 0, 1, 1)
        self.progress_console = QtWidgets.QTextEdit(ProgressDialog)
        self.progress_console.setReadOnly(True)
        self.progress_console.setObjectName("progress_console")
        self.gridLayout.addWidget(self.progress_console, 1, 0, 1, 1)

        self.retranslateUi(ProgressDialog)
        self.buttonBox.accepted.connect(ProgressDialog.accept)
        self.buttonBox.rejected.connect(ProgressDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(ProgressDialog)

    def retranslateUi(self, ProgressDialog):
        _translate = QtCore.QCoreApplication.translate
        ProgressDialog.setWindowTitle(_translate("ProgressDialog", "Data analysis progress dialog"))
        self.progress_header.setText(_translate("ProgressDialog", "<html><head/><body><p><span style=\" font-size:14pt;\">Data analysis is being performed. Please wait till data analysis is complete or cancel the data analysis.</span></p></body></html>"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ProgressDialog = QtWidgets.QDialog()
    ui = Ui_ProgressDialog()
    ui.setupUi(ProgressDialog)
    ProgressDialog.show()
    sys.exit(app.exec_())

