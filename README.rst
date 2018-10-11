Sudoku-Tk - Sudoku games and puzzle solver
==========================================
Copyright 2016-2018 Juliette Monsel <j_4321@protonmail.com>

|Release| |License|

Sudoku-Tk is a software written in Python 3 with a Tk GUI.
It enables you to play sudoku and to solve sudoku puzzles.
You can start from an empty grid, load puzzles or generate them.
You can save the game to continue later and there is a timer.

Sudoku-Tk should work on any OS provided the dependencies are installed. 
No compilation is needed since Python is an interpreted language.

Prerequisites
-------------

This software is based on Python 3 and Tkinter interface so you will need
to have them installed to use it. This software also depends on the additionnal
python libraries Pillow and Numpy.

Windows
~~~~~~~

Install:

- Python 3: https://www.python.org/downloads/windows/
- Pillow: https://pypi.python.org/pypi/Pillow/
- Numpy: https://pypi.python.org/pypi/numpy

In all cases, be careful to choose the Python 3 versions
(it won't work with Python 2)

Or install Pillow and Numpy with pip:

::

    pip install numpy pillow
    

Linux
~~~~~

Install with your package manager the following packages (names might
slightly change according to the distribution):

Ubuntu/Debian:

::

    $sudo apt-get install python3-tk python3-pil python3-numpy

If you use tcl/tk < 8.6, you will also need python3-pil.imagetk

Archlinux:

::

    $sudo pacman -S tk python-pillow python-numpy


Getting started
---------------

Unpack the archive. 

You can directly launch sudoku-tk

In Windows, you might need to select 'open with pythonw.exe' (which is in
the file C:\Python3x).

In Linux, you can make sudoku-tk.py executable or launch it with

::

    $ python3 sudoku-tk


You can also install it with

::

    $ python3 setup.py install 


Note
----

If you had installed version 1.1 and you are updating to 1.2, please 
uninstall all files from the previous version otherwise the old module
SudokuTkModules (renamed sudokutk) will stay in your system.

Troubleshooting
---------------

If you encounter bugs or if you have suggestions, please open an issue on
`GitHub <https://github.com/j4321/CheckMails/issues>`__ or write me an email
at <j_4321@protonmail.com>.


.. |Release| image:: https://badge.fury.io/gh/j4321%2FSudoku-Tk.svg
    :alt: Latest Release
    :target: https://github.com/j4321/Sudoku-Tk/releases
.. |License| image:: https://img.shields.io/github/license/j4321/Sudoku-Tk.svg
    :target: https://www.gnu.org/licenses/gpl-3.0.en.html
