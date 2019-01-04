# -*- coding: utf-8 -*-
"""
This file contains the main GUI class that is used in the *Conditional game data analyse tool (CGDAT)* was created for a friend
of mine to help him with the data analysis he had to do for his graduation project. This tool is licensed under the GPL open source license.
You are therefore free use the source code in any way provided that you the original copyright statements.

Author:
    Rick Staa

Maintainer:
    Wesley Bosman

**Classes:**

.. autosummary::
   :toctree: _autosummary

    .progressDialog
    .importDialog
    .outputSettingsDialog
    .DataAnalyserGUI

"""

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
import webbrowser  # Used for displaying the documentation
import traceback
import math

### Get relative script path ###
dirname = os.path.dirname(os.path.abspath(__file__))

### Set working directory ###
os.chdir(dirname)

### Create the needed python user interface classes out of the QT UI files ###
subprocess.call(r"python -m PyQt5.uic.pyuic -x " + os.path.join(dirname, '..', r'qt\cgdat.ui') + " -o " + os.path.join(dirname, '..', r'scripts\qt_ui\cgdat_ui.py'))
subprocess.call(r"python -m PyQt5.uic.pyuic -x " + os.path.join(dirname, '..', r'qt\output_settings.ui') + " -o " + os.path.join(dirname, '..', r'scripts\qt_ui\output_settings_ui.py'))
subprocess.call(r"python -m PyQt5.uic.pyuic -x " + os.path.join(dirname, '..', r'qt\about.ui') + " -o " + os.path.join(dirname, '..', r'scripts\qt_ui\about_ui.py'))
subprocess.call(r"python -m PyQt5.uic.pyuic -x " + os.path.join(dirname, '..', r'qt\progress_dialog.ui') + " -o " + os.path.join(dirname, '..', r'scripts\qt_ui\progress_dialog_ui.py'))
subprocess.call(r"python -m PyQt5.uic.pyuic -x " + os.path.join(dirname, '..', r'qt\import_dialog.ui') + " -o " + os.path.join(dirname, '..', r'scripts\qt_ui\import_dialog_ui.py'))

### Import custom classes and functions ###
from qt_custom import Worker, WorkerSignals
from qt_custom import MultiSelectMenu

### Import the python UI classes ###
from qt_ui import Ui_MainWindow
from qt_ui import Ui_About
from qt_custom import importDialog, outputSettingsDialog, progressDialog

#####################################################################
#### Deal with high resolution screens                           ####
#####################################################################
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

#####################################################################
#### Script settings                                             ####
#####################################################################
sections = ["Speed","Acceleration"]
operators = ['>','>=','<','<=','==','!=','&']
freq = (1.0/(0.166667/100.0))  # Data recording frequency [Hz]

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
        app.aboutToQuit.connect(self.closeEvent)

        ########################################
        ### Set main GUI menu items ############
        ########################################

        ### Create media paths ###
        self.toggle_icon_on = os.path.abspath(os.path.join(dirname, "..", "media/toggle_on.png")).replace('\\','/')    # Toggle on icon
        self.toggle_icon_disabled = os.path.abspath(os.path.join(dirname, "..", "media/toggle_off_disabled.png")).replace('\\','/')    # Toggle on icon
        self.toggle_icon_off = os.path.abspath(os.path.join(dirname, "..", "media/toggle_off.png")).replace('\\','/')  # Toggle off icon
        about_icon_path = os.path.join(dirname, '..', r'media\about_icon.svg')                      # About icon path
        docs_icon_path = os.path.join(dirname, '..', r'media\docs_icon.png')                      # About icon path

        ### Create other paths ###
        self.docs_path = os.path.abspath(os.path.join(dirname, "..", "docs/documentation.lnk")).replace('\\','/')    # Toggle on icon

        ### Setup about icon menu action ###
        about_icon = QtGui.QIcon()
        about_icon.addPixmap(QtGui.QPixmap(about_icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(about_icon)  # Set icon
        self.actionAbout.triggered.connect(self.action_about_slot)  # Set slot

        ### Setup documentation menu action ###
        docs_icon = QtGui.QIcon()
        docs_icon.addPixmap(QtGui.QPixmap(docs_icon_path), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionDocumentation.setIcon(docs_icon)  # Set icon
        self.actionDocumentation.triggered.connect(self.action_doc_slot)  # Set slot

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
        self.time_file_toggle.setStyleSheet("QCheckBox::indicator:checked {image: url('"+self.toggle_icon_on+"');}\n QCheckBox::indicator:unchecked {image: url('"+self.toggle_icon_off+"');}\n QCheckBox::indicator:disabled {image: url('"+self.toggle_icon_disabled+"');}")
        self.time_file_browser_btn.clicked.connect(self.get_time_sections_file)
        self.time_file_toggle.setEnabled(0)

        ### Setup time range option ###
        self.time_range_toggle.setStyleSheet("QCheckBox::indicator:checked {image: url('"+self.toggle_icon_on+"');}\n QCheckBox::indicator:unchecked {image: url('"+self.toggle_icon_off+"');}\n QCheckBox::indicator:disabled {image: url('"+self.toggle_icon_disabled+"');}")
        self.time_range_toggle.setEnabled(0)

        ### Setup player filter option ###
        self.player_filter_toggle.setStyleSheet("QCheckBox::indicator:checked {image: url('"+self.toggle_icon_on+"');}\n QCheckBox::indicator:unchecked {image: url('"+self.toggle_icon_off+"');}\n QCheckBox::indicator:disabled {image: url('"+self.toggle_icon_disabled+"');}")
        self.player_filter_toggle.setEnabled(0)
        self.player_filter_drop_down_menu = MultiSelectMenu()
        self.player_filter_drop_down_menu.setObjectName("player_filter_choicer")
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.player_filter_drop_down_menu.sizePolicy().hasHeightForWidth())
        self.player_filter_drop_down_menu.setSizePolicy(sizePolicy)
        self.additional_options_layout.addWidget(self.player_filter_drop_down_menu, 2, 2, 1, 1)
        self.player_filter_drop_down_menu.setText("Please import a data file to see the available players")
        self.player_filter_drop_down_menu.setEnabled(0)

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
        self.condition_add_row_btn.setToolTip("<html><head/><body><p>Add condition.</p></body></html>")
        self.condition_add_row_btn.setMinimumSize(QtCore.QSize(22, 22))
        self.condition_add_row_btn.setMaximumSize(QtCore.QSize(22, 22))
        self.condition_add_row_btn.setObjectName("condition_add_row_btn")
        self.condition_add_row_btn.setText("+")
        self.condition_add_row_btn.clicked.connect(self.add_conditions_row)
        self.conditions_grid.addWidget(self.condition_add_row_btn, 0, 2, 1, 1)

        ### Add a condition remove button ###
        self.condition_remove_row_btn = QtWidgets.QToolButton(self.conditions_group_box)
        self.condition_remove_row_btn.setToolTip("<html><head/><body><p>Remove condition.</p></body></html>")
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
        self.output_settings_btn.clicked.connect(self.set_output_settings)

        ########################################
        ### Create ouput settings dialog     ###
        ########################################

        ### Create helper Variables ###
        self.input_file_freq = freq  # Create member variable holding input file frequency settings
        self.output_columns = [] # Create member variables to save output collumns settings
        self.input_file_freq_toggle = False # Create member variable to save old frame toggle state
        self.output_columns_toggle = False # Create member variable to save old output columns toggle
        self.output_settings_freq_warning = True # Create member variable to save wheter a warning needs to be displayed

        ##{ Create dialog object ###
        self.output_settings_dialog = outputSettingsDialog()
        self.output_settings_dialog.setModal(True)
        self.output_settings_dialog.finished.connect(self.output_settings_dialog_finished)  # Connect finished signal to function that checks if the used cancelled the analysis
        self.output_settings_dialog.frame_rate_value.setValue(self.input_file_freq)

    #########################################################
    #### GUI member functions                            ####
    #########################################################

    #################################################
    ### Menu about action function                ###
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
    ### Menu docs action function                 ###
    #################################################
    def action_doc_slot(self):
        '''Qt slot function displays the documentation. This slot is triggered when the docs menu item is clicked or
        the user uses the F2 keyboard shortcut.
        '''

        ## open documentation ##
        webbrowser.open_new(self.docs_path)

    #################################################
    ### Menu docs action function                 ###
    #################################################
    def set_output_settings(self):
        '''Qt slot used to open the output_settings UI which can be used to set some additional settings for the output file. Currently the following
        additional settings are supported:

            - Change the input file frequency: By default this will be around 600 hz.
            - Set the columns to include in the output file: By default the CGDAT tool only keeps the variables (csv columns) that are specified in your conditions.
        '''

        ### Display output settings dialog ###
        self.output_settings_dialog.show()

    #################################################
    ### Settings dialog finished slot             ###
    #################################################
    def output_settings_dialog_finished(self, result):
        '''Qt slot that is triggered when the output settings dialog is finished. This function
        updates the settings the user changed into the GUI member variables.
        '''

        ### Variables ###
        if not result:  # If dialog was accepted

            ### Reset frame rate ###
            self.output_settings_dialog.frame_rate_value.setValue(self.input_file_freq)  # Reset frequency
            self.output_settings_dialog.frame_rate_toggle.setChecked(self.input_file_freq_toggle)  # Reset toggle

            ### Reset columns settings list ###
            for action in self.output_settings_dialog.column_choicer_drop_down_menu.toolmenu.actions():
                if action.text() in self.output_columns:  # Check which actions were checked and reset menu
                    action.setChecked(1)  # Check action
                else:
                    action.setChecked(0)  # Un-check action
            self.output_settings_dialog.columns_toggle.setChecked(self.output_columns_toggle) # Reset toggle

        else:
            self.input_file_freq = self.output_settings_dialog.frame_rate_value.value()  # Save frame rate
            self.output_columns = self.output_settings_dialog.column_choicer_drop_down_menu.selectedItems()  # Save collumns
            self.output_columns_toggle = self.output_settings_dialog.columns_toggle.isChecked()  # Save collumns toggle
            self.input_file_freq_toggle = self.output_settings_dialog.frame_rate_toggle.isChecked()  # Save freq toggle

            ### If data file is already imported show dialog that states that file needs to be reimported before frame rate is effective ###
            if self.input_file_path.isEnabled() and self.input_file_freq_toggle:
                if self.output_settings_freq_warning:  # Display warning if user didn't disable it
                    ## Display Info message ##
                    info_str = "A data file was already imported, to use the adjusted frame rate please reimport the data file."
                    cb = QtWidgets.QCheckBox("Don't show message again.")
                    msg = QtWidgets.QMessageBox()
                    msg.setCheckBox(cb)
                    msg.setIcon(QtWidgets.QMessageBox.Information)
                    msg.setText(info_str)
                    msg.setWindowTitle("Info")
                    msg.show()
                    msg.exec_()

                    ## Disable dialog if user checked the checkbox ##
                    self.output_settings_freq_warning = True if not msg.checkBox().isChecked() else False

    #################################################
    ### Get input file path function              ###
    #################################################
    def get_input_file(self):
        '''Qt slot function created to get a user specified input file. It is linked to the input_file_browser_btn and displays a
        file choicer dialog in which the user can specify the input data file.
        '''

        ### Create file dialog ###
        file_dialog = QtWidgets.QFileDialog()
        fileName, _ = file_dialog.getOpenFileName(None,"Select input file", "","CSV Files (*.csv)")
        fileName = os.path.normpath(fileName)

        ### Enable input field if not empty ###
        if not (fileName == "."):  # If not empty

            ### Create and show progress dialog ###
            import_str = """The data file is being imported. Please wait until the import is ready or cancel the import by using the cancel button below."""
            self.import_dialog = importDialog()
            self.import_dialog.setModal(True)
            self.import_dialog.progress_header.setText(import_str)
            self.import_dialog.finished.connect(self.import_dialog_finished)  # Connect finished signal to function that checks if the used cancelled the analysis
            self.import_dialog.show()

            ### Enable input file display widget ###
            self.input_file_path.setText(fileName)
            self.input_file_path.setEnabled(1)

            ### Create worker that checks if the data file is vallid ###
            self.data_input_worker = Worker(self.analyse_input_data_file)  # Any other args, kwargs are passed to the run function

            ### Connect worker signals ###
            self.data_input_worker.signals.finished.connect(self.data_input_worker_finished)  # Checks the process result
            self.data_input_worker.signals.error.connect(self.catch_thread_errors)  # Checks the process result

            ### Clean player filter list if it is already filled ###
            self.player_filter_drop_down_menu.clear()

            ### Clean column selection list ###
            self.output_settings_dialog.column_choicer_drop_down_menu.clear()

            ### Start Worker ###
            self.data_input_worker.start()

        else:
            if (self.input_file_path.text() == ""):  # If no file has been specified yet
                self.input_file_path.setText("")
                self.input_file_path.setEnabled(0)

    #################################################
    ### Get input file path function              ###
    #################################################
    def analyse_input_data_file(self, *args, **kwargs):
        '''Qt slot function that is used to check if the data file is vallid and following add the available players to the player filter comboBox. This slot function is
        run in a worker thread so it does not freeze the GUI.
        '''

        ### Import the csv file ###
        try:
            self.df = pd.read_csv(self.input_file_path.text(), header=0, encoding='utf-8')   # Try to read in data fileexc
            self.df.columns = self.df.columns.str.title()  # Capitalize columns to prohibit key errors
        except Exception as e:

            ### Return warning message ###
            warning_str = """Unfortunately something went wrong while importing the datafile. Please check if you supplied a vallid data file and try again."""
            return (False, "import_error", warning_str, e)

        ### Check whether a player column is present ###
        if not ("Name" in self.df.columns):

            ### Return info message ###
            warning_str = """The file you imported doesn't contain a player column. As a result the player filter option has been disabled. Please specify another file if you want to filter you data by player name."""
            return (False, "player_filter_error", warning_str)

        ### Check wheter file contains a time stamp collumn ###
        if not ("Timestamp" in self.df.columns):

            ### Return info message ###
            warning_str = """The file you imported doesn't contain a timestamp column. Please import a vallid data file and try again."""
            return (False, "timestamp_error", warning_str)

        ### Add a time axis to the dataframe ###
        try:
            if self.input_file_freq_toggle:  # If user changed frame rate
                date_time_list = pd.to_datetime((self.timeDelta2DateTime(self.df['Timestamp']*(1/self.input_file_freq))))  # Create DateTimeIndex
                self.df.index = date_time_list  # Set DateTimeIndex
            else:  # Use default
                date_time_list = pd.to_datetime((self.timeDelta2DateTime(self.df['Timestamp']*(1/freq))))  # Create DateTimeIndex
                self.df.index = date_time_list  # Set DateTimeIndex
        except Exception as e:
            ### Return warning message ###
            warning_str = """Unfortunately something went wrong while creating a time axis. Please try againcontact the developer."""
            return (False, "import_error", warning_str, e)

        ### If everything went correctly return True as a result ###
        return (True,)

    #################################################
    ### Update player filter menu function        ###
    #################################################
    def data_input_worker_finished(self, result):
        """QT slot function used to check whether the data file import was successful. If successful it updates the
        player filter choicer menu by adding the available players to the menu options.

        Args:
            bool: Boolean specifying whether the data file import was successfully.
        """

        ### Apply the right action ###
        if result[0]:  # If import was successful

            ### Close wait dialog ###
            self.import_dialog.accept()

            ### Get the players present in the data file ###
            self.players = np.unique(self.df["Name"].tolist()).tolist()  # Get unique players
            self.players = [player for player in self.players if player not in ('ball', 'nan')]  # Remove nan and ball

            ### Add players to player filter drop down menu ###
            for player in self.players: # Add rest of the players
                self.player_filter_drop_down_menu.addItem(player)
            self.player_filter_drop_down_menu.removeAllOption()  # Add a select all option to the menu
            self.player_filter_drop_down_menu.addAllOption()  # Add a select all option to the menu

            ### Change toolbox menu text ###
            self.player_filter_drop_down_menu.setEnabled(1) # Enable player filter drop down menu
            self.input_file_path.setEnabled(1)  # Enable input file path field
            self.time_range_toggle.setEnabled(1) # Enable time range toggle
            self.player_filter_toggle.setEnabled(1) # Enable player toggle
            self.player_filter_drop_down_menu.setText("Select players")

            ### Add Columns to settings menu ###
            for columns in self.df.columns:
                self.output_settings_dialog.column_choicer_drop_down_menu.addItem(columns)
            self.output_settings_dialog.column_choicer_drop_down_menu.setText("Please select the columns you want to include in your analysis")
            self.output_settings_dialog.column_choicer_drop_down_menu.setEnabled(1)
            self.output_settings_dialog.columns_toggle.setEnabled(1)

        else:  # If import failed

            ### Display warning message if no thread error occurred ###
            if (str(result[1]) == "thread_error"):

                ### Close wait dialog ###
                self.import_dialog.reject()

            elif (str(result[1]) == "timestamp_error"):

                ### Close wait dialog ###
                self.import_dialog.reject()

                ### Display Info message ###
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(result[2])
                msg.setWindowTitle("Warning")
                msg.show()
                msg.exec_()

            elif (str(result[1]) == "player_filter_error"):

                ### Close wait dialog ###
                self.import_dialog.accept()

                ### Disable player filter ###
                self.player_filter_toggle.setEnabled(0)
                self.player_filter_drop_down_menu.setEnabled(0)
                self.player_filter_drop_down_menu.setText("Please import a data file to see the available players")

                ### Enable other filters ###
                self.time_range_toggle.setEnabled(1) # Enable file path toggle

                ### Display Info message ###
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText(result[2])
                msg.setWindowTitle("Info")
                msg.show()
                msg.exec_()

            else:
                ### Close wait dialog ###
                self.import_dialog.reject()

                ### Display error message ###
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(result[2])
                if result[3].args.__len__() != 0:
                    msg.setInformativeText("<b>Error msg:</b><br>"+str(result[3]))
                msg.setWindowTitle("Warning")
                msg.show()
                msg.exec_()

    #################################################
    #### Data analyse dialog finished function   ####
    #################################################
    def import_dialog_finished(self, result):
        """This function is used to check whether the data import was
        successful or whether the user cancelled the import using the cancel button present
        on the dialog window.

        Args:
            result (int): Bool specifying whether the QDialog was accepted (1) or rejected (0)
        """

        ### Terminate threads if the cancel button is clicked ###
        if not result:
            self.input_file_path.setText("")  # Reset input file text
            self.input_file_path.setEnabled(0)  # Disable input file path field
            self.time_range_toggle.setEnabled(0) # Disable time range toggle
            self.player_filter_toggle.setEnabled(0) # Disable player toggle
            self.player_filter_drop_down_menu.setEnabled(0)
            self.player_filter_drop_down_menu.setText("Please import a data file to see the available players")
            self.data_input_worker.terminate()  # Terminate worker thread

    #################################################
    ### Get time sections file path function      ###
    #################################################
    def get_time_sections_file(self):
        '''Qt slot function created to get a user specified time sectsions input file. In this file the :samp:`begin times`
        and :samp:`End times` of the sections where the data analysis has to be performed are specified.
        It is linked to the time_file_browser_btn and displays a file choicer dialog in which the user can specify the input data file.
        '''

        ### Create file dialog ###
        file_dialog = QtWidgets.QFileDialog()
        fileName, _ = file_dialog.getOpenFileName(None,"Select time sections file", "","CSV Files (*.csv)")
        fileName = os.path.normpath(fileName)

        ### Enable input field if not empty ###
        if not (fileName == "."):  # If empty

            ### Create and show progress dialog ###
            import_str = """The time sections data file is being imported. Please wait until the import is ready or cancel the import by using the cancel button below."""
            self.import_dialog = importDialog()
            self.import_dialog.setModal(True)
            self.import_dialog.progress_header.setText(import_str)
            self.import_dialog.finished.connect(self.time_import_dialog_finished)  # Connect finished signal to function that checks if the used cancelled the analysis
            self.import_dialog.show()

            ### Enable input file display widget ###
            self.time_file_path.setText(fileName)
            self.time_file_path.setEnabled(1)

            ### Create worker that checks if the data file is vallid ###
            self.time_input_worker = Worker(self.analyse_input_time_data_file)  # Any other args, kwargs are passed to the run function

            ### Connect worker signals ###
            self.time_input_worker.signals.finished.connect(self.time_input_worker_finished)  # Checks the process result
            self.time_input_worker.signals.error.connect(self.catch_thread_errors)  # Checks the process result

            ### Start Worker ###
            self.time_input_worker.start()

        else:
            if (self.time_file_path.text() == ""):  # If no file has been specified yet
                self.time_file_path.setText("")
                self.time_file_path.setEnabled(0)

    #################################################
    ### Get input file path function              ###
    #################################################
    def analyse_input_time_data_file(self, *args, **kwargs):
        '''Qt slot function that is used to check if the time sections data file is vallid. This slot function is
        run in a worker thread so it does not freeze the GUI.
        '''

        ### Import the csv file ###
        try:
            ### Get data out of specified time sections file ###
            self.df_time = pd.read_csv(self.time_file_path.text(), header=0, encoding="utf-8", sep=';')
            self.df_time.columns = self.df_time.columns.str.title()  # Make sure the columns are capitalized
        except Exception as e:

            ### Return warning message ###
            warning_str = """Unfortunately something went wrong while importing the datafile. Please check if you supplied a vallid data file and try again."""
            return (False, "import_error", warning_str, e)

        ### Begin and end time columns are present ###
        if not ('Start Time' in self.df_time.columns) or not ('End Time' in self.df_time.columns):

            ### Return info message ###
            warning_str = """The time section file you imported doesn't contain a 'Start Time' and/or 'Begin Time' column. As a result, the time section filter option has been disabled. Please import another file if you want to filter your data by based on specified time sections."""
            return (False, "time_filter_error", warning_str)
        else:

            ### Return that the result that the time sections file is correct ###
            return (True,)

    #################################################
    ### Update player filter menu function        ###
    #################################################
    def time_input_worker_finished(self, result):
        """QT slot function used to check whether the time section file was successfully imported. If successful it updates the
        player filter choicer menu by adding the available players to the menu options.

        Args:
            bool: Boolean specifying whether the data file import was successfully.
        """

        ### Apply the right action ###
        if result[0]:  # If import was successful

            ### Close wait dialog ###
            self.import_dialog.accept()

            ### Change toolbox menu text ###
            self.time_file_toggle.setEnabled(1)  # Enable input file path field

        else:  # If import failed

            ### Display warning message if no thread error occurred ###
            if (str(result[1]) == "thread_error"):

                ### Close wait dialog ###
                self.import_dialog.reject()

            elif (str(result[1]) == "time_filter_error"):

                ### Close wait dialog ###
                self.import_dialog.reject()

                ### Display error message ###
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText(result[2])
                msg.setWindowTitle("Info")
                msg.show()
                msg.exec_()

            else:
                ### Close wait dialog ###
                self.import_dialog.reject()

                ### Display error message ###
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(result[2])
                if result[3].args.__len__() != 0:
                    msg.setInformativeText("<b>Error msg:</b><br>"+str(result[3]))
                msg.setWindowTitle("Warning")
                msg.show()
                msg.exec_()

    #################################################
    #### Time import dialog finished function    ####
    #################################################
    def time_import_dialog_finished(self, result):
        """This function is used to check whether the file specifying the time sections was
        imported successfully or whether the user cancelled the import using the cancel button present
        on the dialog window.

        Args:
            result (int): Bool specifying whether the QDialog was accepted (1) or rejected (0)
        """

        ### Terminate threads if the cancel button is clicked ###
        if not result:
            self.time_file_path.setText("")  # Reset input file text
            self.time_file_toggle.setEnabled(0)  # Disable input file path field
            self.time_file_path.setEnabled(0)  # Disable input file path field
            self.time_input_worker.terminate()  # Terminate worker thread

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
    #### Catch worker error                      ####
    #################################################
    def catch_thread_errors(self, error_tuple):
        '''This function catches errors in worker threads and outputs them to the user.

        Args:
            error_tuple (tuple): The error tuple that was send by the worker tread.
        '''

        ### Display error message ###
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText("Something went wrong in one of the GUI threads. Please contact the project maintainer if the problem persists.")
        msg.setInformativeText("<b>Error msg:</b><br>"+str(error_tuple[0]).replace("<class '","").replace("'>","")+": "+str(error_tuple[1])+"<br><br>"+str(error_tuple[2]))
        msg.setWindowTitle("Error")
        msg.show()
        msg.exec_()

    #################################################
    #### Create folder function                   ###
    #################################################
    def createFolder(self, directory):
        """This function is used to create a folder when it does not exists"""
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
        except OSError:
            print ('Error: Creating directory. ' + directory)

    #################################################
    #### Create DateTime list function            ###
    #################################################
    def timeDelta2DateTime(self, time_delta_list):
        '''This method converts a list containing the time since measurement onset [seconds] into a
        list containing dateTime objects counting up from 00:00:00.

        Args:
            time_delta_list (list): List containing the times since the measurement has started.

        Returns:
            list: A list with the time in the DateTime format.
        '''

        ### Use divmod to convert seconds to m,h,s.ms ###
        s, fs = list(zip(*[divmod(item, 1) for item in time_delta_list]))
        m, s = list(zip(*[divmod(item, 60) for item in s]))
        h, m = list(zip(*[divmod(item, 60) for item in m]))

        ### Create DatTime list ###
        ms = [item*1000 for item in fs] # Convert fractional seconds to ms
        time_list_int = list(zip(*[list(map(int,h)), list(map(int,m)), list(map(int,s)), list(map(int,ms))])) # Combine h,m,s,ms in one list

        # Return dateTime object list
        return [datetime(2018,1,1,item[0],item[1],item[2],item[3]) for item in time_list_int]

    #################################################
    #### Add padding to bool array function        ###
    #################################################
    def padBoolArray(self, bool_array, n):

        ### Check whether a bool array was inputted ###
        bool_test = all([item.dtype == bool for item in bool_array])

        if bool_test:
            ### Perform padding operation ###
            bool_array_padded = bool_array.copy()  # Make hardcopy so that we don't change the original object
            for index, item in enumerate(bool_array):  # Loop through the supplied bool array
                if item:  # If bool == True
                    bool_array_padded[(index-n):(index+n+1)] = True  # Set n neighboors before and after also to true

            ### Return new padded list ###
            return bool_array_padded
        else:  # Raise typeError
            raise TypeError("Please input a array containing only booleans.")

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
    #### Data analyse dialog finished function   ####
    #################################################
    def data_analyse_dialog_finished(self, result):
        """This function is used to check whether the data analysis was
        completed successfully or that the user cancelled the data analysis.
        When the data analysis was cancelled it terminates any running workers.

        Args:
            result (int): Bool specifying whether the QDialog was accepted (1) or rejected (0)
        """

        ### Terminate threads if the cancel button is clicked ###
        if not result:
            for worker in self.data_analyse_worker:
                worker.terminate()  # Terminate worker thread

    #################################################
    #### Condition validity check function       ####
    #################################################
    def worker_finished(self, result):
        ''' Qt slot function which is triggered when a thread is completed. It is connected
        to the threads finished signal. These signals are created using the pyqtSignal class.
        '''

        ### Append finished workers ###
        self.finished_workers += 1
        self.active_workers -= 1

        ### Apply the right action ###
        if result[0]:  # If import was successful

            ### Update progress bar ###
            self.progress_dialog.updateProgressBar((self.finished_workers/self.worker_size)*100)

        else:  # If data analysis failed

            ### Display warning message if no thread error occurred ###
            if (str(result[1]) == "thread_error"):

                ### Close wait dialog ###
                self.progress_dialog.reject()

            elif (str(result[1]) == "save_error"):

                ### Append red error message to console text edit ###
                self.progress_dialog.updateProgressConsole(result[2], "#ff0000")

            elif (str(result[1])=="key_error"):

                ### Close wait dialog ###
                self.progress_dialog.reject()

                ### Print warning message ###
                warn_dialog = QtWidgets.QMessageBox()
                warn_dialog.setIcon(QtWidgets.QMessageBox.Warning)
                warn_dialog.setWindowTitle('Warning')
                if len(result[2]) > 1:
                    warn_dialog.setText('Unfortunately, some of your conditions contain invalid variables please check conditions ' + result[2] + ' again.')
                else:
                    warn_dialog.setText('Unfortunately one of your conditions contains invalid variables please check condition ' + result[2] + ' again.')
                warn_dialog.setInformativeText("<b>Vallid keys</b>: " + result[3])
                warn_dialog.setStandardButtons(QtWidgets.QMessageBox.Ok)
                warn_dialog.exec_()

            else: # Catch other errors

                ### Close wait dialog ###
                self.progress_dialog.reject()

                ### Display error message ###
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Warning)
                msg.setText(result[2])
                if result[3].args.__len__() != 0:
                    msg.setInformativeText("<b>Error msg:</b><br>"+str(result[3]))
                msg.setWindowTitle("Warning")
                msg.show()
                msg.exec_()

    #################################################
    #### Start data analyse slot                 ####
    #################################################
    def start_data_analysis(self):
        '''Qt slot function that is used to start the data analysis in a number of worker
        threads so that the GUI does not freeze when the data analysis is performed. The
        actual data analysis is performed by the :func:`analyse_data` function.'''

        ### Validate if user input is correct ###
        test_result = self.check_condition()

        ### Create progress dialog object ###
        self.progress_dialog = progressDialog()

        ### Get player list if player filter is enabled ###
        if self.player_filter_toggle.isChecked():
                filtered_players = self.player_filter_drop_down_menu.selectedItems()

        ### If user input is correct run the data analysis ###
        if test_result:

            ### Create worker list ###
            self.data_analyse_worker = []
            self.finished_workers = 0
            self.active_workers = 0

            ### Check which data analysis needs to be performed and then start the workers ###
            if not self.player_filter_toggle.isChecked():  # Player filter not selected

                ### Create dialog header ###
                dialog_header = "Performing data analysis..."

                ### Specify number of workers ###
                self.worker_size = 1

                ### Create and show progress dialog ###
                self.progress_dialog.progress_header.setText(dialog_header)
                self.progress_dialog.setModal(True)
                self.progress_dialog.finished.connect(self.data_analyse_dialog_finished)  # Connect finished signal to function that checks if the used cancelled the analysis
                self.progress_dialog.show()

                ### Pass the analyse_data function to the workers to execute ###
                self.data_analyse_worker.append(Worker(self.analyse_data))  # Any other args, kwargs are passed to the run function

                ### Connect status signals ###
                self.data_analyse_worker[0].signals.ready.connect(self.progress_dialog.updateProgressConsole)
                self.data_analyse_worker[0].signals.finished.connect(self.worker_finished)

                ### Start workers ###
                self.data_analyse_worker[0].start()
                self.active_workers += 1

            elif self.player_filter_toggle.isChecked() and (len(filtered_players) == 0):  # If player filter was enabled but no player selected

                ### Create dialog header ###
                dialog_header = "Performing data analysis..."

                ### Specify number of workers ###
                self.worker_size = 1

                ### Display non-modal popup ###
                info_str = "The player filter was enabled but no players were specified. As a result the player filter will not be applied in the data analysis."
                msg = QtWidgets.QMessageBox()
                msg.setIcon(QtWidgets.QMessageBox.Information)
                msg.setText(info_str)
                msg.setWindowTitle("Info")
                msg.exec_()

                ### Create progress dialog ###
                self.progress_dialog.progress_header.setText(dialog_header)
                self.progress_dialog.setModal(True)
                self.progress_dialog.finished.connect(self.data_analyse_dialog_finished)  # Connect finished signal to function that checks if the used cancelled the analysis
                self.progress_dialog.show()

                ### Pass the analyse_data function to the workers to execute ###
                self.data_analyse_worker.append(Worker(self.analyse_data))  # Any other args, kwargs are passed to the run function

                ### Connect status signals ###
                self.data_analyse_worker[0].signals.ready.connect(self.progress_dialog.updateProgressConsole)
                self.data_analyse_worker[0].signals.finished.connect(self.worker_finished)

                ### Start workers ###
                self.data_analyse_worker[0].start()
                self.active_workers += 1

            else: # If more players are selected

                ### Create dialog header and display info message if needed ###
                if len(filtered_players) > 1:
                    dialog_header = ("Performing data analysis for %i players." % len(filtered_players))
                else:
                    dialog_header = "Performing data analysis for 1 player."

                ### Specify number of workers ###
                self.worker_size = len(filtered_players)

                ### Create and show progress dialog ###
                self.progress_dialog.progress_header.setText(dialog_header)
                self.progress_dialog.setModal(True)
                self.progress_dialog.finished.connect(self.data_analyse_dialog_finished)  # Connect finished signal to function that checks if the used cancelled the analysis
                self.progress_dialog.show()

                ### Start workers ###
                self.started_workers = 0  # Started worker incrementer
                ii = 0 # Worker list incrementer
                while self.started_workers < self.worker_size:  # Keep looping till all workers have been started
                    if self.active_workers < 3:  # If the number of workers is less than 3 start a new worker

                        ### Get player name ###
                        player_name = filtered_players[ii]

                        ### Pass the analyse_data function to the workers to execute ###
                        self.data_analyse_worker.append(Worker(self.analyse_data, player_name))  # Any other args, kwargs are passed to the run function

                        ### Connect status signals ###
                        self.data_analyse_worker[ii].signals.ready.connect(self.progress_dialog.updateProgressConsole)
                        self.data_analyse_worker[ii].signals.finished.connect(self.worker_finished)

                        ### Start workers ###
                        self.data_analyse_worker[ii].start()

                        ### Increment workers variables ###
                        self.active_workers += 1  # Increment active workers
                        self.started_workers += 1  # Increment started workers
                        ii += 1  # Increment worker list incrementer

                    else:  # If more than 3 workers are active process other events
                        QtWidgets.QApplication.processEvents()

    #################################################
    #### Data analyse function                   ####
    #################################################
    def analyse_data(self, *args, **kwargs):
        '''The function in which the data analysis is performed. The function uses the data present in the csv file
        which is specified in the input_file_path member variable. The data analysis is performed using the
        :func:`pandas.read_csv()` function which returns a pandas dataframe. Following the data in this dataframe
        is checked against the conditional statements specified in the conditions grid of the main GUI window.

        Args:
            player_name (str, optional): The name of the player that needs to be analysed. Put "" if you don't want to filter by player. If :samp:`player_name` = :samp:`None` the player is not used as a condition.
            progress_callback (str): The worker progress string which needs to be printed to the dialog console.

        Returns:
            Bool: Descriptor specifying whether the data analyse was successfully.
        '''

        ### Retrieve arguments and print start message ###
        ready_signal = kwargs['ready_callback']
        if len(args) < 1:
            player_name = None
            ready_signal.emit("Starting data analysis...")
        else:
            player_name = args[0]
            ready_signal.emit("Starting data analysis for %s..."%player_name)

        #################################################
        ### Perform data analysis #######################
        #################################################

        ### Create hardcopy of database ###
        df_tmp = self.df.copy()

        ### Create writer object
        if not(player_name==None): # If a player was specified

            ### Make player name path save ###
            player_name_lower = player_name.lower() # Make lower case
            player_name_safe = "".join([c for c in player_name_lower if c.isalpha() or c.isdigit() or c==' ']).rstrip() # Replace not accepted characters
            player_name_str = player_name_safe.replace(" ", "_")

            ### Create folder if it does not exist ###
            save_folder = self.output_file_path.text()+"\\"+ player_name_str
            self.createFolder(save_folder)

            ### Create save path ###
            timestr = time.strftime("%Y-%m-%d_%H%M%S")  # Create filename for output file (based on time data)
            output_file_path = os.path.join(self.output_file_path.text(), (player_name_str + "\\" + player_name_str + "_" +timestr + r'.xlsx'))  # Create output file path
        else:
            timestr = time.strftime("%Y-%m-%d_%H%M%S")  # Create filename for output file (based on time data)
            output_file_path = os.path.join(self.output_file_path.text(), (timestr + r'.xlsx'))  # Create output file path
        writer = pd.ExcelWriter(output_file_path, engine='xlsxwriter', datetime_format='hh:mm:ss.ms')  # Create data writer

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
            condition_tmp_2 = [("df_tmp[\""+ w.capitalize()+"\"]") if w.isalpha() else w for w in condition_tmp_1]
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

            ### Filter the data based on time sections when time section file is specified ###
            if self.time_file_toggle.isChecked() and not (self.input_file_path.text() == ''):

                ### Create hardcopy of time dataframe ###
                df_time_tmp = self.df_time.copy()

                ### Substract the "Begin Time" of the "Start" row from all of the other Begin and start times ###
                begin_times = pd.to_timedelta(df_time_tmp['Start Time'])  # Get start times out of dataframe (timedelta format)
                end_times = pd.to_timedelta(df_time_tmp['End Time'])  # Get end times out of dataframe (timedelta format)
                start_time_offset = pd.to_timedelta(df_time_tmp[(df_time_tmp["Name"] == "Start")]["Start Time"].tolist()[0]) # Get time offset
                begin_times = begin_times - start_time_offset  # Substract time offset from begin times
                end_times = end_times - start_time_offset  # Substract time offset from end times

                ### Convert begin and start times to datetime format (needed for the pd.between_times module) ###
                begin_times = pd.to_datetime(begin_times).dt.time  # List containing section begin times
                end_times = pd.to_datetime(end_times).dt.time  # List containing sections end times

                ### Get data within specific time ranges ###
                df_sections = [df_tmp.between_time(i, j, include_start=True, include_end=True) for (i,j) in zip(begin_times, end_times)]
                df_result_tmp = pd.concat(df_sections) # Add all the dataframes of the time_sections together again
                df_time_sections_bool_array = df_tmp.index.isin(df_result_tmp.index)  # Get a bool array of which elements we want to include based on the time sections

            #################################################
            ### Filter on player name is player name exists##
            #################################################
            if not (player_name == None):
                df_player_bool_array = df_tmp["Name"]==player_name  # Only keep data belonging to the player specified in player_name

            #################################################
            ### Check data against conditions ###############
            #################################################
            try:
                df_condition_bool_array = eval(condition)

                ### If it doesn't throw an error set key as vallid ###
                key_invalid.append(False)  # Save key value check result

            ### If not vallid save what went wrong ###
            except KeyError as e:
                key_invalid.append(True)  # Save key value check result
                print(e)  # Print error

            #################################################
            ### Change index to time index ##################
            #################################################

            ### Change DateTime index to Time index (We don't need the date) ###
            # df_result_tmp = df_tmp.copy() # Create hardcopy
            # time_column = [val.time() for val in df_result_tmp.index]
            # df_result_tmp['Time'] = [val.time() for val in df_result_tmp.index]

            df_result_tmp = df_tmp.copy()
            time_str_column = [str(val.strftime('%H:%M:%S.%f')) for val in self.df.index]
            df_result_tmp.insert(0,'Time',time_str_column)
            # df_tmp['Time'] = pd.Series([val.strftime('%H:%M:%S.%f') for val in self.df.index])

            #################################################
            ### Create boolean result array #################
            #################################################
            if (not (player_name == None)) & (self.time_file_toggle.isChecked() and not (self.input_file_path.text() == '')):  # All filters enabled
                df_results_bool = df_player_bool_array.values & df_time_sections_bool_array & df_condition_bool_array.values

            elif (not (player_name == None)):  # If only player filter was enabled
                df_results_bool = df_player_bool_array.values & df_condition_bool_array.values

            elif (self.time_file_toggle.isChecked() and not (self.input_file_path.text() == '')):  # If only time section filter was enabled
                df_results_bool = df_time_sections_bool_array & df_condition_bool_array.values

            else:  # If no filters were enabled
                df_results_bool = df_condition_bool_array.values

            #################################################
            ### Add padding if this was specified ###########
            #################################################
            if self.time_range_toggle.isChecked():

                ### Calculate number of frames the padding should be ###
                if self.input_file_freq_toggle:  # If user changed frame rate
                    padding_time = self.time_range_value.value()  # Get padding time
                    padding = math.floor(padding_time/(1/self.input_file_freq))  # Calculate number of samples we should pad the sections with
                    df_results_bool = self.padBoolArray(df_results_bool,padding)  # Apply padding
                else:
                    padding_time = self.time_range_value.value()  # Get padding time
                    padding = math.floor(padding_time/(1/freq))  # Calculate number of samples we should pad the sections with
                    df_results_bool = self.padBoolArray(df_results_bool,padding)  # Apply padding

            #################################################
            ### Get result data out of dataframe ############
            #################################################
            df_result_tmp = df_result_tmp[df_results_bool]

            #################################################
            ### Remove not specified columns ################
            #################################################

            ### Get keywords that are used in the condition ###
            keywords = [w.capitalize() for w in condition_tmp_1 if w.isalpha()]

            ### Remove not specified vars (columns) out of dataframe ###
            if self.output_columns_toggle:  # Use user settings
                keywords_tmp = ['Timestamp','Time']+self.output_columns  # Append 'Timestamp' and 'Time columns to output columns
                df_result_tmp = df_result_tmp[self.output_columns]  # Use user defined columns

            else:  # Use only columns specified in the conditions
                keywords_tmp = ['Timestamp','Time']+keywords  # Append 'Timestamp' and 'Time columns to output columns
                df_result_tmp = df_result_tmp[keywords_tmp]

            #################################################
            ### Save condition result to xlsx file object ###
            #################################################
            df_result_tmp = df_result_tmp.sort_index()
            df_result_tmp.to_excel(writer, sheet_name=condition_text.text(),index=False)
            del df_result_tmp  # Remove temporary results dataframe

        ### If keys were not vallid display error message ###
        if any(key_invalid):

                ### Make key condition index error display string ###
                key_invalid_idx_list = [ii+1 for ii, x in enumerate(key_invalid) if x == True]
                key_condition_error_str = ', '.join(map(str, key_invalid_idx_list)) if len(key_invalid_idx_list) != 2 else ' & '.join(map(str, key_invalid_idx_list))
                key_vallid_list = df_tmp.columns
                key_vallid_list_error_str = ', '.join(map(str, key_vallid_list)) if len(key_vallid_list) != 2 else ' & '.join(map(str, key_vallid_list))

                ### Send feedback that data analysis has not been performed successfully ###
                return (False, "key_error", key_condition_error_str, key_vallid_list_error_str) # (Data analysis result, return message)

        ### Otherwise save results to xlsx file ###
        else:

            ### Send progress to dialog console ###
            if player_name:
                ready_signal.emit("Saving results for player %s to a xlsx file..." % player_name) # When player filter is enabled
            else:
                ready_signal.emit("Saving results to xlsx file...")  # When player filter is not enabled

            ### Save results to xlsx file ###
            try:
                writer.save()
            except Exception as e:
                save_error_str = "Unfortunately the results for player " + player_name + """ could not be saved to a xlsx file.
                Please check if you have the right permissions to write to the (""" + ("%s) folder." % self.output_file_path.text()) + """ If problems
                persist please contact the developer."""
                return (False,"save_error", save_error_str, e)

            ## Display save successful message ##
            if player_name:
                ready_signal.emit("Results for player %s successfully save to a xlsx file!" % player_name) # When player filter is enabled
            else:
                ready_signal.emit("Results successfully saving to a xlsx file!" )  # When player filter is not enabled

            ### Print done message ###
            if player_name:
                ready_signal.emit("Data analysis for %s completed!"%player_name)
            else:
                ready_signal.emit("Data analysis completed!")

            ### Send feedback that data analysis was successfull ###
            return (True,)

    #################################################
    #### Close even function                     ####
    #################################################
    def closeEvent(self):
        '''This method gets called when the user closes the GUI. This method performs some extra
        actions to make sure all threads are killed and all timers stopped.'''

        pass

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
    CGDAT_icon = os.path.join(dirname, '..', r'media\cgdat_new.png')
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(CGDAT_icon), QtGui.QIcon.Normal, QtGui.QIcon.Off)
    MainWindow.setWindowIcon(icon)

    ### Show main window ###
    MainWindow.showMaximized()
    sys.exit(app.exec_())