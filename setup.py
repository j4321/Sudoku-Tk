#! /usr/bin/python3
# -*- coding:Utf-8 -*-

from distutils.core import setup
from sys import platform

files = ["puzzles/easy/*", "puzzles/medium/*", "puzzles/difficult/*",
         "images/*","locale/en_US/LC_MESSAGES/*","locale/fr_FR/LC_MESSAGES/*"]
if platform == "linux":
    data_files = [("/usr/share/applications", ["sudoku-tk.desktop"]),
                  ("/usr/share/pixmaps", ["sudoku-tk.png"])]
else:
    data_files = []

setup(name = "sudoku-tk",
      version = "1.1",
      description = "Sudoku games and puzzle solver",
      author = "Juliette Monsel",
      author_email = "j_4321@protonmail.com",
      url = "https://sourceforge.net/p/sudoku-tk-j4321",
      license = "GNU General Public License v3",
      packages = ['SudokuTkModules'],
      package_data = {'SudokuTkModules': files},
      scripts = ["sudoku-tk"],
      data_files = data_files,
      long_description = """ Sudoku-Tk enables you to play sudoku. You can load puzzles, generate puzzles or start from an empty grid. Sudoku-Tk can also solve the sudoku. """,
      requires = ["PIL", "tkinter", "sys", "os", "configparser", "pickle", "locale", "gettext", "numpy", "webbrowser"]
)





