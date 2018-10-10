#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Sudoku-Tk - Sudoku games and puzzle solver
Copyright 2016 Juliette Monsel <j_4321@protonmail.com>

Sudoku-Tk is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Sudoku-Tk is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Constants and global functions of Sudoku Game
"""

from sys import platform
from configparser import ConfigParser
from locale import getdefaultlocale
import os
import gettext
from tkinter import TclVersion

VERSION = "1.2.0"

PL = platform[0]

# Traduction

APP_NAME = "Sudoku-Tk"

# local directory
PATH = os.path.split(__file__)[0]

LOCALE_PATH = os.path.join(PATH, 'locale')


# default path to save, open ...
if os.access(PATH, os.W_OK):
    # user has writing rights on the path
    INITIALDIR = os.path.split(PATH)[0]  # pour enregister / importer ...
else:
    INITIALDIR = os.path.join(os.path.expanduser("~"), "Sudoku-Tk")

CONFIG = ConfigParser()
PATH_CONFIG = os.path.join(INITIALDIR, "sudoku-tk.ini")
PATH_SAVE = os.path.join(INITIALDIR, ".last.sudoku")

if os.path.exists(PATH_CONFIG):
    CONFIG.read(PATH_CONFIG)
    LANGUE = CONFIG.get("General", "language")
else:
    if not os.path.exists(INITIALDIR):
        os.mkdir(INITIALDIR)
    CONFIG.add_section("General")
    CONFIG.add_section("Statistics")
    CONFIG.set("Statistics", "easy", "")
    CONFIG.set("Statistics", "medium", "")
    CONFIG.set("Statistics", "difficult", "")
    # use the default locale to set the language
    lc = getdefaultlocale()[0][:2]
    if lc == "fr":
        LANGUE = "fr_FR"
    else:
        LANGUE = "en_US"
    CONFIG.set("General", "language", LANGUE)


gettext.find(APP_NAME, LOCALE_PATH)
gettext.bind_textdomain_codeset(APP_NAME, "UTF - 8")
gettext.bindtextdomain(APP_NAME, LOCALE_PATH)
gettext.textdomain(APP_NAME)


# Get the language to use
LANG = gettext.translation(APP_NAME, LOCALE_PATH,
                           languages=[LANGUE], fallback=True)
LANG.install()

# chemins des images
IMAGES_LOCATION = os.path.join(PATH, 'images')

PLAY = os.path.join(IMAGES_LOCATION, "play.png")
PAUSE = os.path.join(IMAGES_LOCATION, "pause.png")
RESTART = os.path.join(IMAGES_LOCATION, "restart.png")
UNDO = os.path.join(IMAGES_LOCATION, "undo.png")
INFO = os.path.join(IMAGES_LOCATION, "info.png")
REDO = os.path.join(IMAGES_LOCATION, "redo.png")
ERREUR = os.path.join(IMAGES_LOCATION, "erreur.png")
QUESTION = os.path.join(IMAGES_LOCATION, "question.png")
ICONE = os.path.join(IMAGES_LOCATION, "icone_24.png")
ICONE_WIN = os.path.join(IMAGES_LOCATION, "icone.ico")
ICONE_48 = os.path.join(IMAGES_LOCATION, "icone_48.png")


PUZZLES_LOCATION = os.path.join(PATH, 'puzzles')
# emplacement du fichier log (pour pouvoir annuler)
nb = 0
if PL == "w":
    LOG = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Temp", "sudoku-tk%i.log")
else:
    LOG = "/tmp/sudoku-tk%i.log"
while os.path.exists(LOG % nb):
    nb += 1
LOG = LOG % nb
# le fichier log est structuré comme suis :
# i\tj;val_prec\tpos_prec;modifs;val\tpos
# où (i,j) = coordonnées de la case modifiée,
# val_prec, pos_prec : contenu de la case avant modif
# val, pos : contenu de la case après modif
# modifs : sous la forme i0,j0\ti1,j1 ..., liste des cases qui ont été modifiées
# lors de l'ajout de la valeur val dans la case (i,j)
# (à cause de la fonction update_grille)


if PL == "w":
    STYLE = None
else:
    STYLE = 'clam'

if TclVersion < 8.6:
    # then tkinter cannot import PNG files directly, we need to use PIL
    from PIL import ImageTk, Image
    from SudokuTkModules.custom_messagebox import ob_checkbutton
    if not CONFIG.has_option("General", "old_tcl_warning") or CONFIG.getboolean("General", "old_tcl_warning"):
        ans = ob_checkbutton(title=_("Information"),
                             message=_("This software has been developped using Tcl/Tk 8.6, but you are using an older version. Therefore there might be errors. Please consider upgrading your Tcl/Tk version."),
                             checkmessage=_("Do not show this message again."))
    CONFIG.set("General", "old_tcl_warning", str(not ans))

    def open_image(file, master=None):
        return ImageTk.PhotoImage(Image.open(file))

else:
    # no need of ImageTk dependency
    from tkinter import PhotoImage

    def open_image(file, master=None):
        return PhotoImage(file=file, master=master)


def set_icon(fen):
    """ icône de l'application """
    if PL == 'w':
        fen.iconbitmap(ICONE_WIN, ICONE_WIN)
    else:
        icon = open_image(ICONE)
        fen.tk.call('wm', 'iconphoto', fen._w, icon)
