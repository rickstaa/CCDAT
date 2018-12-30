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
class CheckableComboBox(QtWidgets.QComboBox):
    """This class is used add multi check functionality to the QComboBox.

    Args:
        default_text_holder (str, optional): Defaults to None. The default text holder that is shown when the QComboBox is not selected.
    """

    #################################################
    ### Class initializer                         ###
    #################################################
    def __init__(self, default_text_holder=None):
        """Initialize object.
        """


        ### Run parent initializer and constructors ###
        super(CheckableComboBox, self).__init__()
        self.default_text_holder = default_text_holder

        ### Setup default textholder ###
        if default_text_holder:
            super(CheckableComboBox, self).addItem(default_text_holder)

    #################################################
    ### setDefaultTextHolder method               ###
    #################################################
    def setDefaultTextHolder(self, default_text_holder):
        """This function is used to remove a default text holder for the QComboBox. This default text holder is shown
        when the QComboBox is not selected.

        Args:
            default_text_holder (str, optional): Defaults to None. The default text holder that is shown when the QComboBox is not selected.
        """

        ### Add default text holder to QComboBox ###
        if self.default_text_holder:  # If default text holder already exists
            self.default_text_holder = default_text_holder
            item = self.model().item(0,0)
            item.setText(self.default_text_holder)
        else:
            self.default_text_holder = default_text_holder
            self.insertItem(0, default_text_holder)

    #################################################
    ### removeDefaultTextHolder method            ###
    #################################################
    def removeDefaultTextHolder(self):
        """This function is used to remove a default text holder for the QComboBox. This default text holder is shown
        when the QComboBox is not selected.
        """

        ### Remove default text holder if it is present ###
        if self.default_text_holder:
            self.default_text_holder = None
            self.removeItem(0)
        else:
            print("No default text holder was set for the QCheckBox.")

    #################################################
    ### addItem method                            ###
    #################################################
    def addItem(self, item):
        """This function overloads the original addItem function of the QComboBox class in order to add
        the multi checkable items functionality.

        Args:
            item (str): The QComboBox item.
        """

        ### Add item to QComboBox ###
        super(CheckableComboBox, self).addItem(item)  # Run parrent addItem method
        item = self.model().item(self.count()-1,0)  # Get item object
        item.setFlags(QtCore.Qt.ItemIsUserCheckable | QtCore.Qt.ItemIsEnabled)  # Enable multiselect functionality
        item.setCheckState(QtCore.Qt.Unchecked)

    def clear(self):
        """Function that overloads the original clear function of the QComboBox class so the default text holder is not removed.
        """

        ### Run parent method ###
        super(CheckableComboBox, self).clear()  # Run parrent addItem method

        ### Add default text holder again ###
        if self.default_text_holder:  # If default text exist add it to the QComboBox
            self.insertItem(0, self.default_text_holder)

    #################################################
    ### itemChecked method                        ###
    #################################################
    def itemChecked(self, index):
        """This function is created to check whether an item of the multi check QComboBox is checked.

        Args:
            index (int): Index of the item you want to check.

        Returns:
            bool: Boolean specifying whether the item was checked.
        """

        ### Get item
        item = self.model().item(index,0)
        return item.checkState() == QtCore.Qt.Checked

    #################################################
    ### itemsChecked method                       ###
    #################################################
    def itemsChecked(self):
        """This function is created to get a list of the items that were checked..

        Returns:
            dict: A dictionary containing all the items that were checked.
        """

        ### Create results list ###
        checked_items = []

        ### Loop through al the items and append them to the list when checked ###
        for ii in range(0,self.count()):
            item = self.model().item(ii,0) # Get item

            ## Append item text to list if it was checked ##
            if (item.checkState() == QtCore.Qt.Checked):
                checked_items.append(self.model().item(ii).text())

        ### Return dictionary with the result ###
        return checked_items

class multiSelectMenu():

    def __init__(self):
        self.toolbutton = QtWidgets.QToolButton(self)
        self.toolbutton.setText('Select Categories ')
        self.toolmenu = QtWidgets.QMenu(self)
        for i in range(3):
            action = self.toolmenu.addAction("Category " + str(i))
            action.setCheckable(True)
        self.toolbutton.setMenu(self.toolmenu)
        self.toolbutton.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        self.toolmenu.installEventFilter(self)

    def eventFilter(self, obj, event):
        if event.type() in [QtCore.QEvent.MouseButtonRelease]:
            if isinstance(obj, QtWidgets.QMenu):
                if obj.activeAction():
                    if not obj.activeAction().menu(): #if the selected action does not have a submenu
                        #eat the event, but trigger the function
                        obj.activeAction().trigger()
                        return True
        return super(multiSelectMenu, self).eventFilter(obj, event)