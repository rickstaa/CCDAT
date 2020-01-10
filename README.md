# Conditional Game Data Analyse Tool (CGAT)

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/affacdc15e004c02a4bffe9bb1d65ae9)](https://www.codacy.com/app/rickstaa/CGDAT?utm_source=github.com&utm_medium=referral&utm_content=rickstaa/CGDAT&utm_campaign=Badge_Grade)
[![Maintained](https://img.shields.io/badge/maintained%3F-yes-brightgreen.svg?style=flat)](https://github.com/rickstaa/CGDAT/pulse)
[![Contributions](https://img.shields.io/badge/contributions-welcome-orange.svg)](contributing.md)
[![Python 3](https://img.shields.io/badge/python%203-3.7%20%7C%203.6%20%7C%203.5-green.svg)](https://www.python.org/)
[![os windows](https://img.shields.io/badge/os-windows-informational)](https://www.microsoft.com)

![logo](https://github.com/rickstaa/CGDAT/blob/master/cgdat/static/media/CGDAT_small.png)

This package contains a simple csv data analyse GUI which I created for a friend of mine to help him with his data analysis.

## Installation

### OS X & Linux

```sh
pip install cgdat
```

⚠ This package was only tested on the windows operation system. ⚠

### Windows

```sh
pip install cgdat
```

## Usage

This package can both be imported as a python package or run as a stand alone gui. To import the python package use `import cgdat`. To use as a stand alone package run the `cgdat-gui` cmd.

### Tool interface

![GUI](https://github.com/rickstaa/CGDAT/blob/master/cgdat/static/media/gui_overview.png)

### Functions

This repository can be used to perform a simple csv game data filtering. The tool can filter a input data file based on:

-   Conditions:
    -   Example: `Speed > 10 & Acceleration &lt; 5`

-   A time section file:
    -   A file containing a `Start Time` and `End Time` column specifying the sections where you want to apply the condition filter.

-   Player name:
    -   In the gui you can specify for which players you want to conduct the analysis. For this option to work the `input_data.csv` file needs to contain a `Name` column.

Further you can add also add a safety padding to the data filtering. Meaning that the program will also include a number of samples before and after the specified conditions are met.

### Console commands

This package also installs some additional console commands:

-   `cgdat-gui` - This will launch the CGDAT gui.
-   `cgdat-shortcut` - This will create a shortcut to launch the GUI on your desktop folder.

## Further documentation

Additional documentation can be loaded in the GUI by clicking the `documentation` option in the help menu or pressing the `F2` shortcut.

## Development setup

If you want to manually install the python package please fork from [github](https://github.com/rickstaa/CGDAT) and run the following commands:

```sh
python setup.py build
python setup.py develop
python setup.py install
```

## Contributing

Contributions to this repository are welcome. See the [contribution guidelines](contributing.md) for more information.

## License

[MIT](LICENSE)
