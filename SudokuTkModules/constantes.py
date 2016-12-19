#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Sudoku-Tk - Sudoku games and puzzle solver
Copyright 2016 Juliette Monsel <j_4321@sfr.fr>

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
from PIL import Image, ImageTk
from locale import getdefaultlocale
import os
import gettext

PL = platform[0]

# Traduction

APP_NAME = "Sudoku-Tk"

# Get the local directory since we are not installing anything
PATH = os.path.split(__file__)[0]

# Init the list of languages to support

FILES_LOCATION = os.path.join(PATH, 'Files')
if os.access(PATH, os.W_OK): # l'utilisateur à les droits en écriture sur le chemin
    INITIALDIR = os.path.split(PATH)[0] # pour enregister / importer ...
else:
    INITIALDIR = os.path.expanduser("~") # pour enregister / importer ...


# Check the default locale
lc = getdefaultlocale()[0][:2]
if lc == "fr":
    # If we have a default, it's the first in the list
    LANGUE = "fr_FR"
else:
    LANGUE = "en_US"
# Now langs is a list of all of the languages that we are going
# to try to use.  First we check the default, then what the system
# told us, and finally the 'known' list

gettext.find(APP_NAME, FILES_LOCATION)
gettext.bind_textdomain_codeset(APP_NAME, "UTF - 8")
gettext.bindtextdomain(APP_NAME, FILES_LOCATION)
gettext.textdomain(APP_NAME)


# Get the language to use
lang = gettext.translation(APP_NAME, FILES_LOCATION,
                           languages=[LANGUE], fallback=True)
# Install the language, map _() (which we marked our
# strings to translate with) to self.lang.gettext() which will
# translate them.



# chemins des images
PLAY = os.path.join(FILES_LOCATION, "play.png")
PAUSE = os.path.join(FILES_LOCATION, "pause.png")
UNDO = os.path.join(FILES_LOCATION, "undo.png")
INFO = os.path.join(FILES_LOCATION, "info.png")
REDO = os.path.join(FILES_LOCATION, "redo.png")
ERREUR = os.path.join(FILES_LOCATION, "erreur.png")
QUESTION = os.path.join(FILES_LOCATION, "question.png")
ICONE = os.path.join(FILES_LOCATION, "icone_24.png")
ICONE_WIN = os.path.join(FILES_LOCATION, "icone.ico")
ICONE_48 = os.path.join(FILES_LOCATION, "icone_48.png")

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


VERSION = "1.0"

if PL == "w":
    STYLE = None
else:
    STYLE = 'clam'

def set_icon(fen):
    """ icône de l'application """
    if PL == 'w':
        fen.iconbitmap(ICONE_WIN, ICONE_WIN)
    else:
        icon = ImageTk.PhotoImage(Image.open(ICONE))
        fen.tk.call('wm', 'iconphoto', fen._w, icon)