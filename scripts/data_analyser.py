""" Data Analyse Tool
    This tool can be used to analyse game data.
"""
# -*- coding: utf-8 -*-

### Import python modules ###
import sys
import pandas as pd
import numpy as np
import os
import xlsxwriter
import subprocess
import re

### Create python UI class ###
subprocess.call(r"python -m PyQt5.uic.pyuic -x C:\Users\ricks\OneDrive\Work\Wesley\qt\data_analyse.ui -o C:\Users\ricks\OneDrive\Work\Wesley\scripts\data_analyse_ui.py")
subprocess.call(r"python -m PyQt5.uic.pyuic -x C:\Users\ricks\OneDrive\Work\Wesley\qt\about.ui -o C:\Users\ricks\OneDrive\Work\Wesley\scripts\about_ui.py")
subprocess.call(r"python -m PyQt5.uic.pyuic -x C:\Users\ricks\OneDrive\Work\Wesley\qt\output_settings.ui -o C:\Users\ricks\OneDrive\Work\Wesley\scripts\output_settings_ui.py")

### Import UI modules ###
from data_analyse_ui import Ui_MainWindow
from about_ui import Ui_about
# from output_settings_ui import UI
from PyQt5 import QtCore, QtGui, QtWidgets

### Get relative path ###
import os
dirname = os.path.dirname(os.path.abspath(__file__))
print dirname

##############################################################
#### Script settings                                      ####
##############################################################
sections = ["Speed","Acceleration"]
operators = ['>','>=','<','<=','==','&']

##############################################################
#### Overload QTCReator class                             ####
##############################################################
class DataAnalyserGUI(Ui_MainWindow):

    ##########################################################
    #### Class initiationn                                ####
    ##########################################################
    def setupUi(self, MainWindow):
        super(DataAnalyserGUI, self).setupUi(MainWindow)

        ### Set menu items ###
        about_icon = os.path.join(dirname, '..', r'media\about_icon.svg')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(about_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon)
        self.actionAbout.triggered.connect(self.action_about_slot)

        ### Link input file choice button ###
        self.input_file_browser.clicked.connect(self.get_input_file)
        results_folder = os.path.normpath(os.path.join(dirname, 'results')).replace("c:\\","C:\\")
        self.output_file_path.setText(results_folder)
        self.output_file_browser.clicked.connect(self.get_output_dir)

        ### Create conditions grid ###
        ## Create Line edit ##
        self.conditions_grid_rows = 0
        self.condition_line_edit = []
        self.condition_line_edit.append(QtWidgets.QLineEdit(self.conditions_group_box))
        self.condition_line_edit[0].setObjectName("condition_line_edit_1")
        self.conditions_grid.addWidget(self.condition_line_edit[0], 0, 1, 1, 1)

        ## Create Label ##
        self.condition_label = []
        self.condition_label.append(QtWidgets.QLabel(self.conditions_group_box))
        self.condition_label[0].setObjectName("condition_label_1")
        self.condition_label[0].setText("1.")
        self.conditions_grid.addWidget(self.condition_label[0], 0, 0, 1, 1)

        ## Add condition add and remove buttons to last condition ##
        self.condition_add_row_btn = QtWidgets.QToolButton(self.conditions_group_box)
        self.condition_add_row_btn.setMinimumSize(QtCore.QSize(22, 22))
        self.condition_add_row_btn.setMaximumSize(QtCore.QSize(22, 22))
        self.condition_add_row_btn.setObjectName("condition_add_row_btn")
        self.condition_add_row_btn.setText("+")
        self.condition_add_row_btn.clicked.connect(self.add_conditions_row)
        self.conditions_grid.addWidget(self.condition_add_row_btn, 0, 2, 1, 1)
        self.condition_remove_row_btn = QtWidgets.QToolButton(self.conditions_group_box)
        self.condition_remove_row_btn.setMinimumSize(QtCore.QSize(22, 22))
        self.condition_remove_row_btn.setMaximumSize(QtCore.QSize(22, 22))
        self.condition_remove_row_btn.setObjectName("condition_remove_row_btn")
        self.condition_remove_row_btn.setText("-")
        self.condition_remove_row_btn.clicked.connect(self.remove_conditions_row)
        self.conditions_grid.addWidget(self.condition_remove_row_btn, 0, 3, 1, 1)

        ## Increase row count ##
        self.conditions_grid_rows +=1

        ### Create data analyse buttons ###
        ## Create reset grid button ##
        self.reset_conditions_grid_btn.clicked.connect(self.reset_conditions)

        ## Create data analyse button ##
        self.analyse_data_btn.clicked.connect(self.analyse_data)

        ## Create output settings button ##
        settings_icon = os.path.join(dirname, '..', r'media\settings_icon.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(settings_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.output_settings_btn.setIcon(icon)
        self.output_settings_btn.clicked.connect(self.output_settings_set)

    ##########################################################
    #### GUI member functions                             ####
    ##########################################################

    ### Menu action function ###
    def action_about_slot(self):
        about = QtWidgets.QDialog()
        ui = Ui_about()
        ui.setupUi(about)
        about.show()
        about.exec_()

    ### Input file selection button slot ###
    def get_input_file(self):
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Select input file", "","CSV Files (*.csv)", options=options)
        fileName = os.path.normpath(fileName)

        ### Check if not empty and enable field ###
        if fileName:
            self.input_file_path.setText(fileName)
            self.input_file_path.setEnabled(1)
        else:
            self.input_file_path.setEnabled(0)

    ### Output file selection button slot ###
    def get_output_dir(self):
        folder_dir = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select output directory')
        folder_dir = os.path.normpath(folder_dir).replace("c:\\","C:\\")

        ### Check if not empty and enable field ###
        if folder_dir:
            self.output_file_path.setText(folder_dir)
            self.output_file_path.setEnabled(1)
        else:
            self.output_file_path.setEnabled(0)

    ### Add condition row slot ###
    def add_conditions_row(self):
        rows = self.conditions_grid_rows # Get number of rows

        ## Create Line edit ##
        self.condition_line_edit.append(QtWidgets.QLineEdit(self.conditions_group_box))
        condition_line_edit_obj_name = "condition_line_edit_" + str(rows+1)
        self.condition_line_edit[rows].setObjectName(condition_line_edit_obj_name)
        self.conditions_grid.addWidget(self.condition_line_edit[rows], rows, 1, 1, 1)

        ## Create Label ##
        self.condition_label.append(QtWidgets.QLabel(self.conditions_group_box))
        label_txt = str(rows+1) + "."
        condition_label_obj_name = "condition_label_obj_name_" + str(rows+1)
        self.condition_label[rows].setObjectName(condition_label_obj_name)
        self.condition_label[rows].setText(label_txt)
        self.conditions_grid.addWidget(self.condition_label[rows], rows, 0, 1, 1)

        ## Change condition buttons to new row ##
        self.conditions_grid.removeWidget(self.condition_add_row_btn)
        self.conditions_grid.removeWidget(self.condition_remove_row_btn)
        self.conditions_grid.addWidget(self.condition_add_row_btn, rows, 2, 1, 1)
        self.conditions_grid.addWidget(self.condition_remove_row_btn, rows, 3, 1, 1)

        ## Increase number of rows
        self.conditions_grid_rows +=1

    ### remove condition row slot ###
    def remove_conditions_row(self):
        rows = self.conditions_grid_rows # Get number of rows

        ## If more than 1 row left ##
        if rows != 1:

            ## Remove last rows ##
            self.conditions_grid.removeWidget(self.condition_line_edit[(rows-1)])
            self.conditions_grid.removeWidget(self.condition_label[(rows-1)])
            self.condition_line_edit[(rows-1)].deleteLater()
            del self.condition_line_edit[(rows-1)]
            self.condition_label[(rows-1)].deleteLater()
            del self.condition_label[(rows-1)]

            ## Change condition buttons to new row ##
            self.conditions_grid.removeWidget(self.condition_add_row_btn)
            self.conditions_grid.removeWidget(self.condition_remove_row_btn)
            self.conditions_grid.addWidget(self.condition_add_row_btn, (rows-2), 2, 1, 1)
            self.conditions_grid.addWidget(self.condition_remove_row_btn, (rows-2), 3, 1, 1)

            ## Remove row count
            self.conditions_grid_rows -=1

    ### Check line edit conditions slot ###
    def reset_conditions(self):

        ## Remove all rows except one ##
        while self.conditions_grid_rows > 1:
            rows = self.conditions_grid_rows # Get number of rows

            ## Remove last rows ##
            self.conditions_grid.removeWidget(self.condition_line_edit[(rows-1)])
            self.conditions_grid.removeWidget(self.condition_label[(rows-1)])
            self.condition_line_edit[(rows-1)].deleteLater()
            del self.condition_line_edit[(rows-1)]
            self.condition_label[(rows-1)].deleteLater()
            del self.condition_label[(rows-1)]

            ## Change condition buttons to new row ##
            self.conditions_grid.removeWidget(self.condition_add_row_btn)
            self.conditions_grid.removeWidget(self.condition_remove_row_btn)
            self.conditions_grid.addWidget(self.condition_add_row_btn, (rows-2), 2, 1, 1)
            self.conditions_grid.addWidget(self.condition_remove_row_btn, (rows-2), 3, 1, 1)

            ## Remove row count
            self.conditions_grid_rows -=1

    ##########################################################
    #### Output settings function slot                     ####
    ##########################################################
    def output_settings_set(self):
        pass

    ##########################################################
    #### Condition input check functio                    ####
    ##########################################################
    def check_condition(self, condition_text):

        ## Create operator list command ##
        operator_escape_str = [("\\"+ op) for op in operators]
        operator_str = "(" + "|".join(operator_escape_str) + ")"

        ## Split command in list items ##
        validity_result = []
        conditions_split = [x.strip() for x in re.split(operator_str, condition_text.text())]

        ## Check if deliminators were placed right ##
        if any([(' ' in y) for y in conditions_split]):
            validity_result.append(False)
        else:
            validity_result.append(True)
        ## Check if operators are correct ##
        symbols = [y.strip() for y in re.split(r"\w", condition_text.text())]  # Remove not symbols
        while '' in symbols:  # Remove white spaces
            symbols.remove('')
        if not any([sym in operators for sym in symbols]):
            validity_result.append(False)
        else:
            validity_result.append(True)

        # ## Check if right keywords are used ##
        # keywords = [w.lower() for w in conditions_split if w.isalpha()]
        # sections_lower = [j.lower() for j in sections]
        # keyword_is_valid = [(elem in sections_lower) for elem in keywords]
        # if not any(keyword_is_valid):
        #     validity_result.append(False)
        # else:
        #     validity_result.append(True)

        ## Return the result of the check ##
        # print validity_result
        return any([not i for i in validity_result])

    ##########################################################
    #### Data analyse function                            ####
    ######a####################################################
    def analyse_data(self):

        ### Check if input file is given ###
        if not self.input_file_path.text():
            warn_dialog = QtWidgets.QMessageBox()
            warn_dialog.setIcon(QtWidgets.QMessageBox.Warning)
            warn_dialog.setWindowTitle('Warning')
            warn_dialog.setText('Please specify an input file.')
            warn_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
            warn_dialog.exec_()

        ### Check if condition is not empty ###
        elif len(self.condition_line_edit) == 0:

            ## Create warning dialog ##
            warn_dialog = QtWidgets.QMessageBox()
            warn_dialog.setIcon(QtWidgets.QMessageBox.Warning)
            warn_dialog.setWindowTitle('Warning')
            warn_dialog.setText('Your conditions appear to be empty please specify a condition.')
            warn_dialog.setInformativeText('Example: speed > 10 & speed < 15 & acceleration > 5 & acceleration < 8')
            warn_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
            warn_dialog.exec_()

        ### Check if condition expressions are vallid ###
        else:

            ### Check if all the given conditions are valid and not ###
            valid_bol_list = []
            for condition_text in self.condition_line_edit:
                valid_bol_list.append(self.check_condition(condition_text))

            ### Print error if conditions are not valid ###
            if any(valid_bol_list):

                ## Create warning information ##
                error_idx_list = [ii for ii, x in enumerate(valid_bol_list) if x == True]
                error_idx_list = [jj + 1 for jj in error_idx_list]
                condition_error_str = ','.join(map(str, error_idx_list)) if len(error_idx_list) != 2 else ' & '.join(map(str, error_idx_list))

                ## Create warning dialog ##
                warn_dialog = QtWidgets.QMessageBox()
                warn_dialog.setIcon(QtWidgets.QMessageBox.Warning)
                warn_dialog.setWindowTitle('Warning')
                warn_dialog.setText('Your conditions are not valid please check condition ' + condition_error_str + ' and try again. The accepted operators are >, >=, <, <=, == and &')
                warn_dialog.setInformativeText('Example: speed > 10 & speed < 15 & acceleration > 5 & acceleration < 8')
                warn_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
                warn_dialog.exec_()

            ### Perform data analyse if conditions are valid ###
            else:

                ### import the csv file, note that the encoding has been set to ANSI###
                df = pd.read_csv(self.input_file_path.text(), header=0, low_memory=False) #, encoding = "ANSI")
                df.columns = map(str.capitalize, df.columns)  # Capitalize collumns to prohibit key errors

                ### Perform data analysis per condition ###
                counter = 1
                for condition_text in self.condition_line_edit:

                    ## Create operator list command ##
                    operator_escape_str = [("\\"+ op) for op in operators]
                    operator_str = "(" + "|".join(operator_escape_str) + ")"

                    ## Split command in list items ##
                    condition_tmp_1 = [x.strip() for x in re.split(operator_str, condition_text.text())]

                    ## warp database around keywords ##
                    condition_tmp_2 = [("df[\""+ w.capitalize()+"\"]") if w.isalpha() else w for w in condition_tmp_1]
                    condition_tmp_3 = " ".join(condition_tmp_2)
                    condition_split_3 = [x.strip() for x in re.split(r"&", condition_tmp_3)]
                    condition = " & ".join(["(" + item + ")" for item in condition_split_3])

                    ## Evaluate condition ##
                    try:
                        df_condition = df[eval(condition)]
                        print df_condition
                    except KeyError as e:
                        warn_dialog = QtWidgets.QMessageBox()
                        warn_dialog.setIcon(QtWidgets.QMessageBox.Warning)
                        warn_dialog.setWindowTitle('Warning')
                        warn_dialog.setText(e.args[0] + " is not a valid key check condition " + str(counter) + " and try again")
                        warn_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        warn_dialog.exec_()

                    ## Print result to datasheet and save ##
                    keywords = [w.capitalize() for w in condition_text.text() if w.isalpha()]

                ## increase counter
                counter += 1


##############################################################
#### Main window                                          ####
##############################################################
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = DataAnalyserGUI()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


# conditions = ["Speed > 10 & Acceleration > 0.69",
#               "Speed > 10 & Acceleration > 1.30",
#               "Speed > 7.5 & Acceleration > 1.30",
#               "Speed > 7.5 & Acceleration < (-1.30)",
#               "Acceleration > 7.50 & Acceleration < -1.30",
#               "Speed => Acceleration"
#              ]

# ### Get current path ###
# dirname = os.path.dirname(__file__)

# ### import the csv file, note that the encoding has been set to ANSI###
# filename = os.path.join(dirname, r'data\test.csv')
# df = pd.read_csv(filename, header=0, low_memory=False) #, encoding = "ANSI")

# ### Specify Conditions ###
# condition1 = ((df['Speed'] > 10) & (df['Acceleration'] > 0.69))
# condition2 = ((df['Speed'] > 10) & (df['Acceleration'] > 1.30))
# condition3 = ((df['Speed'] > 7.5) & (df['Acceleration'] > 1.30))
# condition4 = ((df['Speed'] > 7.5) & (df['Acceleration'] < (-1.30)))

# ### Test conditions ###
# df_sub_1 = df[condition1]
# df_sub_2 = df[condition2]
# df_sub_3 = df[condition3]
# df_sub_4 = df[condition4]

# idx = np.where(condition3.values == True)[0]
# for item2 in idx:
#     condition1[item2-2]

# ### Only get collumns you want ###
# df_sub_1 = df_sub_1[['Speed','Acceleration']]
# df_sub_2 = df_sub_2[['Speed','Acceleration']]
# df_sub_3 = df_sub_3[['Speed','Acceleration']]
# df_sub_4 = df_sub_4[['Speed','Acceleration']]


# # ### Get data around found times ###

# # ### Save in excel file ###
# # # Each condition on one sheet

# # # Create a Pandas Excel writer using XlsxWriter as the engine.
# # filename = os.path.join(dirname, 'data_analyse_result.xlsx')
# # writer = pd.ExcelWriter(filename, engine='xlsxwriter')

# # # df.to_excel(writer, sheet_name='Sheet1')
# # df_sub_1.to_excel(writer, sheet_name='Condition1')
# # df_sub_2.to_excel(writer, sheet_name='Condition2')
# # df_sub_3.to_excel(writer, sheet_name='Condition3')
# # df_sub_4.to_excel(writer, sheet_name='Condition4')
# # writer.save()


# # def game_analyse(input_file, output_path, output_name, condition_list):


### Condition add ###
### Create conditions grid ###
# self.condition_line_edit = []
# self.condition_label = []
# for condition in range(1): # Loop through rows

#     ## Create Line edit ##
#     self.condition_line_edit.append(QtWidgets.QLineEdit(self.conditions_group_box))
#     condition_label_obj_name = "condition_line_edit_" + str(condition + 1)
#     print str(len(self.condition_line_edit))
#     self.condition_line_edit[condition].setObjectName(condition_label_obj_name)
#     self.conditions_grid.addWidget(self.condition_line_edit[condition], condition, 1, 1, 1)

#     ## Create Label ##
#     self.condition_label.append(QtWidgets.QLabel(self.conditions_group_box))
#     condition_label_obj_name = "condition_label_" + str(condition + 1)
#     self.condition_label[condition].setObjectName(condition_label_obj_name)
#     label_txt = str(condition + 1) + "."
#     self.condition_label[condition].setText(label_txt)
#     self.conditions_grid.addWidget(self.condition_label[condition], condition, 0, 1, 1)

# ## Add condition add and remove buttons to last condition ##
# rows = self.conditions_grid.rowCount() # Get number of rows
# print "rows:" + str(rows)
# self.condition_add_row_btn = QtWidgets.QToolButton(self.conditions_group_box)
# self.condition_add_row_btn.setMinimumSize(QtCore.QSize(22, 22))
# self.condition_add_row_btn.setMaximumSize(QtCore.QSize(22, 22))
# self.condition_add_row_btn.setObjectName("condition_add_row_btn")
# self.condition_add_row_btn.setText("+")
# self.conditions_grid.addWidget(self.condition_add_row_btn, (rows-1), 2, 1, 1)
# self.condition_remove_row_btn = QtWidgets.QToolButton(self.conditions_group_box)
# self.condition_remove_row_btn.setMinimumSize(QtCore.QSize(22, 22))
# self.condition_remove_row_btn.setMaximumSize(QtCore.QSize(22, 22))
# self.condition_remove_row_btn.setObjectName("condition_remove_row_btn")
# self.condition_remove_row_btn.setText("-")
# self.conditions_grid.addWidget(self.condition_remove_row_btn, (rows-1), 3, 1, 1)
