#! /usr/bin/python3
# -*- coding:Utf-8 -*-
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


Class for the virtual keyboard to enter numbers in the grid
"""

from tkinter import Toplevel
from tkinter.ttk import Style, Button
from sudokutk.constantes import LOG
from numpy import array

class Clavier(Toplevel):
    """ Pavé numérique pour choisir un chiffre """
    def __init__(self, parent, case, val_ou_pos, **options):
        """ créer le Toplevel 'À propos de Bracelet Generator' """
        Toplevel.__init__(self, parent, **options)
        self.withdraw()
        self.type = val_ou_pos # clavier pour rentrer une valeur ou une possibilité
        self.overrideredirect(True)
        self.case = case
        self.transient(self.master)
        self.style = Style(self)
        self.style.configure("clavier.TButton", font="Arial 12")
        self.boutons = [[Button(self, text="1", width=2, style="clavier.TButton", command=lambda: self.entre_nb(1)),
                         Button(self, text="2", width=2, style="clavier.TButton", command=lambda: self.entre_nb(2)),
                         Button(self, text="3", width=2, style="clavier.TButton", command=lambda: self.entre_nb(3))],
                        [Button(self, text="4", width=2, style="clavier.TButton", command=lambda: self.entre_nb(4)),
                         Button(self, text="5", width=2, style="clavier.TButton", command=lambda: self.entre_nb(5)),
                         Button(self, text="6", width=2, style="clavier.TButton", command=lambda: self.entre_nb(6))],
                        [Button(self, text="7", width=2, style="clavier.TButton", command=lambda: self.entre_nb(7)),
                         Button(self, text="8", width=2, style="clavier.TButton", command=lambda: self.entre_nb(8)),
                         Button(self, text="9", width=2, style="clavier.TButton", command=lambda: self.entre_nb(9))]]
        for i in range(3):
            for j in range(3):
                self.boutons[i][j].grid(row=i, column=j)
        self.protocol("WM_DELETE_WINDOW", self.quitter)
        self.resizable(0, 0)
        self.attributes("-topmost",0)

    def focus_out(self, event):
        """ quitte si la fenêtre n'est plus au premier plan """
        try:
            if not self.focus_get():
                self.quitter()
        except KeyError:
            # erreur déclenchée par la présence d'une tkMessagebox
            self.quitter()

    def entre_nb(self, val):
        """ commande de la touche val du clavier """
        i, j = self.case.get_i(), self.case.get_j()

        # données pour le log
        val_prec = self.case.get_val()
        pos_prec = array(self.case.get_possibilites(), dtype=str)
        coords = "%i\t%i;" % (i, j)
        undo_ch = "%i\t%s;" % (val_prec,"".join(pos_prec))
        modifs = ";"

        # modification de la case
        if self.type == "val":
            self.master.modifie_nb_cases_remplies(self.case.edit_chiffre(val))
            if not self.master.test_case(i, j, val_prec):
                modifs = self.master.update_grille(i, j, val_prec)
            self.quitter()
        else:
            self.master.modifie_nb_cases_remplies(self.case.edit_possibilite(val))
            self.master.test_possibilite(i, j, val)

        # données pour le log
        pos = array(self.case.get_possibilites(), dtype=str)
        redo_ch = "%i\t%s\n" % (self.case.get_val(),"".join(pos))

        self.master.log()
        with open(LOG, "a") as log:
            log.write(coords + undo_ch + modifs + redo_ch)
        self.master.test_remplie()


    def quitter(self):
        """ ferme la fenêtre """
        if self.master:
            self.master.focus_set()
            self.master.set_clavier(None)
        self.destroy()

    def set_case(self, case):
        self.case = case

    def display(self, geometry):
        self.geometry(geometry)
        self.update_idletasks()
        self.deiconify()
        self.focus_set()
        self.lift()
        self.bind("<FocusOut>", self.focus_out)
