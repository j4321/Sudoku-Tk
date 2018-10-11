#! /usr/bin/python3
# -*-coding:Utf-8 -*-
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


Class to display the progress in filling the puzzle
"""

from tkinter.ttk import Frame, Label


class Progression(Frame):
    """Class to display the progress in filling the puzzle."""

    def __init__(self, master, number, **kwargs):
        kwargs.setdefault('width', 34)
        kwargs.setdefault('height', 34)
        kwargs.setdefault('style', 'case.TFrame')
        Frame.__init__(self, master, **kwargs)
        self.grid_propagate(False)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.number = number
        self._nb = 0

        self.label_number = Label(self, style='case.TLabel', text=str(number),
                                  font='Arial 16')
        self.label_nb = Label(self, style='case.TLabel', text='0', font='Arial 9')
        self.label_number.grid(row=0, column=0, sticky='e', padx=0)
        self.label_nb.grid(row=0, column=1, sticky='n')

    @property
    def nb(self):
        return self._nb

    @nb.setter
    def nb(self, value):
        self._nb = value
        self.label_nb.configure(text=str(self._nb))

        if self._nb < 9:
            self.configure(style='case.TFrame')
            self.label_number.configure(style='case.TLabel')
            self.label_nb.configure(style='case.TLabel')
        elif self._nb == 9:
            self.configure(style='case_init.TFrame')
            self.label_number.configure(style='case_init.TLabel')
            self.label_nb.configure(style='case_init.TLabel')
        else:
            self.configure(style='erreur.TFrame')
            self.label_number.configure(style='erreur.TLabel')
            self.label_nb.configure(style='erreur.TLabel')
