.. role:: raw-html(raw)
   :format: html

Conditional Game Data Analyse Tool (CGAT)
===================================================
This package contains a simple csv data analyse GUI which I created for a friend of mine to help him with his data analysis.

.. image:: https://img.shields.io/badge/python-3.7-blue.svg
   :target: https://www.python.org/downloads/release/python-370/
   :alt: Python version badge

.. image:: https://img.shields.io/badge/maintained%3F-yes!-brightgreen.svg?style=flat
   :target: https://github.com/rickstaa/CGDAT
   :alt: Maintained badge

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0
   :alt: License badge 

:raw-html:`<br />`

.. image:: https://github.com/rickstaa/CGDAT/blob/master/cgdat/static/media/CGDAT_small.png
   :target: https://github.com/rickstaa/CGDAT
   :alt: CGDAT LOGO

Installation
=====================

Install using the python package index (PyPi)
---------------------------------------------------

OS X & Linux:
^^^^^^^^^^^^^^^

::

    pip install cgdat

.. image:: https://github.com/rickstaa/CGDAT/blob/master/cgdat/static/media/linux_mac_warning.png
   :alt: Warning box

Windows:
^^^^^^^^^^^^^^^

::

    pip install cgdat

Development setup
------------------------------

If you want to manually install the python package please fork from `github <https://github.com/rickstaa/CGDAT>`_ and run the following commands::

    python setup.py build
    python setup.py develop
    python setup.py install

A overview of the CGDAT GUI.

Usage
=====================================
This package can both be imported as a python package or run as a stand alone gui (see :numref:`figure_1`). To import the python package use :samp:`import cgdat`. To use as a stand alone package run the :samp:`cgdat-gui` cmd.

Tool interface
-------------------------

.. figure:: https://github.com/rickstaa/CGDAT/blob/master/cgdat/static/media/gui_overview.png
   :scale: 100 %
   :alt: A overview of the CGDAT GUI window.
   :name: figure_1

   A overview of the CGDAT GUI.

Functions
-----------------------

This repository can be used to perform a simple csv game data filtering. The tool can filter a input data file based on:

* Conditions:
    * Example: Speed > 10 & Acceleration < 5
* A time section file:
    * A file containing a :samp:`Start Time` and :samp:`End Time` column specifying the sections where you want to apply the condition filter.
* Player name:
    * In the gui you can specify for which players you want to conduct the analysis. For this option to work the :samp:`input_data.csv` file needs to contain a :samp:`Name` column.

Further you can add also add a safety padding to the data filtering. Meaning that the program will also include a number of samples before and after the specified conditions are met.

Console commands
--------------------------

This package also installs some additional console commands:

* :samp:`cgdat-gui` - This will launch the CGDAT gui.
* :samp:`cgdat-shortcut` - This will create a shortcut to launch the GUI on your desktop folder.

Further documentation
==============================

Additional documentation can be loaded in the GUI by clicking the `documentation` option in the help menu or pressing the `F2` shortcut.

Additional information
===============================

Licence
-------------------------------
This tool is licensed under the GPL open source license. You are therefore free use the source code in any way provided that you the original copyright statements.

Release History
--------------------------------
* 2.0.2:

    * CHANGE: Updated the setup.py and the project Readme.md.

* 2.0.1:

    * CHANGE(docs): Updated docs (module code remains unchanged).

* 2.0.0:

    * First proper release on PiPy.

Meta
-----------------------------------------------

Rick Staa – `@github <https://github.com/rickstaa>`_

Distributed under the GNU General Public License v3 (GPLv3). See :samp:'`LICENSE <https://github.com/rickstaa/CGDAT/blob/master/LICENSE>`_' for more information.

Contributing
----------------------------------

1. Fork it (<https://github.com/rickstaa/CGDAT>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

Contributors
-----------------------------
* Created by Rick Staa
* Maintained by Wesley Bosman `(wesleybosmann@gmail.com <mailto:wesleybosmann@gmail.com>`_)

Credits
-----------------------------
* CDAT icon created by FreePis from `www.flaticon.com <https://www.flaticon.com>`_.

