"""
This file contains the main GUI class that is used in the *Conditional game data analyse tool (CGDAT)* was created for a friend
of mine to help him with the data analysis he had to do for his graduation project. This tool is licences under the GPL open
source licence. You are therefore free use the source code in any way provided that you the original copyright statements.

Author:
    Rick Staa
Maintainer:
    Wesley Bosman

"""
# TODO: When a condition on a string variable is specified the user interfaces displays the condition not vallid error
# TODO: Create setup file
# TODO: Create time file chooser
# TODO: Create documentation
# TODO: Create time range setter
# TODO: Create column chooser settings menu
# TODO: Add xls option
# TODO: time data input file check for delimiter
# TODO: Check if time data file and data file are in the right format

### Import needed python modules ###
import sys
import pandas as pd
import numpy as np
import os
import xlsxwriter
import subprocess
import re
import time
import os
from PyQt5 import QtCore, QtGui, QtWidgets

### Get relative script path ###
dirname = os.path.dirname(os.path.abspath(__file__))

### Create the needed python user interface classes out of the QT UI files ###
subprocess.call(r"python -m PyQt5.uic.pyuic -x " + os.path.join(dirname, '..', r'qt\CGDAT.ui') + " -o " + os.path.join(dirname, '..', r'scripts\CGDAT_ui.py'))
subprocess.call(r"python -m PyQt5.uic.pyuic -x " + os.path.join(dirname, '..', r'qt\output_settings.ui') + " -o " + os.path.join(dirname, '..', r'scripts\output_settings_ui.py'))
subprocess.call(r"python -m PyQt5.uic.pyuic -x " + os.path.join(dirname, '..', r'qt\about.ui') + " -o " + os.path.join(dirname, '..', r'scripts\about_ui.py'))

### Import custom classes and functions ###
from qt_custom import Worker, WorkerSignals

### Import the python UI classes ###
from CGDAT_ui import Ui_MainWindow
from about_ui import Ui_about
from output_settings_ui import Ui_output_settings

#####################################################################
#### Script settings                                             ####
#####################################################################
sections = ["Speed","Acceleration"]
operators = ['>','>=','<','<=','==','&']
freq = 1000  # Data recording frequency [Hz]

#####################################################################
#### Overload Qt DataAnalyserGUI class                           ####
#####################################################################
class DataAnalyserGUI(Ui_MainWindow):
    """This is the qt class used to create the general user interface for the CGDAT data analysis tool.
    It inherits from the Ui_MainWindow class that is automatically created by the PyQt5.uic.pyuic converter.

    Args:
        Ui_MainWindow (CGDAT_ui.Ui_MainWindow): Python GUI class created out of the CGDAT.ui file by the PyQt5.uic.pyuic converter.

    """

    #########################################################
    #### Class initiation                                ####
    #########################################################
    def setupUi(self, MainWindow):
        '''The function which is used to set up the parts of the GUI that were not already defined in the CGDAT.ui file. Further it is
        also used to add functionalities to the objects in the generated qt GUI python class.

        Args:
            MainWindow (PyQt5.QtWidgets.QMainWindow): Python Main window object  created out of the CGDAT_ui.Ui_MainWindow class.
        '''
        super(DataAnalyserGUI, self).setupUi(MainWindow)  # Run parent initializer function

        ########################################
        ### Set main GUI menu items ############
        ########################################

        ### Setup about icon and menu action ###
        about_icon = os.path.join(dirname, '..', r'media\about_icon.svg')                   # About icon path
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(about_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon)  # Set icon
        self.actionAbout.triggered.connect(self.action_about_slot)  # Set slot

        ########################################
        ### Add settings buttons ###############
        ########################################

        ### Link input file chooser button signal to slot ###
        self.input_file_browser_btn.clicked.connect(self.get_input_file)

        ### Link output file chooser button signal to slot ###
        self.results_folder = os.path.normpath(os.path.join(dirname, '..', r'results')).replace("c:\\","C:\\")
        self.output_file_path.setText(self.results_folder)
        self.output_file_browser_btn.clicked.connect(self.get_output_dir)

        ### Link time sections chooser button signal to slot ###
        self.time_file_browser_btn.clicked.connect(self.get_time_sections_file)

        ########################################
        ### Create condition choicer grid ######
        ########################################

        ### Grid row counter ###
        self.conditions_grid_rows = 1  # Create variable to count the grid rows

        ### Create condition line edits ###
        self.condition_line_edit = []
        self.condition_line_edit.append(QtWidgets.QLineEdit(self.conditions_group_box))
        self.condition_line_edit[0].setObjectName("condition_line_edit_1")
        self.conditions_grid.addWidget(self.condition_line_edit[0], 0, 1, 1, 1)

        ### Create condition labels ###
        self.condition_label = []
        self.condition_label.append(QtWidgets.QLabel(self.conditions_group_box))
        self.condition_label[0].setObjectName("condition_label_1")
        self.condition_label[0].setText("1.")
        self.conditions_grid.addWidget(self.condition_label[0], 0, 0, 1, 1)

        ### Add a condition add button ###
        self.condition_add_row_btn = QtWidgets.QToolButton(self.conditions_group_box)
        self.condition_add_row_btn.setMinimumSize(QtCore.QSize(22, 22))
        self.condition_add_row_btn.setMaximumSize(QtCore.QSize(22, 22))
        self.condition_add_row_btn.setObjectName("condition_add_row_btn")
        self.condition_add_row_btn.setText("+")
        self.condition_add_row_btn.clicked.connect(self.add_conditions_row)
        self.conditions_grid.addWidget(self.condition_add_row_btn, 0, 2, 1, 1)

        ### Add a condition remove button ###
        self.condition_remove_row_btn = QtWidgets.QToolButton(self.conditions_group_box)
        self.condition_remove_row_btn.setMinimumSize(QtCore.QSize(22, 22))
        self.condition_remove_row_btn.setMaximumSize(QtCore.QSize(22, 22))
        self.condition_remove_row_btn.setObjectName("condition_remove_row_btn")
        self.condition_remove_row_btn.setText("-")
        self.condition_remove_row_btn.clicked.connect(self.remove_conditions_row)
        self.conditions_grid.addWidget(self.condition_remove_row_btn, 0, 3, 1, 1)

        ########################################
        ### Create data analyse menu ###########
        ########################################

        ### Create a reset grid button ###
        self.reset_conditions_grid_btn.clicked.connect(self.reset_conditions)

        ### Create data analyse button ###
        self.analyse_data_btn.clicked.connect(self.analyse_data)

        ### Create output settings button ###
        settings_icon = os.path.join(dirname, '..', r'media\settings_icon.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(settings_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.output_settings_btn.setIcon(icon)
        self.output_settings_btn.clicked.connect(self.set_settings)

    #########################################################
    #### GUI member functions                            ####
    #########################################################

    #################################################
    ### Menu action function                      ###
    #################################################
    def action_about_slot(self):
        '''Qt slot function created to display the about window. This slot is triggered when the about menu item is clicked or
        the user uses the F1 keyboard shortcut.
        '''
        about = QtWidgets.QDialog()
        ui = Ui_about()
        ui.setupUi(about)
        about.show()
        about.exec_()

    #################################################
    ### Get input file path function              ###
    #################################################
    def get_input_file(self):
        '''Qt slot function created to get a user specified input file. It is linked to the input_file_browser_btn and displays a
        file choicer dialog in which the user can specify the input data file.
        '''

        ### Create file dialog ###
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Select input file", "","CSV Files (*.csv)", options=options)
        fileName = os.path.normpath(fileName)

        ### Enable input field if not empty ###
        if not (fileName == "."):  # If empty
            self.input_file_path.setText(fileName)
            self.input_file_path.setEnabled(1)
        else:
            self.input_file_path.setText("")
            self.input_file_path.setEnabled(0)

    #################################################
    ### Get time sections file path function      ###
    #################################################
    def get_time_sections_file(self):
        '''Qt slot function created to get a user specified time sectsions input file. In this file the :samp:`begin times`
        and :samp:`End times` of the sections where the data analysis has to be performed are specified.
        It is linked to the time_file_browser_btn and displays a file choicer dialog in which the user can specify the input data file.
        '''

        ### Create file dialog ###
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getOpenFileName(None,"Select time sections file", "","CSV Files (*.csv)", options=options)
        fileName = os.path.normpath(fileName)

        ### Enable input field if not empty ###
        if not (fileName == "."):  # If empty
            self.time_file_path.setText(fileName)
            self.time_file_path.setEnabled(1)
        else:
            self.time_file_path.setText("")
            self.time_file_path.setEnabled(0)

    #################################################
    ### Get output folder file path function      ###
    #################################################
    def get_output_dir(self):
        '''Qt slot function created to get a user specified output folder. It is linked to the output_file_browser_btn_btn and displays a
        folder choicer dialog in which the user can specify the input data file. If no folder is specified the output files will
        be placed in a CGDAT/results folder which is placed in the windows documents folder.
        '''

        ### Create folder dialog ###
        folder_dir = QtWidgets.QFileDialog.getExistingDirectory(None, 'Select output directory')
        folder_dir = os.path.normpath(folder_dir).replace("c:\\","C:\\")

        ### Enable output field if user gave output folder input ###
        if folder_dir != ".": # If empty
            self.output_file_path.setText(folder_dir)
            self.output_file_path.setEnabled(1)
        else:
            self.output_file_path.setText(self.results_folder)
            self.output_file_path.setEnabled(0)

    #################################################
    ### Add extra condition row function          ###
    #################################################
    def add_conditions_row(self):
        '''Qt slot function created to add an extra condition row to the condition grid. It is linked to the
        condition_add_row_btn and triggered when the button is clicked.
        '''

        ### Get the nr of rows that are currently present in the condition grid ###
        rows = self.conditions_grid_rows

        ### Create new line edit ###
        self.condition_line_edit.append(QtWidgets.QLineEdit(self.conditions_group_box))
        condition_line_edit_obj_name = "condition_line_edit_" + str(rows+1)
        self.condition_line_edit[rows].setObjectName(condition_line_edit_obj_name)
        self.conditions_grid.addWidget(self.condition_line_edit[rows], rows, 1, 1, 1)

        ### Create new label ###
        self.condition_label.append(QtWidgets.QLabel(self.conditions_group_box))
        label_txt = str(rows+1) + "."
        condition_label_obj_name = "condition_label_obj_name_" + str(rows+1)
        self.condition_label[rows].setObjectName(condition_label_obj_name)
        self.condition_label[rows].setText(label_txt)
        self.conditions_grid.addWidget(self.condition_label[rows], rows, 0, 1, 1)

        ### Move condition buttons to new row ###
        self.conditions_grid.removeWidget(self.condition_add_row_btn)
        self.conditions_grid.removeWidget(self.condition_remove_row_btn)
        self.conditions_grid.addWidget(self.condition_add_row_btn, rows, 2, 1, 1)
        self.conditions_grid.addWidget(self.condition_remove_row_btn, rows, 3, 1, 1)

        ### Increase condition row counter ###
        self.conditions_grid_rows +=1

    #################################################
    ### Remove condition row function             ###
    #################################################
    def remove_conditions_row(self):
        '''Qt slot function created to add an extra condition row to the condition grid. It is linked to the
        condition_remove_row_btn and triggered when the button is clicked.
        '''

        ### Get the nr of rows that are currently present in the condition grid ###
        rows = self.conditions_grid_rows

        ### remove condition row if more than 1 row is present ###
        if rows != 1:

            ### Remove last condition row ###
            self.conditions_grid.removeWidget(self.condition_line_edit[(rows-1)])
            self.conditions_grid.removeWidget(self.condition_label[(rows-1)])
            self.condition_line_edit[(rows-1)].deleteLater()
            del self.condition_line_edit[(rows-1)]
            self.condition_label[(rows-1)].deleteLater()
            del self.condition_label[(rows-1)]

            ### Move condition buttons to new last row ###
            self.conditions_grid.removeWidget(self.condition_add_row_btn)
            self.conditions_grid.removeWidget(self.condition_remove_row_btn)
            self.conditions_grid.addWidget(self.condition_add_row_btn, (rows-2), 2, 1, 1)
            self.conditions_grid.addWidget(self.condition_remove_row_btn, (rows-2), 3, 1, 1)

            ### Decrement row counter ###
            self.conditions_grid_rows -=1

    #################################################
    ### Reset condition field function            ###
    #################################################
    def reset_conditions(self):
        '''Qt slot function created to reset the condition grid to its original state in which only condition row is present.
        It is linked to the reset_conditions_grid_btn.
        '''

        ### Remove all condition rows except one ###
        while self.conditions_grid_rows > 1:
            rows = self.conditions_grid_rows  # Get number of rows currently present

            ### Remove last row ###
            self.conditions_grid.removeWidget(self.condition_line_edit[(rows-1)])
            self.conditions_grid.removeWidget(self.condition_label[(rows-1)])
            self.condition_line_edit[(rows-1)].deleteLater()
            del self.condition_line_edit[(rows-1)]
            self.condition_label[(rows-1)].deleteLater()
            del self.condition_label[(rows-1)]

            ### Move condition buttons to new last row ###
            self.conditions_grid.removeWidget(self.condition_add_row_btn)
            self.conditions_grid.removeWidget(self.condition_remove_row_btn)
            self.conditions_grid.addWidget(self.condition_add_row_btn, (rows-2), 2, 1, 1)
            self.conditions_grid.addWidget(self.condition_remove_row_btn, (rows-2), 3, 1, 1)

            ### Decrement row counter ###
            self.conditions_grid_rows -=1

        ### Clean last condition row ###
        else:
            self.condition_line_edit[0].setText("")

    #################################################
    #### Set output settings function            ####
    #################################################
    def set_settings(self):
        '''Qt slot function created to display the settings dialog. In this settings dialog users can specify some
        extra settings:

        - The output file name. By default the output name is based on the current time.
        - The dataframe columns they want to include in the data analysis results file. By default
        only the columns that are present in the conditional statements are included.
        '''
        pass

    #########################################################
    #### Other functions                                 ####
    #########################################################

    #################################################
    #### Condition validity check function       ####
    #################################################
    def check_condition(self, condition_text):
        '''Qt slot function created to reset the condition grid to its original state in which only condition row is present.
        It is linked to the reset_conditions_grid_btn.
        '''

        ### Create vallid operator list ###
        operator_escape_str = [("\\"+ op) for op in operators]
        operator_str = "(" + "|".join(operator_escape_str) + ")"

        ### Split input command in list items ###
        validity_result = []  # True if conditional statement is vallid (Return variable)
        conditions_split = [x.strip() for x in re.split(operator_str, condition_text.text())]

        #################################################
        ### Check validity of condition statement #######
        #################################################

        ### Check if delimiters were placed right ###
        if any([(' ' in y) for y in conditions_split]):
            validity_result.append(False)  # Condition failed condition validity test
        else:
            validity_result.append(True)  # Condition passed condition validity test

        #################################################
        ### Check validity of operators #################
        #################################################
        symbols = [y.strip() for y in re.split(r"\w", condition_text.text())]  # Get all operators out of condition statemen

        ### Remove empty list items ###
        while '' in symbols: # Remove white spaces in trimmed
            symbols.remove('')

        ### Check if operators are valid ###
        if not any([sym in operators for sym in symbols]):
            validity_result.append(False)  # Operators failed the validity test
        else:
            validity_result.append(True)  # Operators passed the validity test

        #################################################
        ### Return test results #########################
        #################################################
        return any([not i for i in validity_result])


    #################################################
    #### Data analyse function                   ####
    #################################################
    def analyse_data(self):
        '''The function in which the data analysis is performed. The function uses the data present in the csv file
        which is specified in the input_file_path member variable. The data analysis is performed using the
        :func:`pandas.read_csv()` function which returns a pandas dataframe. Following the data in this dataframe
        is checked against the conditional statements specified in the conditions grid of the main GUI window.
        '''

        #################################################
        ### Check if input file path is not empty #######
        #################################################
        response_given = []
        for condition_text in self.condition_line_edit:
            response_given.append((len(condition_text.text()) == 0))

        ### Display message box when input file path is empty ###
        if not self.input_file_path.text():
            warn_dialog = QtWidgets.QMessageBox()
            warn_dialog.setIcon(QtWidgets.QMessageBox.Warning)
            warn_dialog.setWindowTitle('Warning')
            warn_dialog.setText('Please specify an input file.')
            warn_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
            warn_dialog.exec_()

        #################################################
        ### Check if conditions are not empty ###########
        #################################################
        elif any(response_given):

            ### Check which conditions are empty ###
            empty_indexes =  [i+1 for i, x in enumerate(response_given) if x]
            empty_indexes_error_str = ','.join(map(str, empty_indexes)) if len(empty_indexes) != 2 else ' & '.join(map(str, empty_indexes))

            ### Create warning dialog specifying the empty conditions ###
            warn_dialog = QtWidgets.QMessageBox()
            warn_dialog.setIcon(QtWidgets.QMessageBox.Warning)
            warn_dialog.setWindowTitle('Warning')
            warn_dialog.setTextFormat(QtCore.Qt.RichText)
            if len(empty_indexes) > 1:
                warn_dialog.setText("Conditions " + empty_indexes_error_str + " appear to be empty please specify a condition.")
            else:
                warn_dialog.setText("Condition " + empty_indexes_error_str + " appears to be empty please specify a condition.")
            warn_dialog.setInformativeText("<b>Example</b>: speed > 10 & speed < 15 & acceleration > 5 & acceleration < 8")
            warn_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
            warn_dialog.exec_()


        #################################################
        ### Check if condition statements are valid #####
        #################################################
        else:

            ### Check if all the given conditions are valid and not ###
            valid_bol_list = []
            for condition_text in self.condition_line_edit:
                valid_bol_list.append(self.check_condition(condition_text))

            ### Print error if conditions are not valid ###
            if any(valid_bol_list):

                ### Create warning information str ###
                error_idx_list = [ii+1 for ii, x in enumerate(valid_bol_list) if x == True]
                condition_error_str = ','.join(map(str, error_idx_list)) if len(error_idx_list) != 2 else ' & '.join(map(str, error_idx_list))

                ### Create warning dialog ###
                warn_dialog = QtWidgets.QMessageBox()
                warn_dialog.setIcon(QtWidgets.QMessageBox.Warning)
                warn_dialog.setWindowTitle('Warning')
                warn_dialog.setTextFormat(QtCore.Qt.RichText)
                if len(error_idx_list) > 1:
                    warn_dialog.setText('Some of your conditions are not valid please check conditions ' + condition_error_str + '. The accepted operators are (&gt;, &gt;=, &lt;, &lt;=, ==, &amp;)')
                else:
                    warn_dialog.setText('One of your conditions is not valid please check condition ' + condition_error_str + '. The accepted operators are (&gt;, &gt;=, &lt;, &lt; =, ==, &amp;)')

                warn_dialog.setInformativeText("<b>Example</b>: speed > 10 & speed < 15 & acceleration > 5 & acceleration < 8")
                warn_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
                warn_dialog.exec_()

            #################################################
            ### Perform data analysis #######################
            #################################################
            else:

                ### Import the csv file###
                df = pd.read_csv(self.input_file_path.text(), header=0, encoding='utf-8')
                df.columns = df.columns.str.title()  # Capitalize columns to prohibit key errors

                ### Create data writer  object ###
                timestr = time.strftime("%Y%m%d-%H%M%S")  # Create filename for output file (based on time data)
                output_file_path = os.path.join(self.output_file_path.text(), (timestr + r'.xlsx'))  # Create output file path
                writer = pd.ExcelWriter(output_file_path, engine='xlsxwriter')  # Create data writer

                ### Perform data analysis on each condition ###
                key_invalid = []  # Create list for key_vallid boolean test
                counter = 1  # Condition counter used in print statement
                for condition_text in self.condition_line_edit:

                    ### Create list with valid operators ###
                    operator_escape_str = [("\\"+ op) for op in operators]
                    operator_str = "(" + "|".join(operator_escape_str) + ")"

                    ### Split command in individual list items ###
                    condition_tmp_1 = [x.strip() for x in re.split(operator_str, condition_text.text())]

                    ### Warp database name around keywords ###
                    condition_tmp_2 = [("df[\""+ w.capitalize()+"\"]") if w.isalpha() else w for w in condition_tmp_1]
                    condition_tmp_3 = " ".join(condition_tmp_2)
                    condition_split_3 = [x.strip() for x in re.split(r"&", condition_tmp_3)]
                    condition = " & ".join(["(" + item + ")" for item in condition_split_3])

                    #################################################
                    ### Filter data based on time sections ##########
                    #################################################
                    # If a time section file was specified in the   #
                    # time_sections_file_path filter the data based #
                    # on theses specified time sections.            #
                    #################################################

                    ### Get data out of specified time sections file ###
                    df_time = pd.read_csv(self.time_file_path.text(), header=0, encoding="utf-8", sep=';')
                    df_time.columns = df_time.columns.str.title()  # Make sure the columns are capitalized

                    ### Create extra time column ###
                    df['Time'] = df['Timestamp']*(1/freq)
                    df.index = pd.to_datetime(df['Time'], unit='s')

                    ### Filter the data based on time sections when time section file is specified ###
                    if self.input_file_path.text():

                        ### Convert begin and start times to datetime format ###
                        begin_times = pd.to_datetime(df_time['Start Time'], format='%H:%M:%S.%f').dt.time  # List containing section begin times
                        end_times = pd.to_datetime(df_time['End Time'], format='%H:%M:%S.%f').dt.time  # List containing sections end times

                        ### Get data within specific time ranges ###
                        df_sections = [df.between_time(i, j) for (i,j) in zip(begin_times, end_times)]
                        df = pd.concat(df_sections) # Add all the dataframes of the time_sections together again

                    #################################################
                    ### Check data against conditions################
                    #################################################
                    try:
                        df_condition = df[eval(condition)]
                        key_invalid.append(False)  # Save key value check result

                        ### Get keywords that are used in the condition ###
                        keywords = [w.capitalize() for w in condition_tmp_1 if w.isalpha()]
                        # keywords.append('Time')  # Add newly created time variable to results dataframe

                        ### Remove not specified vars (columns) out of dataframe ###
                        df_filter = df_condition[keywords]

                        ### print data to excel file ###
                        df_filter.to_excel(writer, sheet_name=condition_text.text())

                        ### Save that the key was vallid ###
                        key_invalid.append(False)

                    ### If not vallid save what went wrong ###
                    except KeyError as e:
                        key_invalid.append(True)  # Save key value check result
                        print(e)  # Print error

                ### If keys were not vallid display error message ###
                if any(key_invalid):

                        ### Make key condition index error display string ###
                        key_invalid_idx_list = [ii+1 for ii, x in enumerate(key_invalid) if x == True]
                        key_condition_error_str = ', '.join(map(str, key_invalid_idx_list)) if len(key_invalid_idx_list) != 2 else ' & '.join(map(str, key_invalid_idx_list))
                        key_vallid_list = df.columns
                        key_vallid_list_error_str = ', '.join(map(str, key_vallid_list)) if len(key_vallid_list) != 2 else ' & '.join(map(str, key_vallid_list))

                        ### Print warning message ###
                        warn_dialog = QtWidgets.QMessageBox()
                        warn_dialog.setIcon(QtWidgets.QMessageBox.Warning)
                        warn_dialog.setWindowTitle('Warning')
                        if len(key_invalid_idx_list) > 1:
                            warn_dialog.setText('Unfortunately some of your conditions contain invalid variables please check conditions ' + key_condition_error_str + ' again.')
                        else:
                            warn_dialog.setText('Unfortunately one of your conditions contain invalid variables please check condition ' + key_condition_error_str + ' again.')
                        warn_dialog.setInformativeText("<b>Vallid keys</b>: " + key_vallid_list_error_str)
                        warn_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
                        warn_dialog.exec_()

                ### Otherwise save results to xlsx file ###
                else:
                    writer.save()

                    ### Print analyse completed message ###
                    analyse_dialog = QtWidgets.QMessageBox()
                    analyse_dialog.setIcon(QtWidgets.QMessageBox.Information)
                    analyse_dialog.setWindowTitle('Info')
                    analyse_dialog.setText("Data analysis complete you can find the file in the specified output folder")
                    analyse_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
                    analyse_dialog.exec_()

##############################################################
#### Main window function                                 ####
##############################################################
if __name__ == '__main__':
    '''The main script running the CGDAT GUI
    '''

    ### Create QT app ###
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ### Create Main window ###
    ui = DataAnalyserGUI()
    ui.setupUi(MainWindow)

    ### Set icon ###
    CGDAT_icon = os.path.join(dirname, '..', r'media\CGDAT.svg')
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(CGDAT_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    MainWindow.setWindowIcon(icon)

    ### Show main window ###
    MainWindow.show()
    sys.exit(app.exec_())

