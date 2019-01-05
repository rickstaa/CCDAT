'''This function creates a shortcut which can be used to run the CGDAT tool'''

### Import needed modules ###
import os, winshell
from win32com.client import Dispatch

### Get relative script path ###
DIRNAME = os.path.dirname(os.path.abspath(__file__))

### Set paths ###
desktop = winshell.desktop()
path = os.path.join(desktop, "CGDAT.lnk")
target = r"cgdat-gui"
icon_path = os.path.abspath(os.path.join(DIRNAME, "static/media/CGDAT.svg")).replace('\\','/')    # Toggle on icon

##############################################################
#### Create shortuct function                             ####
##############################################################
def main():

    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(path)
    shortcut.Targetpath = target
    shortcut.IconLocation = icon_path
    shortcut.save()

main()