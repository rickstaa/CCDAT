'''Python function used to install the CGDAT package, its dependencies and create a shortcut.'''

### Import needed modules ###
import win32com.client
import sys
import re
import re
import os
import subprocess

### Get python executable path and script path ###
dirname = os.path.dirname(os.path.abspath(__file__))
target_location = os.path.abspath(os.path.join(dirname, '..', "cgdat.lnk")).replace('\\','/')    # Toggle on icon
icon_path = os.path.abspath(os.path.join(dirname, '..', "cgdat/static/media/CGDAT.ico")).replace('\\','/')    # Toggle on icon
cgdat_path = os.path.abspath(os.path.join(dirname, "start_cgdat.py")).replace('\\','/')    # Toggle on icon

### Get working directory ###
DIRNAME = os.path.dirname(os.path.abspath(__file__))
DIRNAME_ONE_UP = os.path.abspath(os.path.join(DIRNAME, "..")).replace('\\','/')
print(DIRNAME_ONE_UP)

### Create paths ###
SPHINX_AUTO_RST_PATH = os.path.abspath(os.path.join(DIRNAME_ONE_UP, "docs/source/_auto_rst")).replace('\\','/')
CGDAT_PACKAGE_PATH = os.path.abspath(os.path.join(DIRNAME_ONE_UP, "cgdat")).replace('\\','/')
SCRIPTS_FOLDER_PATH = os.path.abspath(os.path.join(DIRNAME_ONE_UP, "scripts")).replace('\\','/')
SETUP_PY_PATH = os.path.abspath(os.path.join(DIRNAME_ONE_UP, "setup.py")).replace('\\','/')

##############################################################
#### Create shortuct function                             ####
##############################################################
if __name__ == '__main__':

    ### Build documentation ###

    # subprocess.call(['sphinx-apidoc', '-o', SPHINX_AUTO_RST_PATH, CGDAT_PACKAGE_PATH])  # Run autodocumentation
    # subprocess.call(['sphinx-apidoc', '-o', SPHINX_AUTO_RST_PATH, SCRIPTS_FOLDER_PATH])  # Run autodocumentation
    # subprocess.call(['python', SETUP_PY_PATH, 'build_sphinx']) # Creatw HTML

    ### Build the program ###
    subprocess.call(['python', SETUP_PY_PATH,'build'])

    ### Develop the program ###
    # subprocess.call(['python', SETUP_PY_PATH,'develop'])

    ### Install the program ###
    subprocess.call(['python', SETUP_PY_PATH, 'install'])

    ### Create shortcut ##
    python_exe = sys.executable
    python_exe_path = re.sub('\\\\python.exe', '', python_exe)
    pythonw_exe_path = python_exe_path + "\\\\pythonw.exe"
    ws = win32com.client.Dispatch("wscript.shell")
    scut = ws.CreateShortcut(target_location)
    scut.TargetPath = pythonw_exe_path
    scut.Arguments = cgdat_path
    scut.IconLocation = icon_path
    scut.Save()
