# subclass
'''This module contains classes and functions that add added custom made widgets and functionalities to the qt GUI. It contains the
following components:

**Classes:**
.. autosummary::
   :toctree: _autosummary

    CheckableComboBox
'''

### Import needed modules ###
from PyQt5 import QtGui, QtCore, QtWidgets
import sys, os

# TODO: Add all option that selects all items

###################################################################
### CheckableComboBox Class                                     ###
###################################################################
class MultiSelectMenu(QtWidgets.QToolButton):
    """This class is used to create a multi selection drop down menu.
    """

    #################################################
    ### Class initializer                         ###
    #################################################
    def __init__(self):
        """Initialize object."""

        ### Run parent initializer and setup components ###
        super(MultiSelectMenu, self).__init__()
        self.setText('Select Categories ')
        self.toolmenu = QtWidgets.QMenu(self)
        self.setMenu(self.toolmenu)
        self.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolmenu.installEventFilter(self)
        self.all_text_enabled = False  # Specify whether a all text is enabled

    #################################################
    ### addItem method                            ###
    #################################################
    def addItem(self, item):
        """Method used to add additional actions to the toolbar menu."""

        ### Add item to menu ###
        action = self.toolmenu.addAction(item)
        action.setCheckable(True)

    #################################################
    ### addAllOption method                       ###
    #################################################
    def addAllOption(self, all_text="Select all"):
        """This function is used to add a "Select all" action to the toolbar menu.

        Args:
            all_text (str, optional): Defaults to "Select all". The text used for the select all element.
        """

        ### Set all_text if specified ###
        self.all_text = all_text

        ### Add all action to menu ###
        action = QtWidgets.QAction(self)
        action.setText(all_text)
        action.setCheckable(True)
        action.changed.connect(self.selectAll)
        self.toolmenu.insertAction(self.toolmenu.actions()[0], action)
        self.all_text_enabled = True

    #################################################
    ### removeAllOption method                       ###
    #################################################
    def removeAllOption(self):
        """This function is used to remove a "Select all" action to the toolbar menu.
        """

        ### Remove select all element if it exists ###
        if self.all_text_enabled:
            self.all_text_enabled = False  # Set select all text to false
            self.toolmenu.removeAction(self.toolmenu.actions()[0])
        else:
            print("No select all action was found.")

    #################################################
    ### selectAll method                          ###
    #################################################
    def selectAll(self):
        """This method is used to select all the options when the select all action is selected
        """

        ### Check or unchecked the other actions based on the "Select all" action ###
        if self.toolmenu.actions()[0].isChecked():  # If "Select all" action is checked
            for action in self.toolmenu.actions()[1:]:
                action.setChecked(1)  # Check actions
        else:
            for action in self.toolmenu.actions()[1:]:
                action.setChecked(0) # Uncheck all actions

    #################################################
    ### selectedItems method                      ###
    #################################################
    def selectedItems(self):
        """This method returns a list containing the items that were selected in the toolbox menu.

        Returns:
            list: List containing the items that were selected.
        """

        ### Create selected items list ###
        selected_items = []

        ### Loop through the toolbar menu and return selected items ###
        if self.all_text_enabled:
            for action in self.toolmenu.actions()[1:]:
                if action.isChecked():  # Check if item is checked
                    selected_items.append(action.text())  # Append item text to list
        else:
            for action in self.toolmenu.actions():
                if action.isChecked():  # Check if item is checked
                    selected_items.append(action.text())  # Append item text to list

        ### Return result ###
        return selected_items

    #################################################
    ### eventFilter method                        ###
    #################################################
    def eventFilter(self, obj, event):
        """This function is used to slightly edit the open and close behaviour of the
        QToolButton. This was done since we want the toolbar drop down menu to stay open
        when the user is selecting players.

        Args:
            obj (QObject): The object on which the event filter needs to be applied.
            event (QEvent): The QEvent we want to overwrite.

        Returns:
            QEvent: Pass the event to the parent class.
        """

        ### Check if the mouse button is released ###
        if event.type() in [QtCore.QEvent.MouseButtonRelease]:
            if isinstance(obj, QtWidgets.QMenu):
                if obj.activeAction():
                    if not obj.activeAction().menu(): #if the selected action does not have a submenu
                        #eat the event, but trigger the function
                        obj.activeAction().trigger()
                        return True

        ### Return event ###
        return super(MultiSelectMenu, self).eventFilter(obj, event)