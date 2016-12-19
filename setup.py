#! /usr/bin/python3
# -*- coding:Utf-8 -*-

from distutils.core import setup

#This is a list of files to install, and where
#(relative to the 'root' dir, where setup.py is)
#You could be more specific.




files = ["Files/*","Files/en_US/LC_MESSAGES/*","Files/fr_FR/LC_MESSAGES/*"]




setup(name = "Sudoku-Tk",
      version = "1.0",
      description = "Sudoku games and puzzle solver",
      author = "Juliette Monsel",
      author_email = "j_4321@sfr.fr",
      url = "http://sourceforge.net/projects/sudoku-tk/",
      license = "GNU General Public License v3",
      #Name the folder where your packages live:
      #(If you have other packages (dirs) or modules (py files) then
      #put them into the package directory - they will be found
      #recursively.)
      packages = ['SudokuTkModules'],
      #'package' package must contain files (see list above)
      #I called the package 'package' thus cleverly confusing the whole issue...
      #This dict maps the package name =to=> directories
      #It says, package *needs* these files.
      package_data = {'SudokuTkModules' : files },
      #'runner' is in the root.
      scripts = ["sudoku-tk.py"],
      long_description = """ Sudoku-Tk enables you to play sudoku. You can load puzzles, generate puzzles or start from an empty grid. Sudoku-Tk can also solve the sudoku. """,
      requires = ["PIL", "tkinter", "sys", "os", "tkinter.ttk", "tkinter.filedialog", "pickle", "locale", "gettext", "numpy", "webbrowser"]
)





