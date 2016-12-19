#! /usr/bin/python3
# -*-coding:Utf-8 -*-
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


Class for the cells in the grid
"""

from SudokuTkModules.constantes import STYLE
from tkinter.ttk import Frame, Style, Label

class Case(Frame):
    """ case de la grille de sudoku """
    def __init__(self, parent, i, j, **options):
        Frame.__init__(self, parent, **options)
        # grid layout
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        # styles
        self.style = Style(self)
        self.style.theme_use(STYLE)
        self.style.configure("case.TFrame", background="white")
        self.style.configure("case.TLabel", background="white", foreground="black")
        self.style.configure("case_init.TFrame", background="lightgrey")
        self.style.configure("case_init.TLabel", background="lightgrey", foreground="black")
        self.style.configure("erreur.TFrame", background="white")
        self.style.configure("erreur.TLabel", background="white", foreground="red")
        self.style.configure("solution.TFrame", background="white")
        self.style.configure("solution.TLabel", background="white", foreground="blue")
        self.configure(style="case.TFrame")

        self.i = i
        self.j = j
        self.modifiable = True
        self.val = 0 # valeur de la case, 0 = vide
        self.possibilites = [] # possibilites écrites dans la case

        # labels
        self.chiffres = [] # tableau 3x3 de labels permettant d'afficher les chiffres dans la case
        sticky_i = ["n", "ns", "s"]
        sticky_j = ["w", "ew", "e"]
        for i in range(3):
            self.chiffres.append([])
            for j in range(3):
                self.chiffres[i].append(Label(self, text=" ", anchor="center",
                                                  style="case.TLabel", width=1))
                self.chiffres[i][j].grid(row=i, column=j,
                                         sticky=sticky_i[i % 3] + sticky_j[j % 3],
                                         padx=1, pady=1)

    def get_val(self):
        return self.val

    def get_i(self):
        return self.i

    def get_j(self):
        return self.j

    def get_possibilites(self):
        return self.possibilites

    def is_modifiable(self):
        return self.modifiable

    def set_modifiable(self, b):
        self.modifiable = b
        if self.modifiable:
            self.configure(style="case.TFrame")
            for i in range(3):
                for j in range(3):
                    self.chiffres[i][j].configure(style="case.TLabel")
        else:
            self.configure(style="case_init.TFrame")
            for i in range(3):
                for j in range(3):
                    self.chiffres[i][j].configure(style="case_init.TLabel")

    def affiche_erreur(self):
        if self.modifiable:
            self.chiffres[0][0].configure(style="erreur.TLabel")

    def affiche_solution(self):
        if self.modifiable:
            self.chiffres[0][0].configure(style="solution.TLabel")

    def affiche_erreur_possibilite(self, val):
        if self.modifiable:
            i = (val - 1)//3
            j = (val - 1) % 3
            self.chiffres[i][j].configure(style="erreur.TLabel")

    def pas_erreur(self, i, j):
        if self.modifiable:
            self.chiffres[i][j].configure(style="case.TLabel")
        else:
            self.chiffres[i][j].configure(style="case_init.TLabel")

    def edit_chiffre(self, val):
        """ Ajoute / Enlève le chiffre val dans la case (valeur sûre) et enlève les possibilités.
            Renvoie nb=1,0,-1 où nb correspond au nombre de chiffres (relatif) ajoutés à la grille."""
        nb = 0
        if self.val != val:
            if not self.val:
                nb = 1
            self.efface_case()
            self.chiffres[0][0].configure(text=val, font="Arial 32")
            self.chiffres[0][0].grid_configure(rowspan=3, columnspan=3, sticky="nsew")
            self.chiffres[0][0].lift()
            self.val = val
        else:
            self.efface_case()
            nb = -1
        return nb

    def edit_possibilite(self, val):
        """ Ajoute / Enlève  la possibilité val dans la case """
        i = (val - 1)//3
        j = (val - 1) % 3
        nb = 0
        if self.val:
            self.efface_case()
            nb = -1
        if not val in self.possibilites:
            self.chiffres[i][j].configure(text=val, font="Arial 9")
            self.possibilites.append(val)
        else:
            self.chiffres[i][j].configure(text=" ")
            self.possibilites.remove(val)
        return nb


    def efface_case(self):
        """ Efface tous les labels de la case """
        for i in range(3):
            for j in range(3):
                self.chiffres[i][j].configure(text=" ", font="Arial 9")
                self.pas_erreur(i,j)
        self.chiffres[0][0].grid_configure(rowspan=1, columnspan=1, sticky="nw")
        self.val = 0
        self.possibilites = []
