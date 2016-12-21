Sudoku-Tk - Sudoku games and puzzle solver
==========================================
Copyright 2016 Juliette Monsel <j_4321@protonmail.com>

Sudoku-Tk is a software written in Python 3 with a Tk GUI.
It enables you to play sudoku and to solve sudoku puzzles.
You can start from an empty grid, load puzzles or generate them.
You can save the game to continue later and there is a timer.

Windows version
---------------


Download Sudoku-Tk-x.y-windows.7z

Unpack the archive

Launch Sudoku-Tk from the shortcut in the folder, it is a
standalone software.


Souce code
----------

It should work on any OS provided the dependencies are installed. 
No compilation is needed since Python is an interpreted language.

1. Prerequisites

This software is based on Python 3 and Tkinter interface so you will need
to have them installed to use it. You might need to install some 
additionnal python libraries.

1.1. Windows users

Install Python 3: https://www.python.org/downloads/windows/
Install Pillow: https://pypi.python.org/pypi/Pillow/
Install Numpy: https://pypi.python.org/pypi/numpy

In all cases, be careful to choose the Python 3 versions
(it won't work with Python 2)

1.2. Linux users

Install with your package manager the following packages (names might
slightly change according to the distribution):

Ubuntu/Debian:

- python3-tk

- python3-pil

- python3-numpy


If you use a 8.5.x version of tcl/tk, you will also need 

- python3-pil.imagetk

Archlinux:

- tk

- python-pillow

- python-numpy


2. Getting started

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


If you have any troubles or comments, don't hesitate to send me an email
at j_4321@protonmail.com
