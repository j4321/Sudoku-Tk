#! /usr/bin/python3
# -*- coding:Utf-8 -*-
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


Custom tkinter messageboxes
"""

from tkinter import Toplevel, BooleanVar
from tkinter.ttk import Label, Button, Checkbutton

class OneButtonBox(Toplevel):
    """ Messagebox with only one button """

    def __init__(self, parent=None, title="", message="", button="Ok", image=None, **options):
        """
            Create a message box with one button:
                parent: parent of the toplevel window
                title: message box title
                message: message box text
                button: message displayed on the button
                image: image displayed at the left of the message
                **options: other options to pass to the Toplevel.__init__ method
        """
        Toplevel.__init__(self, parent, **options)
        self.transient(parent)
        self.title(title)
        if image:
            Label(self, text=message, wraplength=335,
                  font="Sans 11", compound="left", image=image).grid(row=0, padx=10, pady=10)
        else:
            Label(self, text=message, wraplength=335,
                  font="Sans 11").grid(row=0, padx=10,pady=10)
        b = Button(self, text=button, command=self.destroy)
        b.grid(row=1, padx=10,pady=10)
        self.grab_set()
        b.focus_set()
        self.wait_window(self)

class OBCheckbutton(Toplevel):
    """ Messagebox with only one button and a checkbox below the button
        for instance to add a 'Do not show this again' option """

    def __init__(self, parent=None, title="", message="", button="Ok", image=None,
                 checkmessage="", **options):
        """
            Create a messagebox with one button and a checkbox below the button:
                parent: parent of the toplevel window
                title: message box title
                message: message box text
                button: message displayed on the button
                image: image displayed at the left of the message
                checkmessage: message displayed next to the checkbox
                **options: other options to pass to the Toplevel.__init__ method
        """
        Toplevel.__init__(self, parent, **options)
        self.transient(parent)
        self.title(title)
        if image:
            Label(self, text=message, wraplength=335,
                  font="Sans 11", compound="left", image=image).grid(row=0, padx=10, pady=10)
        else:
            Label(self, text=message, wraplength=335,
                  font="Sans 11").grid(row=0, padx=10,pady=10)
        b = Button(self, text=button, command=self.destroy)
        b.grid(row=1, padx=10,pady=10)
        self.var = BooleanVar(self)
        c = Checkbutton(self, text=checkmessage, variable=self.var)
        c.grid(row=2, padx=10, pady=10)
        self.grab_set()
        b.focus_set()
        self.wait_window(self)

    def get_check(self):
        return self.var.get()

class TwoButtonBox(Toplevel):
    """ Messagebox with two buttons """

    def __init__(self, parent=None, title="", message="", button1="Yes", button2="No",
                 image=None, **options):
        """
            Create a messagebox with two buttons:
                parent: parent of the toplevel window
                title: message box title
                message: message box text
                button1/2: message displayed on the first/second button
                image: image displayed at the left of the message
                **options: other options to pass to the Toplevel.__init__ method
        """

        Toplevel.__init__(self, parent, **options)
        self.transient(parent)
        self.title(title)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rep = ""
        self.button1 = button1
        self.button2 = button2
        if image:
            Label(self, text=message, wraplength=335,
                  font="Sans 11", compound="left", image=image).grid(row=0,
                                                                   padx=10,
                                                                   pady=10,
                                                                   columnspan=2)
        else:
            Label(self, text=message, wraplength=335,
                  font="Sans 11").grid(row=0, padx=10,pady=10, columnspan=2)
        b1 = Button(self, text=button1, command=self.command1)
        b1.grid(row=1, column=0, padx=15, pady=10, sticky="e")
        Button(self, text=button2, command=self.command2).grid(row=1, column=1,
                                                              padx=15, pady=10,
                                                              sticky="w")
        self.grab_set()
        b1.focus_set()
        self.wait_window(self)

    def command1(self):
        self.rep = self.button1
        self.destroy()

    def command2(self):
        self.rep = self.button2
        self.destroy()

    def get_rep(self):
        return self.rep

def one_button_box(parent=None, title="", message="", button="Ok", image=None,
                   **options):
    """ Open a OneButtonBox and return "ok" when closed. """
    OneButtonBox(parent, title, message, button, image, **options)
    return "ok"

def ob_checkbutton(parent=None, title="", message="", button="Ok", image=None,
                   checkmessage="", **options):
    """ Open a OBCheckbutton and return the value of the checkbutton when closed. """
    ob = OBCheckbutton(parent, title, message, button, image, checkmessage, **options)
    return ob.get_check()

def two_button_box(parent=None, title="", message="", button1="Yes", button2="No",
                   image=None, **options):
    """ Open a TwoButtonBox and return the text of the button chosen by the user"""
    tbb = TwoButtonBox(parent, title, message, button1, button2, image, **options)
    return tbb.get_rep()
