#! /usr/bin/python3
# -*- coding: utf-8 -*-
"""
Sudoku-Tk - Sudoku games and puzzle solver
Copyright 2016-2018 Juliette Monsel <j_4321@protonmail.com>

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

The png icons are modified versions of icons from the elementary project
(the xfce fork to be precise https://github.com/shimmerproject/elementary-xfce)
Copyright 2007-2013 elementary LLC.


Constants and global functions of Sudoku Game
"""

from sys import platform
from configparser import ConfigParser
from locale import getdefaultlocale
import os
import gettext
from tkinter import TclVersion
from subprocess import check_output, CalledProcessError
from tkinter import filedialog


VERSION = '1.2.1'

PL = platform[0]


# local directory
PATH = os.path.split(__file__)[0]

LOCALE_PATH = os.path.join(PATH, 'locale')


# --- default path to save, open ...
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

# --- translation
APP_NAME = "Sudoku-Tk"
gettext.find(APP_NAME, LOCALE_PATH)
gettext.bind_textdomain_codeset(APP_NAME, "UTF - 8")
gettext.bindtextdomain(APP_NAME, LOCALE_PATH)
gettext.textdomain(APP_NAME)


# Get the language to use
LANG = gettext.translation(APP_NAME, LOCALE_PATH,
                           languages=[LANGUE], fallback=True)
LANG.install()

# --- chemins des images
IMAGES_LOCATION = os.path.join(PATH, 'images')

PLAY = os.path.join(IMAGES_LOCATION, "play.png")
PAUSE = os.path.join(IMAGES_LOCATION, "pause.png")
RESTART = os.path.join(IMAGES_LOCATION, "restart.png")
UNDO = os.path.join(IMAGES_LOCATION, "undo.png")
INFO = os.path.join(IMAGES_LOCATION, "info.png")
REDO = os.path.join(IMAGES_LOCATION, "redo.png")
CHECK = os.path.join(IMAGES_LOCATION, "check.png")
ERREUR = os.path.join(IMAGES_LOCATION, "erreur.png")
QUESTION = os.path.join(IMAGES_LOCATION, "question.png")
ICONE = os.path.join(IMAGES_LOCATION, "icone_24.png")
ICONE_WIN = os.path.join(IMAGES_LOCATION, "icone.ico")
ICONE_48 = os.path.join(IMAGES_LOCATION, "icone_48.png")


PUZZLES_LOCATION = os.path.join(PATH, 'puzzles')
# emplacement du fichier log (pour pouvoir annuler)


if PL == "w":
    STYLE = None
else:
    STYLE = 'clam'


# ---  filebrowser
ZENITY = False

try:
    import tkfilebrowser as tkfb
except ImportError:
    tkfb = False

if PL != "w":
    paths = os.environ['PATH'].split(":")
    for path in paths:
        if os.path.exists(os.path.join(path, "zenity")):
            ZENITY = True


def askopenfilename(defaultextension, filetypes, initialdir, initialfile="", title=_('Open'), **options):
    """ plateform specific file browser:
            - defaultextension: extension added if none is given
            - initialdir: directory where the filebrowser is opened
            - filetypes: [('NOM', '*.ext'), ...]
    """
    if tkfb:
        return tkfb.askopenfilename(title=title,
                                    defaultext=defaultextension,
                                    filetypes=filetypes,
                                    initialdir=initialdir,
                                    initialfile=initialfile,
                                    **options)
    elif ZENITY:
        try:
            args = ["zenity", "--file-selection",
                    "--filename", os.path.join(initialdir, initialfile)]
            for ext in filetypes:
                args += ["--file-filter", "%s|%s" % ext]
            args += ["--title", title]
            file = check_output(args).decode("utf-8").strip()
            filename, ext = os.path.splitext(file)
            if not ext:
                ext = defaultextension
            return filename + ext
        except CalledProcessError:
            return ""
        except Exception:
            return filedialog.askopenfilename(title=title,
                                              defaultextension=defaultextension,
                                              filetypes=filetypes,
                                              initialdir=initialdir,
                                              initialfile=initialfile,
                                              **options)
    else:
        return filedialog.askopenfilename(title=title,
                                          defaultextension=defaultextension,
                                          filetypes=filetypes,
                                          initialdir=initialdir,
                                          initialfile=initialfile,
                                          **options)


def asksaveasfilename(defaultextension, filetypes, initialdir=".", initialfile="", title=_('Save As'), **options):
    """ plateform specific file browser for saving a file:
            - defaultextension: extension added if none is given
            - initialdir: directory where the filebrowser is opened
            - filetypes: [('NOM', '*.ext'), ...]
    """
    if tkfb:
        return tkfb.asksaveasfilename(title=title,
                                      defaultext=defaultextension,
                                      initialdir=initialdir,
                                      filetypes=filetypes,
                                      initialfile=initialfile,
                                      **options)
    elif ZENITY:
        try:
            args = ["zenity", "--file-selection",
                    "--filename", os.path.join(initialdir, initialfile),
                    "--save", "--confirm-overwrite"]
            for ext in filetypes:
                args += ["--file-filter", "%s|%s" % ext]
            args += ["--title", title]
            file = check_output(args).decode("utf-8").strip()
            if file:
                filename, ext = os.path.splitext(file)
                if not ext:
                    ext = defaultextension
                return filename + ext
            else:
                return ""
        except CalledProcessError:
            return ""
        except Exception:
            return filedialog.asksaveasfilename(title=title,
                                                defaultextension=defaultextension,
                                                initialdir=initialdir,
                                                filetypes=filetypes,
                                                initialfile=initialfile,
                                                **options)
    else:
        return filedialog.asksaveasfilename(title=title,
                                            defaultextension=defaultextension,
                                            initialdir=initialdir,
                                            filetypes=filetypes,
                                            initialfile=initialfile,
                                            **options)


# --- compatibility
if TclVersion < 8.6:
    # then tkinter cannot import PNG files directly, we need to use PIL
    from PIL import ImageTk, Image
    from sudokutk.custom_messagebox import ob_checkbutton
    if not CONFIG.has_option("General", "old_tcl_warning") or CONFIG.getboolean("General", "old_tcl_warning"):
        ans = ob_checkbutton(title=_("Information"),
                             message=_("This software has been developped using Tcl/Tk 8.6, but you are using an older version. Therefore there might be errors. Please consider upgrading your Tcl/Tk version."),
                             checkmessage=_("Do not show this message again."))
    CONFIG.set("General", "old_tcl_warning", str(not ans))

    def open_image(file, master=None):
        return ImageTk.PhotoImage(Image.open(file), master=master)

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
