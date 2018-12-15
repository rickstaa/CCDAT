# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\ricks\OneDrive\Development\Tools\CGDAT\scripts\..\qt\output_settings.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_output_settings(object):
    def setupUi(self, output_settings):
        output_settings.setObjectName("output_settings")
        output_settings.resize(400, 300)
        self.gridLayout = QtWidgets.QGridLayout(output_settings)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox = QtWidgets.QGroupBox(output_settings)
        self.groupBox.setStyleSheet("QGroupBox{padding-top:15px; margin-top:-15px}")
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setText("")
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.checkBox_3 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_3.setObjectName("checkBox_3")
        self.gridLayout_2.addWidget(self.checkBox_3, 0, 2, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout_2.addWidget(self.checkBox, 0, 0, 1, 1)
        self.checkBox_2 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout_2.addWidget(self.checkBox_2, 0, 1, 1, 1)
        self.checkBox_4 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_4.setObjectName("checkBox_4")
        self.gridLayout_2.addWidget(self.checkBox_4, 1, 2, 1, 1)
        self.checkBox_5 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_5.setObjectName("checkBox_5")
        self.gridLayout_2.addWidget(self.checkBox_5, 1, 1, 1, 1)
        self.checkBox_6 = QtWidgets.QCheckBox(self.groupBox)
        self.checkBox_6.setObjectName("checkBox_6")
        self.gridLayout_2.addWidget(self.checkBox_6, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(output_settings)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(output_settings)
        self.buttonBox.accepted.connect(output_settings.accept)
        self.buttonBox.rejected.connect(output_settings.reject)
        QtCore.QMetaObject.connectSlotsByName(output_settings)

    def retranslateUi(self, output_settings):
        _translate = QtCore.QCoreApplication.translate
        output_settings.setWindowTitle(_translate("output_settings", "Dialog"))
        self.label_2.setText(_translate("output_settings", "<html><head/><body><p><span style=\" text-decoration: underline;\">Change output name</span></p></body></html>"))
        self.label.setText(_translate("output_settings", "<html><head/><body><p><span style=\" text-decoration: underline;\">Change output variables</span></p></body></html>"))
        self.checkBox_3.setText(_translate("output_settings", "CheckBox"))
        self.checkBox.setText(_translate("output_settings", "CheckBox"))
        self.checkBox_2.setText(_translate("output_settings", "CheckBox"))
        self.checkBox_4.setText(_translate("output_settings", "CheckBox"))
        self.checkBox_5.setText(_translate("output_settings", "CheckBox"))
        self.checkBox_6.setText(_translate("output_settings", "CheckBox"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    output_settings = QtWidgets.QDialog()
    ui = Ui_output_settings()
    ui.setupUi(output_settings)
    output_settings.show()
    sys.exit(app.exec_())

