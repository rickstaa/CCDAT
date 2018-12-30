# -*- coding: utf-8 -*-
"""
This file contains the main GUI class that is used in the *Conditional game data analyse tool (CGDAT)* was created for a friend
of mine to help him with the data analysis he had to do for his graduation project. This tool is licensed under the GPL open source license.
You are therefore free use the source code in any way provided that you the original copyright statements.

Author:
    Rick Staa
Maintainer:
    Wesley Bosman

"""

# TODO: Create setup file
# TODO: Create documentation
# TODO: Create time range setter
# TODO: Create column chooser settings menu
# TODO: Add xls option
# TODO: time data input file check for delimiter
# TODO: Check if time data file and data file are in the right format
# TODO: Multithread key error
# TODO: Wrong input files
# TODO: Link documentation

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
from datetime import datetime

### Get relative script path ###
dirname = os.path.dirname(os.path.abspath(__file__))

### Create the needed python user interface classes out of the QT UI files ###
subprocess.call(r"python -m PyQt5.uic.pyuic -x " + os.path.join(dirname, '..', r'qt\cgdat.ui') + " -o " + os.path.join(dirname, '..', r'scripts\qt_ui\cgdat_ui.py'))
subprocess.call(r"python -m PyQt5.uic.pyuic -x " + os.path.join(dirname, '..', r'qt\output_settings.ui') + " -o " + os.path.join(dirname, '..', r'scripts\qt_ui\output_settings_ui.py'))
subprocess.call(r"python -m PyQt5.uic.pyuic -x " + os.path.join(dirname, '..', r'qt\about.ui') + " -o " + os.path.join(dirname, '..', r'scripts\qt_ui\about_ui.py'))
subprocess.call(r"python -m PyQt5.uic.pyuic -x " + os.path.join(dirname, '..', r'qt\progress_dialog.ui') + " -o " + os.path.join(dirname, '..', r'scripts\qt_ui\progress_dialog_ui.py'))

### Import custom classes and functions ###
from qt_custom import Worker, WorkerSignals
from qt_custom import CheckableComboBox
from qt_custom.qt_extra2 import multiSelectMenu

### Import the python UI classes ###
from qt_ui import Ui_MainWindow
from qt_ui import Ui_About
from qt_ui import Ui_OutputSettings
from qt_ui import Ui_ProgressDialog

#####################################################################
#### Script settings                                             ####
#####################################################################
sections = ["Speed","Acceleration"]
operators = ['>','>=','<','<=','==','&']
freq = 0.166667/100  # Data recording frequency [Hz]

#####################################################################
#### Overload Qt DataAnalyserGUI class                           ####
#####################################################################
class DataAnalyserGUI(Ui_MainWindow):
    """This is the qt class used to create the general user interface for the CGDAT data analysis tool.
    It inherits from the Ui_MainWindow class that is automatically created by the PyQt5.uic.pyuic converter.

    Args:
        Ui_MainWindow (CGDAT_ui.Ui_MainWindow): Python GUI class created out of the CGDAT.ui file by the PyQt5.uic.pyuic converter.

    """

    # #########################################################
    # #### Class initiation                                ####
    # #########################################################
    # # Done to make sure new objects can be passed during    #
    # # the initiation.                                       #
    # #########################################################
    # def __init__(self, *args, **kwargs):
    #     super(DataAnalyserGUI, self).__init__(*args, **kwargs)

    #########################################################
    #### UI initiation                                   ####
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
        about_icon = os.path.join(dirname, '..', r'media\about_icon.svg')                      # About icon path
        self.toggle_icon_on = os.path.abspath(os.path.join(dirname, "..", "media/toggle_on.png")).replace('\\','/')    # Toggle on icon
        self.toggle_icon_off = os.path.abspath(os.path.join(dirname, "..", "media/toggle_off.png")).replace('\\','/')  # Toggle off icon

        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(about_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon)  # Set icon
        self.actionAbout.triggered.connect(self.action_about_slot)  # Set slot

        ########################################
        ### Add file settings buttons ##########
        ########################################

        ### Link input file chooser button signal to slot ###
        self.input_file_browser_btn.clicked.connect(self.get_input_file)

        ### Link output file chooser button signal to slot ###
        self.results_folder = os.path.normpath(os.path.join(dirname, '..', r'results')).replace("c:\\","C:\\")
        self.output_file_path.setText(self.results_folder)
        self.output_file_browser_btn.clicked.connect(self.get_output_dir)

        ########################################
        ### Add additional options #############
        ########################################

        ### Setup time range option ###
        self.time_file_toggle.setStyleSheet("QCheckBox::indicator:checked {image: url('"+self.toggle_icon_on+"');}\n QCheckBox::indicator:unchecked {image: url('"+self.toggle_icon_off+"');}")
        # self.time_file_toggle.clicked.connect(self.toggle_time_file_settings)
        self.time_file_browser_btn.clicked.connect(self.get_time_sections_file)

        ### Setup time range option ###
        self.time_range_toggle.setStyleSheet("QCheckBox::indicator:checked {image: url('"+self.toggle_icon_on+"');}\n QCheckBox::indicator:unchecked {image: url('"+self.toggle_icon_off+"');}")
        # self.time_range_toggle.clicked.connect(self.toggle_time_range_settings)

        ### Setup player filter option ###
        self.player_filter_toggle.setStyleSheet("QCheckBox::indicator:checked {image: url('"+self.toggle_icon_on+"');}\n QCheckBox::indicator:unchecked {image: url('"+self.toggle_icon_off+"');}")
        # self.player_filter_toggle.clicked.connect(self.toggle_player_filter_settings)
        # self.player_filter_drop_down_menu = multiSelectMenu()
        self.player_filter_combo_box = CheckableComboBox("-- To filter by player please input a data file --")
        self.player_filter_combo_box.setObjectName("player_filter_choicer")
        self.additional_options_layout.addWidget(self.player_filter_combo_box, 2, 2, 1, 1)
        self.player_filter_combo_box.setEnabled(0)

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
        self.analyse_data_btn.clicked.connect(self.start_data_analysis)

        ### Create output settings button ###
        settings_icon = os.path.join(dirname, '..', r'media\settings_icon.png')
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(settings_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.output_settings_btn.setIcon(icon)
        self.output_settings_btn.clicked.connect(self.set_settings)

        ########################################
        ### Create GUI multithread pool ########
        ########################################
        # self.threadpool = QtCore.QThreadPool()

        ### Print threading info ###
        # print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        ########################################
        ### Create data analyse progress bar ###
        ########################################
        # self.progress = QtGui.QProgressBar(self)
        # self.progress.setGeometry(200, 80, 250, 20)

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
        ui = Ui_About()
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

            ### Create worker that checks if the data file is vallid ###
            self.data_input_worker = Worker(self.analyse_input_data_file)  # Any other args, kwargs are passed to the run function

            ### Connect worker signals ###
            # self.data_input_worker.signals.result.connect(self.print_output)  # Results signal slot

            ### Start Worker ###
            self.data_input_worker.start()

            ### Enable input file display widget ###
            self.input_file_path.setText(fileName)
            self.input_file_path.setEnabled(1)

            ### Disable player filter combobox and remove options ###
            self.player_filter_combo_box.setEnabled(1)
            self.player_filter_combo_box.clear()
        else:

            ### Disable input file display widget ###
            self.input_file_path.setText("")
            self.input_file_path.setEnabled(0)

            ### Disable player filter combobox and remove options ###
            self.player_filter_combo_box.setDefaultTextHolder("-- To filter by player please input a data file --")
            self.player_filter_combo_box.clear()
            self.player_filter_combo_box.setEnabled(0)

    #################################################
    ### Get input file path function              ###
    #################################################
    def analyse_input_data_file(self, progress_callback):
        '''Qt slot function that is used to check if the data file is vallid and following add the available players to the player filter comboBox. This slot function is
        run in a worker thread so it does not freeze the GUI.
        '''

        ### Import the csv file ###
        self.df = pd.read_csv(self.input_file_path.text(), header=0, encoding='utf-8')
        self.df.columns = self.df.columns.str.title()  # Capitalize columns to prohibit key errors

        ## TODO: If contains player column
        ## TODO: Display data hasn't yet loaded popup
        ### Get the players present in the data file ###
        self.players = np.unique(self.df["Name"].tolist()).tolist()  # Get unique players
        self.players = [player for player in self.players if player not in ('ball', 'nan')]  # Remove nan and ball

        ### Add players to player filter QComboBox ###
        self.player_filter_combo_box.setDefaultTextHolder("-- Please select the players for whom you want to perform the data analysis --")
        self.player_filter_combo_box.clear()
        self.player_filter_combo_box.addItem("All players")
        for player in self.players:
            self.player_filter_combo_box.addItem(player)

    #################################################
    ### Toggle time file settings fields          ###
    #################################################
    def toggle_time_file_settings(self):
        '''Qt slot function used to disable and enable the time file settings fields based on whether the time file filter option is enabled.
        '''

        ### Enable input field if time file filter is enabled ###
        if self.time_file_toggle.checkState():  # If checked
            self.time_file_browser_btn.setEnabled(1)
        else:
            self.time_file_browser_btn.setEnabled(0)

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
            if (self.time_file_path.text() == ""):  # If no file has been specified yet
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
    def check_condition(self):
        '''Qt slot function created to check whether the conditions have the right format.

        Args:
            condition_text (str): The condition text.

        Returns:
            bool: Boolean specifying whether the condition format is correct.
        '''

        #################################################
        ### Check if input file path is not empty #######
        #################################################

        ### Display message box when input file path is empty ###
        if not self.input_file_path.text():
            warn_dialog = QtWidgets.QMessageBox()
            warn_dialog.setIcon(QtWidgets.QMessageBox.Warning)
            warn_dialog.setWindowTitle('Warning')
            warn_dialog.setText('Please specify an input file.')
            warn_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
            warn_dialog.exec_()
            return False  # Return that the check has failed

        #################################################
        ### Check if conditions are not empty ###########
        #################################################
        response_given = []
        for condition_text in self.condition_line_edit:
            response_given.append(not (len(condition_text.text()) == 0)) ## Set true if empty

        ### Check if response list is empty ###
        if not any(response_given) and (not bool(self.time_file_toggle.checkState()) or not len(self.condition_line_edit) == 1): # Throw error if empty unless time sections is enabled and only one condition row is present.

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
                warn_dialog.setText("Condition " + empty_indexes_error_str + " appears to be empty please specify a condition. Or add a time section file.")
            warn_dialog.setInformativeText("<b>Example</b>: speed > 10 & speed < 15 & acceleration > 5 & acceleration < 8")
            warn_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
            warn_dialog.exec_()
            return False  # Return that the check has failed

        #################################################
        ### If enabled check if time file is present ####
        #################################################
        if bool(self.time_file_toggle.checkState()) and self.time_file_path.text() == "":

            ### Create warning dialog specifying the empty conditions ###
            warn_dialog = QtWidgets.QMessageBox()
            warn_dialog.setIcon(QtWidgets.QMessageBox.Warning)
            warn_dialog.setWindowTitle('Warning')
            warn_dialog.setTextFormat(QtCore.Qt.RichText)
            warn_dialog.setText("""It seems that you enabled the 'Use time section file' option but didn't specify a time section file.
                                   Please specify a time section file or disable the 'Use time section file' option again.""")
            warn_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
            warn_dialog.exec_()
            return False

        #################################################
        ### Check validity of condition statement #######
        #################################################

        ### Create vallid operator list ###
        operator_escape_str = [("\\"+ op) for op in operators]
        operator_str = "(" + "|".join(operator_escape_str) + ")"

        ### Split input command in list items ###
        result_invalid = []  # True if conditional statement is vallid (Return variable)
        conditions_split = [x.strip() for x in re.split(operator_str, condition_text.text())]

        ### Check if delimiters were placed right ###
        if any([(' ' in y) for y in conditions_split]):
            result_invalid.append(True)   # Condition failed condition validity test
        else:
            result_invalid.append(False)  # Condition passed condition validity test

        #################################################
        ### Check validity of operators #################
        #################################################
        symbols = [y.strip() for y in re.split(r"\w", condition_text.text())]  # Get all operators out of condition statemen
        symbols = [x.replace('"', '').strip() for x in symbols]  # Remove possible double quotes

        ### Remove empty list items ###
        while '' in symbols: # Remove white spaces in trimmed
            symbols.remove('')

        ### Check if operators are valid ###
        if not any([sym in operators for sym in symbols]) and not symbols == []:
            result_invalid.append(True)  # Operators failed the validity test
        else:
            result_invalid.append(False)  # Operators passed the validity test

        ### Print error if conditions are not valid ###
        if any(result_invalid):

            ### Create warning information str ###
            error_idx_list = [ii+1 for ii, x in enumerate(result_invalid) if x == True]
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
            return False

        #################################################
        ### Return test results #########################
        #################################################

        ### If user input passed all test return True ###
        return True

    #################################################
    #### Condition validity check function       ####
    #################################################
    def progress_fn(self, progress_object):
        '''Qt slot function which is triggered when a thread sends a progress signal. This is used to
        display some progress messages for the user on the dialog console.

        Args:
            progress_str (str): The worker progress string which needs to be printed to the dialog console.
        '''

        ### Append progress message to progress console ###
        if type(progress_object) == tuple:
            self.progress_dialog.ui.progress_console.append(progress_object[0])
            self.progress_dialog.ui.progress_bar.setValue(progress_object[1])   # Set progress bar when only one analysis is performed
        else:
            self.progress_dialog.ui.progress_console.append(progress_object)

    #################################################
    #### Condition validity check function       ####
    #################################################
    def thread_complete(self):
        ''' Qt slot function which is triggered when a thread is completed. It is connected
        to the threads finished signal. These signals are created using the pyqtSignal class.
        '''

        ### Change Progress Bar ###
        self.progress_dialog.ui.progress_bar.setValue(100)
        self.progress_dialog.ui.buttonBox.removeButton(self.progress_dialog.ui.buttonBox.button(QtWidgets.QDialogButtonBox.Cancel))  # Remove cancel button
        self.progress_dialog.ui.buttonBox.addButton("Finish", QtWidgets.QDialogButtonBox.AcceptRole)

    #################################################
    #### Start data analyse slot                 ####
    #################################################
    def start_data_analysis(self):
        '''Qt slot function that is used to start the data analysis in a number of worker
        threads so that the GUI does not freeze when the data analysis is performed. The
        actual data analysis is performed by the :func:`analyse_data` function.'''

        ### Validate if user input is correct ###
        test = self.player_filter_combo_box.itemsChecked()
        test_result = self.check_condition()

        ### If user input is correct run the data analysis ###
        if test_result:

            ### Pass the analyse_data function to the workers to execute ###
            self.data_analyse_worker = Worker(self.analyse_data)  # Any other args, kwargs are passed to the run function

            ### Connect status signals ###
            # self.data_analyse_worker.signals.result.connect(self.print_output)  # Results signal slot
            self.data_analyse_worker.signals.finished.connect(self.thread_complete)
            self.data_analyse_worker.signals.progress.connect(self.progress_fn)

            ### Start workers ###
            self.data_analyse_worker.start()

            ### Create progress dialog ###
            self.progress_dialog = QtWidgets.QDialog(None, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)
            self.progress_dialog.ui = Ui_ProgressDialog()
            self.progress_dialog.ui.setupUi(self.progress_dialog)
            self.progress_dialog.setModal(True)

            ### Set dialog header ###
            if not self.player_filter_toggle.checkState():
                self.progress_dialog.ui.progress_header.setText("Performing data analysis...")
            else:
                self.progress_dialog.ui.progress_header.setText("Performing data analysis for 1 player.")

            ### Display dialog ###
            self.progress_dialog.show()
            self.progress_dialog.exec_()

            ### Terminate threads if the cancel button is clicked ###
            if not self.progress_dialog.result():
                print(self.progress_dialog.result())
                self.data_analyse_worker.terminate()  # Terminate worker thread

    #################################################
    #### Data analyse function                   ####
    #################################################
    def analyse_data(self, progress_callback, player_name=None):
        '''The function in which the data analysis is performed. The function uses the data present in the csv file
        which is specified in the input_file_path member variable. The data analysis is performed using the
        :func:`pandas.read_csv()` function which returns a pandas dataframe. Following the data in this dataframe
        is checked against the conditional statements specified in the conditions grid of the main GUI window.

        Args:
            player_name (str, optional): Defaults to None. The name of the player that needs to be analysed. If :samp:`player_name` = :samp:`None` the player is not used as a condition.
            progress_callback (str): The worker progress string which needs to be printed to the dialog console.

        Returns:
            Bool: Descriptor specifying whether the data analyse was successfully.
        '''

        ### Send progress to dialog console ###
        if player_name == None:
            progress_callback.emit("Starting data analysis...")  # When player filter is not enabled
        else:
            progress_callback.emit("Starting data analysis for player %s...", player_name) # When player filter is enabled

        #################################################
        ### Perform data analysis #######################
        #################################################

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
            condition_tmp_2 = [("self.df[\""+ w.capitalize()+"\"]") if w.isalpha() else w for w in condition_tmp_1]
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

            ### Create extra time column ###
            self.df['Time'] = self.df['Timestamp']*(1/freq)
            self.df.index = pd.to_datetime(self.df['Time'], unit='s')

            ### Filter the data based on time sections when time section file is specified ###
            if self.time_file_toggle.isChecked() and not (self.input_file_path.text() == ''):

                ### Get data out of specified time sections file ###
                self.df_time = pd.read_csv(self.time_file_path.text(), header=0, encoding="utf-8", sep=';')
                self.df_time.columns = self.df_time.columns.str.title()  # Make sure the columns are capitalized

                ### Substract the "Begin Time" of the "Start" row from all of the other Begin and start times ###
                begin_times = pd.to_timedelta(self.df_time['Start Time'])  # Get start times out of dataframe (timedelta format)
                end_times = pd.to_timedelta(self.df_time['End Time'])  # Get end times out of dataframe (timedelta format)
                start_time_offset = pd.to_timedelta(self.df_time[(self.df_time["Name"] == "Start")]["Start Time"].tolist()[0]) # Get time offset
                begin_times = begin_times - start_time_offset  # Substract time offset from begin times
                end_times = end_times - start_time_offset  # Substract time offset from end times

                ### Convert begin and start times to datetime format (needed for the pd.between_times module) ###
                begin_times = pd.to_datetime(begin_times).dt.time  # List containing section begin times
                end_times = pd.to_datetime(end_times).dt.time  # List containing sections end times

                ### Get data within specific time ranges ###
                df_sections = [self.df.between_time(i, j) for (i,j) in zip(begin_times, end_times)]
                self.df = pd.concat(df_sections) # Add all the dataframes of the time_sections together again

            #################################################
            ### Check data against conditions################
            #################################################
            try:
                df_condition = self.df[eval(condition)]
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
                key_vallid_list = self.df.columns
                key_vallid_list_error_str = ', '.join(map(str, key_vallid_list)) if len(key_vallid_list) != 2 else ' & '.join(map(str, key_vallid_list))

                ### Send feedback that data analysis has not been performed successfully ###
                print("Error")
                return (False, key_vallid_list_error_str) # (Data analysis result, return message)

                # ### Print warning message ###
                # warn_dialog = QtWidgets.QMessageBox()
                # warn_dialog.setIcon(QtWidgets.QMessageBox.Warning)
                # warn_dialog.setWindowTitle('Warning')
                # if len(key_invalid_idx_list) > 1:
                #     warn_dialog.setText('Unfortunately some of your conditions contain invalid variables please check conditions ' + key_condition_error_str + ' again.')
                # else:
                #     warn_dialog.setText('Unfortunately one of your conditions contain invalid variables please check condition ' + key_condition_error_str + ' again.')
                # warn_dialog.setInformativeText("<b>Vallid keys</b>: " + key_vallid_list_error_str)
                # warn_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
                # warn_dialog.exec_()

        ### Otherwise save results to xlsx file ###
        else:

            ### Send progress to dialog console ###
            if player_name == None:
                progress_callback.emit(("Saving results to xlsx file...", 50))  # When player filter is not enabled
            else:
                progress_callback.emit("Saving results for player %s to a xlsx file...", player_name) # When player filter is enabled

            ### Save results to xlsx file ###
            writer.save()

            ### Send progress to dialog console ###
            if player_name == None:
                progress_callback.emit("Results successfully saved to xlsx file!")  # When player filter is not enabled
                progress_callback.emit("Data analysis completed!")  # When player filter is not enabled
            else:
                progress_callback.emit("Results for player %s successfully saved to xlsx file!", player_name) # When player filter is enabled
                progress_callback.emit("Data analysis for player %s completed!", player_name) # When player filter is enabled

            ### Send feedback that data analysis was successfull ###
            return True

            # ### Print analyse completed message ###
            # analyse_dialog = QtWidgets.QMessageBox()
            # analyse_dialog.setIcon(QtWidgets.QMessageBox.Information)
            # analyse_dialog.setWindowTitle('Info')
            # analyse_dialog.setText("Data analysis complete you can find the file in the specified output folder")
            # analyse_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
            # analyse_dialog.exec_()

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
