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


Class for the GUI
"""
#TODO: set numbers back to black when conflicted number is erased
#TODO: use list instead of file for log

import sudokutk.constantes as cst
from sudokutk.constantes import open_image, CONFIG, LOG,  askopenfilename, asksaveasfilename
from sudokutk.clavier import Clavier
from sudokutk.about import About
from sudokutk.aide import Aide
from sudokutk.grille import Grille, genere_grille, difficulte_grille
from sudokutk.case import Case
from sudokutk.progression import Progression
from sudokutk.tooltip import TooltipWrapper
from tkinter import Tk, Menu, StringVar, Toplevel
from tkinter.ttk import Button, Style, Label, Frame
from sudokutk.custom_messagebox import one_button_box, two_button_box
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from pickle import Pickler, Unpickler, UnpicklingError
from os.path import exists, join
from os import remove


class Sudoku(Tk):
    def __init__(self, file=None):
        Tk.__init__(self, className="Sudoku-Tk")
        self.title("Sudoku-Tk")
        self.resizable(0,0)
        self.protocol("WM_DELETE_WINDOW", self.quitter)
        cst.set_icon(self)
        self.columnconfigure(3, weight=1)

        # --- style
        bg = '#dddddd'
        activebg = '#efefef'
        pressedbg = '#c1c1c1'
        lightcolor = '#ededed'
        darkcolor = '#cfcdc8'
        bordercolor = '#888888'
        focusbordercolor = '#5E5E5E'
        disabledfg = '#999999'
        disabledbg = bg

        button_style_config = {'bordercolor': bordercolor,
                               'background': bg,
                               'lightcolor': lightcolor,
                               'darkcolor': darkcolor}

        button_style_map = {'background': [('active', activebg),
                                           ('disabled', disabledbg),
                                           ('pressed', pressedbg)],
                            'lightcolor': [('pressed', darkcolor)],
                            'darkcolor': [('pressed', lightcolor)],
                            'bordercolor': [('focus', focusbordercolor)],
                            'foreground': [('disabled', disabledfg)]}

        style = Style(self)
        style.theme_use(cst.STYLE)
        style.configure('TFrame', background=bg)
        style.configure('TLabel', background=bg)
        style.configure('TScrollbar', gripcount=0, troughcolor=pressedbg,
                             **button_style_config)
        style.map('TScrollbar', **button_style_map)
        style.configure('TButton', **button_style_config)
        style.map('TButton', **button_style_map)
        style.configure('TCheckutton', **button_style_config)
        style.map('TCheckutton', **button_style_map)
        self.option_add('*Toplevel.background', bg)
        self.option_add('*Menu.background', bg)
        self.option_add('*Menu.activeBackground', activebg)
        self.configure(bg=bg)

        style.configure("bg.TFrame", background="grey")
        style.configure("case.TFrame", background="white")
        style.configure("case.TLabel", background="white", foreground="black")
        style.configure("case_init.TFrame", background="lightgrey")
        style.configure("case_init.TLabel", background="lightgrey", foreground="black")
        style.configure("erreur.TFrame", background="white")
        style.configure("erreur.TLabel", background="white", foreground="red")
        style.configure("solution.TFrame", background="white")
        style.configure("solution.TLabel", background="white", foreground="blue")
        style.configure("pause.TLabel", foreground="grey", background='white')

        # --- images
        self.im_erreur = open_image(cst.ERREUR)
        self.im_pause = open_image(cst.PAUSE)
        self.im_restart = open_image(cst.RESTART)
        self.im_play = open_image(cst.PLAY)
        self.im_info = open_image(cst.INFO)
        self.im_undo = open_image(cst.UNDO)
        self.im_redo = open_image(cst.REDO)
        self.im_question = open_image(cst.QUESTION)

        # --- timer
        self.chrono = [0,0]
        self.tps = Label(self, text="%02i:%02i"% tuple(self.chrono),
                         font="Arial 16")
        self.debut = False # la partie a-t-elle commencée ?
        self.chrono_on = False # le chrono est-il en marche ?

        # --- buttons
        self.b_pause = Button(self, state="disabled", image=self.im_pause,
                                  command=self.play_pause)
        self.b_restart = Button(self, state="disabled", image=self.im_restart,
                                command=self.recommence)
        self.b_undo = Button(self, image=self.im_undo, command=self.undo)
        self.b_redo = Button(self, image=self.im_redo, command=self.redo)

        # --- tooltips
        self.tooltip_wrapper = TooltipWrapper(self)
        self.tooltip_wrapper.add_tooltip(self.b_pause, _("Pause game"))
        self.tooltip_wrapper.add_tooltip(self.b_restart, _("Restart game"))
        self.tooltip_wrapper.add_tooltip(self.b_undo, _("Undo"))
        self.tooltip_wrapper.add_tooltip(self.b_redo, _("Redo"))

        # --- numbers
        frame_nb = Frame(self, style='bg.TFrame', width=36)
        self.progression = []
        for i in range(1, 10):
            self.progression.append(Progression(frame_nb, i))
            self.progression[-1].pack(padx=1, pady=1)

        # --- level indication
        frame = Frame(self)
        frame.grid(row=0, columnspan=5, padx=(30, 10), pady=10)
        Label(frame, text=_("Level") + ' - ', font="Arial 16").pack(side='left')
        self.label_level = Label(frame, font="Arial 16", text=_("Unknown"))
        self.label_level.pack(side='left')
        self.level = "unknown" # puzzle level

        # --- frame contenant la grille de sudoku
        self.frame_puzzle = Frame(self, style="bg.TFrame")
        self.frame_pause = Frame(self, style="case.TFrame")
        self.frame_pause.grid_propagate(False)
        self.frame_pause.columnconfigure(0, weight=1)
        self.frame_pause.rowconfigure(0, weight=1)
        Label(self.frame_pause, text='PAUSE', style='pause.TLabel',
              font='Arial 30 bold').grid()

        # --- placement
        frame_nb.grid(row=1, column=6, sticky='en', pady=0, padx=(0, 30))
        self.frame_puzzle.grid(row=1, columnspan=5, padx=(30, 15))
        self.tps.grid(row=2, column=0, sticky="e", padx=(30, 10), pady=30)
        self.b_pause.grid(row=2, column=1, sticky="w", padx=2, pady=30)
        self.b_restart.grid(row=2, column=2, sticky="w", padx=2, pady=30)
        self.b_undo.grid(row=2, column=3, sticky="e", pady=30, padx=2)
        self.b_redo.grid(row=2, column=4, sticky="w", pady=30, padx=(2, 10))

        # --- menu
        menu = Menu(self, tearoff=0)

        menu_nouveau = Menu(menu, tearoff=0)

        menu_levels = Menu(menu_nouveau, tearoff=0)
        menu_levels.add_command(label=_("Easy"), command=self.new_easy)
        menu_levels.add_command(label=_("Medium"), command=self.new_medium)
        menu_levels.add_command(label=_("Difficult"), command=self.new_difficult)

        menu_nouveau.add_cascade(label=_("Level"), menu=menu_levels)
        menu_nouveau.add_command(label=_("Generate a puzzle"),
                                 command=self.genere_grille,
                                 accelerator="Ctrl+G")
        menu_nouveau.add_command(label=_("Empty grid"),
                                 command=self.grille_vide,
                                 accelerator="Ctrl+N")

        menu_ouvrir = Menu(menu, tearoff=0)
        menu_ouvrir.add_command(label=_("Game"), command=self.import_partie,
                                accelerator="Ctrl+O")
        menu_ouvrir.add_command(label=_("Puzzle"), command=self.import_grille,
                                accelerator="Ctrl+Shift+O")

        menu_game = Menu(menu, tearoff=0)
        menu_game.add_command(label=_("Restart"), command=self.recommence)
        menu_game.add_command(label=_("Solve"), command=self.resolution)
        menu_game.add_command(label=_("Save"), command=self.sauvegarde,
                              accelerator="Ctrl+S")
        menu_game.add_command(label=_("Export"), command=self.export_impression,
                              accelerator="Ctrl+E")
        menu_game.add_command(label=_("Evaluate level"),
                              command=self.evaluate_level)

        menu_language = Menu(menu, tearoff=0)
        self.langue = StringVar(self)
        self.langue.set(cst.LANGUE[:2])
        menu_language.add_radiobutton(label="Français",
                                      variable=self.langue,
                                      value="fr", command=self.translate)
        menu_language.add_radiobutton(label="English", variable=self.langue,
                                      value="en", command=self.translate)


        menu_help = Menu(menu, tearoff=0)
        menu_help.add_command(label=_("Help"), command=self.aide, accelerator='F1')
        menu_help.add_command(label=_("About"), command=self.about)

        menu.add_cascade(label=_("New"), menu=menu_nouveau)
        menu.add_cascade(label=_("Open"), menu=menu_ouvrir)
        menu.add_cascade(label=_("Game"), menu=menu_game)
        menu.add_cascade(label=_("Language"), menu=menu_language)
        menu.add_command(label=_("Statistics"), command=self.show_stat)
        menu.add_cascade(label=_("Help"), menu=menu_help)

        self.configure(menu=menu)

        # --- clavier popup
        self.clavier = None

        # --- cases
        self.nb_cases_remplies = 0
        self.blocs = np.zeros((9, 9), dtype=object)
        for i in range(9):
            for j in range(9):
                self.blocs[i, j] = Case(self.frame_puzzle, i, j, self.update_nbs, width=50, height=50)
                px, py = 1, 1
                if i % 3 == 2 and i != 8:
                    py = (1,3)
                if j % 3 == 2 and j != 8:
                    px =(1,3)
                self.blocs[i, j].grid(row=i, column=j, padx=px, pady=py)
                self.blocs[i, j].grid_propagate(0)

        # --- création du fichier log
        self.log_reinit()

        # --- raccourcis clavier et actions de la souris
        self.bind("<Button>", self.edit_case)
        self.bind("<Control-z>", lambda e: self.undo())
        self.bind("<Control-y>", lambda e: self.redo())
        self.bind("<Control-s>", lambda e: self.sauvegarde())
        self.bind("<Control-e>", lambda e: self.export_impression())
        self.bind("<Control-o>", lambda e: self.import_partie())
        self.bind("<Control-Shift-O>", lambda e: self.import_grille())
        self.bind("<Control-n>", lambda e: self.grille_vide())
        self.bind("<Control-g>", lambda e: self.genere_grille())
        self.bind("<FocusOut>", self.focus_out)
        self.bind("<F1>", self.aide)

        # --- open game
        if file:
            try:
                self.load_sudoku(file)
            except FileNotFoundError:
                one_button_box(self, _("Error"),
                               _("The file %(file)r does not exist.") % file,
                               image=self.im_erreur)
            except (KeyError, EOFError, UnpicklingError):
                try:
                    self.load_grille(file)
                except Exception:
                    one_button_box(self, _("Error"),
                                   _("This file is not a valid sudoku file."),
                                   image=self.im_erreur)
        elif exists(cst.PATH_SAVE):
            self.load_sudoku(cst.PATH_SAVE)
            remove(cst.PATH_SAVE)

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level
        self.label_level.configure(text=_(level.capitalize()))

    def update_nbs(self, nb, delta):
        self.progression[nb - 1].nb += delta

    def reset_nbs(self):
        for p in self.progression:
            p.nb = 0

    def evaluate_level(self):
        grille = Grille()
        for i in range(9):
            for j in range(9):
                val = self.blocs[i, j].get_val()
                if val:
                    grille.ajoute_init(i, j, val)
        self.level = difficulte_grille(grille)

    def show_stat(self):
        """ show best times """
        def reset():
            """ reset best times """
            for level in ["easy", "medium", "difficult"]:
                CONFIG.set("Statistics", level, "")
            top.destroy()

        if self.chrono_on:
            self.play_pause()
        top = Toplevel(self)
        top.transient(self)
        top.columnconfigure(1, weight=1)
        top.resizable(0,0)

        top.title(_("Statistics"))
        top.grab_set()

        Label(top, text=_("Best times"), font="Sans 12 bold").grid(row=0, columnspan=2,
                                              padx=30, pady=10)

        for i,level in enumerate(["easy", "medium", "difficult"]):
            Label(top, text=_(level.capitalize()),
                  font="Sans 10 bold").grid(row=i+1, column=0, padx=(20,4),
                                       pady=4, sticky="e")
            tps = CONFIG.get("Statistics", level)
            if tps:
                tps = int(tps)
                m = tps//60
                s = tps % 60
                Label(top, text="%i min %i s" % (m, s),
                      font="Sans 10").grid(row=i + 1, column=1,
                                           sticky="w", pady=4,
                                           padx=(4,20))
        Button(top, text=_("Close"), command=top.destroy).grid(row=4, column=0, padx=(10,4), pady=10)
        Button(top, text=_("Clear"), command=reset).grid(row=4, column=1, padx=(4, 10), pady=10)

    def new_easy(self):
        nb = np.random.randint(1, 101)
        fichier = join(cst.PUZZLES_LOCATION, "easy", "puzzle_easy_%i.txt" % nb)
        self.import_grille(fichier)
        self.level = "easy"

    def new_medium(self):
        nb = np.random.randint(1, 101)
        fichier = join(cst.PUZZLES_LOCATION, "medium", "puzzle_medium_%i.txt" % nb)
        self.import_grille(fichier)
        self.level = "medium"

    def new_difficult(self):
        nb = np.random.randint(1, 101)
        fichier = join(cst.PUZZLES_LOCATION, "difficult", "puzzle_difficult_%i.txt" % nb)
        self.import_grille(fichier)
        self.level = "difficult"

    def translate(self):
        """ changement de la langue de l'interface """
        one_button_box(self, _("Information"),
                       _("The language setting will take effect after restarting the application"),
                       image=self.im_info)
        CONFIG.set("General", "language", self.langue.get())

    def focus_out(self, event):
        """ met en pause si la fenêtre n'est plus au premier plan """
        try:
            if not self.focus_get() and self.chrono_on:
                self.play_pause()
        except KeyError:
            # erreur déclenchée par la présence d'une tkMessagebox
            if self.chrono_on:
                self.play_pause()

    def log_reinit(self):
        """ réinitialise le fichier log (ie efface l'historique des actions) """
        with open(LOG, "w") as log:
            log.write("# Sudoku logfile\n\n")
        self.log_ligne = 1  # ligne actuelle dans le fichier log (pour undo)
        self.log_nb_ligne = 2  # nombre de lignes du fichier log
        self.b_undo.configure(state="disabled")
        self.b_redo.configure(state="disabled")

    def log(self):
        """ annule la possibilté de faire redo une fois qu'on a remodifié la grille. """
        self.log_nb_ligne += 1
        self.log_ligne += 1
        self.b_undo.configure(state="normal")
        if self.log_ligne != self.log_nb_ligne - 1:
            self.b_redo.configure(state="disabled")
            with open(LOG, "r") as log:
                logfile = log.readlines()
            with open(LOG, "w") as log:
                # supprime les actions annulées précédemment
                for ligne in logfile[:self.log_ligne]:
                    log.write(ligne)
            self.log_nb_ligne = self.log_ligne + 1

    def about(self):
        if self.chrono_on:
            self.play_pause()
        About(self)

    def aide(self, event=None):
        if self.chrono_on:
            self.play_pause()
        Aide(self)

    def quitter(self):
        rep = _("Yes")
        if self.debut:
            rep = two_button_box(self, _("Confirmation"),
                                 _("Do you want to interrupt the current puzzle?"),
                                 _("Yes"), _("No"), image=self.im_question)
        if rep == _("Yes"):
            if self.debut:
                self.save(cst.PATH_SAVE)
            self.destroy()

    def undo(self):
        if self.log_ligne > 1 and self.chrono_on:
            self.b_redo.configure(state="normal")
            with open(LOG, "r") as log:
                logfile = log.readlines()
            coords, undo_ch, modifs, redo_ch = logfile[self.log_ligne].split(";")
            i, j = coords.split("\t")
            val_prec, pos_prec = undo_ch.split("\t")
            val = int(redo_ch.split("\t")[0])
            i, j, val_prec = int(i), int(j), int(val_prec)
            modifs = modifs.split("\t")
            # actualisation de la ligne courante du fichier log
            self.log_ligne -= 1
            if self.log_ligne == 1:
                self.b_undo.configure(state="disabled")

            if self.blocs[i, j].get_val():
                self.modifie_nb_cases_remplies(-1)
                self.update_nbs(self.blocs[i, j].get_val(), -1)
            self.blocs[i, j].efface_case()
            if val_prec:
                self.modifie_nb_cases_remplies(self.blocs[i, j].edit_chiffre(val_prec))
                if not self.test_case(i, j, val):
                    self.update_grille(i, j, val)
            else:
                for nb in pos_prec:
                    v = int(nb)
                    self.modifie_nb_cases_remplies(self.blocs[i, j].edit_possibilite(v))
                    self.test_possibilite(i, j, v)
            if modifs[0]:
                for ch in modifs:
                    k, l = ch.split(",")
                    k, l = int(k), int(l)
                    self.blocs[k, l].edit_possibilite(val)

    def redo(self):
        if self.log_ligne < self.log_nb_ligne - 1 and self.chrono_on:
            self.b_undo.configure(state="normal")
            with open(LOG, "r") as log:
                logfile = log.readlines()
            self.log_ligne += 1
            if self.log_ligne == self.log_nb_ligne - 1:
                self.b_redo.configure(state="disabled")
            with open(LOG, "r") as log:
                logfile = log.readlines()
            coords, undo_ch, modifs, redo_ch = logfile[self.log_ligne].split(";")
            redo_ch = redo_ch[:-1]
            i, j = coords.split("\t")
            val, pos = redo_ch.split("\t")
            i, j, val = int(i), int(j), int(val)
            val_prec = self.blocs[i, j].get_val()
            if val_prec:
                self.modifie_nb_cases_remplies(-1)
                self.update_nbs(val_prec, -1)
            self.blocs[i, j].efface_case()
            if val:
                self.modifie_nb_cases_remplies(self.blocs[i, j].edit_chiffre(val))
                if not self.test_case(i, j, val_prec):
                    self.update_grille(i, j, val_prec)
            else:
                for nb in pos:
                    v = int(nb)
                    self.modifie_nb_cases_remplies(self.blocs[i, j].edit_possibilite(v))
                    self.test_possibilite(i, j, v)


    def restart(self, m=0, s=0):
        """ réinitialise le chrono et les boutons """
        self.chrono = [m, s]
        self.chrono_on = False
        self.debut = False
        self.tps.configure(text="%02i:%02i"% tuple(self.chrono))
        self.b_undo.configure(state="disabled")
        self.b_pause.configure(state="disabled", image=self.im_pause)
        self.b_redo.configure(state="disabled")
        self.b_restart.configure(state="disabled")
        self.log_reinit()
        self.frame_pause.place_forget()

    def play_pause(self):
        """ Démarre le chrono s'il était arrêté, le met en pause sinon """
        if self.debut:
            if self.chrono_on:
                self.chrono_on = False
                self.b_pause.configure(image=self.im_play)
                self.b_redo.configure(state="disabled")
                self.b_undo.configure(state="disabled")
                self.tooltip_wrapper.set_tooltip_text(self.b_pause, _("Resume game"))
                self.frame_pause.place(in_=self.frame_puzzle, x=0, y=0, anchor='nw',
                                       relwidth=1, relheight=1)
            elif self.nb_cases_remplies != 81:
                self.chrono_on = True
                self.b_pause.configure(image=self.im_pause)
                self.tps.after(1000, self.affiche_chrono)
                if self.log_ligne > 1:
                    self.b_undo.configure(state="normal")
                if self.log_ligne < self.log_nb_ligne - 1:
                    self.b_redo.configure(state="normal")
                self.tooltip_wrapper.set_tooltip_text(self.b_pause, _("Pause game"))
                self.frame_pause.place_forget()

    def affiche_chrono(self):
        """ Met à jour l'affichage du temps """
        if self.chrono_on:
            self.chrono[1] += 1
            if self.chrono[1] == 60:
                self.chrono[0] += 1
                self.chrono[1] = 0
            self.tps.configure(text="%02i:%02i"% tuple(self.chrono))
            self.tps.after(1000, self.affiche_chrono)

    def modifie_nb_cases_remplies(self, nb):
        self.nb_cases_remplies += nb

    def edit_case(self, event):
        if event.num in [1,3]:
            if not self.debut and self.nb_cases_remplies != 81:
                self.debut = True
                self.b_pause.configure(state="normal")
                self.b_restart.configure(state="normal")
                self.play_pause()
            if str(event.widget) != "." and self.chrono_on:
                if self.clavier:
                    self.clavier.quitter()
                ref = self.blocs[0, 0].winfo_parent()
                case = event.widget.grid_info().get("in", None)
                if str(case) == ref:
                    case = event.widget
                try:
                    if case.is_modifiable():
                        if event.num == 1:
                            self.clavier = Clavier(self, case, "val")
                        elif event.num == 3:
                            self.clavier = Clavier(self, case, "possibilite")
                        self.clavier.display("+%i+%i" % (case.winfo_rootx()-25,case.winfo_rooty()+50))
                except AttributeError:
                    if self.clavier:
                        self.clavier.quitter()

            elif self.clavier:
                self.clavier.quitter()

    def test_case(self, i, j, val_prec=0):
        """ Teste si la valeur de la case est en contradiction avec celles des
            autres cases de la ligne / colonne / bloc et renvoie True s'il y a une erreur."""
        val = self.blocs[i, j].get_val()
        a, b = i // 3, j // 3
        error = False
        if val:
            if ((self.blocs[i, :] == val).sum() > 1 or (self.blocs[:, j] == val).sum() > 1 or
                (self.blocs[3 * a: 3 * (a + 1), 3 * b: 3 * (b + 1)] == val).sum() > 1):
                # erreur !
                self.blocs[i, j].affiche_erreur()
                error = True
        if val_prec:
            # a number was removed, remove obsolete errors
            line = self.blocs[i, :] == val_prec
            column = self.blocs[:, j] == val_prec
            bloc = self.blocs[3 * a: 3 * (a + 1), 3 * b: 3 * (b + 1)] == val_prec
            if line.sum() == 1:
                self.blocs[i, line.argmax()].no_error()
                self.test_case(i, line.argmax())
            if column.sum() == 1:
                self.blocs[column.argmax(), j].no_error()
                self.test_case(column.argmax(), j)
            if bloc.sum() == 1:
                x, y = divmod(bloc.argmax(), 3)
                self.blocs[3 * a + x, 3 * b + y].no_error()
                self.test_case(3 * a + x, 3 * b + y)
        return error

    def test_possibilite(self, i, j, val):
        """ Teste si la possibilité val de la case est en contradiction avec les valeurs des
            autres cases de la ligne / colonne / bloc """
        a, b = i // 3, j // 3
        if ((self.blocs[i, :] == val).sum() > 0 or (self.blocs[:, j] == val).sum() > 0 or
            (self.blocs[3 * a: 3 * (a + 1), 3 * b: 3 * (b + 1)] == val).sum() > 0):
            # erreur !
            self.blocs[i, j].affiche_erreur_possibilite(val)

    def test_remplie(self):
        """ Test si la grille est remplie """
        if self.nb_cases_remplies == 81:
            grille = Grille()
            for i in range(9):
                for j in range(9):
                    val = self.blocs[i, j].get_val()
                    if val:
                        grille.ajoute_init(i, j, val)
            sol = grille.solve()
            if type(sol) == np.ndarray:
                self.play_pause()
                self.frame_pause.place_forget()
                one_button_box(self, _("Information"),
                               _("You solved the puzzle in %(min)i minutes and %(sec)i secondes.") % {"min": self.chrono[0], "sec": self.chrono[1]},
                               image=self.im_info)
                if self.level != "unknown":
                    best = CONFIG.get("Statistics", self.level)
                    current = self.chrono[0]*60 + self.chrono[1]
                    if best:
                        best = int(best)
                        if current < best:
                            CONFIG.set("Statistics", self.level, str(current))
                    else:
                        CONFIG.set("Statistics", self.level, str(current))
                self.b_pause.configure(state="disabled")
                self.debut = False

            else:
                i,j = sol[1]
                if self.blocs[i, j].get_val():
                    self.blocs[i, j].affiche_erreur()
                one_button_box(self, _("Information"), _("There is a mistake."),
                               image=self.im_info)

    def update_grille(self, i, j, val_prec=0):
        """ Enlève les possibilités devenues impossibles suite à l'ajout d'une
            valeur dans la case (i,j) """
        val = self.blocs[i, j].get_val()
        modif = []
        a, b = i // 3, j // 3
        if val_prec:
            x, y = divmod(val_prec - 1, 3)
            print(val_prec, x, y)
        for k, (line, column, bloc) in enumerate(zip(self.blocs[i, :], self.blocs[:, j], self.blocs[3 * a: 3 * (a + 1), 3 * b: 3 * (b + 1)].flatten())):
            # works because if line is bloc then pos1 is pos3 and both are edited at once
            pos1 = line.get_possibilites()
            pos2 = column.get_possibilites()
            pos3 = bloc.get_possibilites()
            if val in pos1:
                self.blocs[i, k].edit_possibilite(val)
                modif.append((i, k))
            if val in pos2:
                self.blocs[k, j].edit_possibilite(val)
                modif.append((k, j))
            if val in pos3:
                m, n = divmod(k, 3)
                self.blocs[3 * a + m, 3 * b + n].edit_possibilite(val)
                modif.append((3 * a + m, 3 * b + n))
            if val_prec:
                if val_prec in pos1:
                    self.blocs[i, k].pas_erreur(x, y)
                    self.test_possibilite(i, k, val_prec)
                if val_prec in pos2:
                    self.blocs[k, j].pas_erreur(x, y)
                    self.test_possibilite(k, j, val_prec)
                if val_prec in pos3:
                    m, n = divmod(k, 3)
                    m, n = 3 * a + m, 3 * b + n
                    if m != i and n != j:
                        self.blocs[m, n].pas_erreur(x, y)
                        self.test_possibilite(m, n, val_prec)
        modif_ch = ""
        for (k, l) in modif:
            modif_ch += "%i,%i\t" % (k, l)
        return modif_ch[:-1] + ";"

    def set_clavier(self, c):
        self.clavier = c

    def grille_vide(self):
        rep = _("Yes")
        if self.debut:
            rep = two_button_box(self, _("Confirmation"),
                                    _("Do you want to abandon the current puzzle?"),
                                    _("Yes"), _("No"), self.im_question)
        if rep == _("Yes"):
            self.nb_cases_remplies = 0
            self.restart()
            self.level = "unknown"
            self.reset_nbs()
            for i in range(9):
                for j in range(9):
                    self.blocs[i, j].set_modifiable(True)
                    self.blocs[i, j].efface_case()


    def genere_grille(self):
        """ Génère une nouvelle grille """
        if self.chrono_on:
            self.play_pause()
        rep = _("Yes")
        if self.debut:
            rep = two_button_box(self, _("Confirmation"),
                                 _("Do you want to abandon the current puzzle?"),
                                 _("Yes"), _("No"), self.im_question)

        if rep == _("Yes"):
            self.configure(cursor="watch")
            self.update()
            rep2 = _("Retry")
            while rep2 == _("Retry"):
                grille = genere_grille()
                diff = difficulte_grille(grille)
                nb = grille.nb_cases_remplies()
                self.configure(cursor="")
                rep2 = two_button_box(self, _("Information"),
                                     _("The generated puzzle contains %(nb)i numbers and its level is %(difficulty)s.") % ({"nb": nb, "difficulty": _(diff.capitalize())}),
                                     _("Retry"), _("Play"), image=self.im_info)
            if rep2 == _("Play"):
                self.level = diff
                self.affiche_grille(grille.get_sudoku())

    def recommence(self):
        if self.chrono_on:
            self.play_pause()
        rep = _("Yes")
        if self.debut:
            rep = two_button_box(self, _("Confirmation"),
                                    _("Do you really want to start again?"),
                                    _("Yes"), _("No"), self.im_question)
        if rep == _("Yes"):
            self.reset_nbs()
            for i in range(9):
                for j in range(9):
                    if self.blocs[i, j].is_modifiable():
                        if self.blocs[i, j].get_val():
                            self.nb_cases_remplies -= 1
                        self.blocs[i, j].efface_case()
                    else:
                        self.update_nbs(self.blocs[i, j].get_val(), 1)
            self.restart()
        elif self.debut:
            self.play_pause()


    def save(self, path):
        grille = np.zeros((9,9), dtype=int)
        modif = np.zeros((9,9), dtype=bool)
        possibilites = []
        for i in range(9):
            possibilites.append([])
            for j in range(9):
                grille[i,j] = self.blocs[i, j].get_val()
                modif[i,j] = self.blocs[i, j].is_modifiable()
                possibilites[i].append(self.blocs[i, j].get_possibilites())
        with open(path, "wb") as fich:
            p = Pickler(fich)
            p.dump(grille)
            p.dump(modif)
            p.dump(possibilites)
            p.dump(self.chrono)
            p.dump(self.level)

    def sauvegarde(self):
        if self.chrono_on:
            self.play_pause()
        fichier = asksaveasfilename(initialdir=cst.INITIALDIR,
                                    defaultextension='.sudoku',
                                    filetypes=[('Sudoku', '*.sudoku')])
        if fichier:
            self.save(fichier)

    def affiche_grille(self, grille):
        """ Affiche la grille """
        self.nb_cases_remplies = 0
        self.restart()
        for i in range(9):
            for j in range(9):
                nb = grille[i,j]
                self.blocs[i, j].efface_case()
                if nb:
                    self.blocs[i, j].set_modifiable(False)
                    self.nb_cases_remplies += 1
                    self.blocs[i, j].edit_chiffre(nb)
                else:
                   self.blocs[i, j].set_modifiable(True)

    def load_sudoku(self, file):
        with open(file,"rb") as fich:
            dp = Unpickler(fich)
            grille = dp.load()
            modif = dp.load()
            possibilites = dp.load()
            chrono = dp.load()
            self.level = dp.load()
        self.nb_cases_remplies = 0
        self.restart(*chrono)
        for i in range(9):
            for j in range(9):
                self.blocs[i, j].efface_case()
                if grille[i,j]:
                    self.nb_cases_remplies += 1
                    self.blocs[i, j].edit_chiffre(grille[i,j])
                else:
                    for pos in possibilites[i][j]:
                        self.blocs[i, j].edit_possibilite(pos)
                self.blocs[i, j].set_modifiable(modif[i,j])

    def import_partie(self):
        """ importe une partie stockée dans un fichier .sudoku """
        if self.chrono_on:
            self.play_pause()
        rep = _("Yes")
        if self.debut:
            rep = two_button_box(self, _("Confirmation"),
                                 _("Do you want to abandon the current puzzle?"),
                                 _("Yes"), _("No"), self.im_question)
        if rep == _("Yes"):
            fichier = askopenfilename(initialdir=cst.INITIALDIR,
                                        defaultextension='.sudoku',
                                        filetypes=[('Sudoku', '*.sudoku')])
            if fichier:
                try:
                    self.load_sudoku(fichier)
                except FileNotFoundError:
                    one_button_box(self, _("Error"),
                                   _("The file %(file)r does not exist.") % fichier,
                                   image=self.im_erreur)
                except (KeyError, EOFError, UnpicklingError):
                    one_button_box(self, _("Error"),
                                   _("This file is not a valid sudoku file."),
                                   image=self.im_erreur)
        elif self.debut:
            self.play_pause()

    def resolution_init(self):
        """ Résolution de la grille initiale (sans tenir compte des valeurs rentrées par l'utilisateur. """
        grille = Grille()
        for i in range(9):
            for j in range(9):
                if not self.blocs[i, j].is_modifiable():
                    val = self.blocs[i, j].get_val()
                    grille.ajoute_init(i, j, val)
        self.configure(cursor="watch")
        self.update()
        sol = grille.solve()
        self.configure(cursor="")
        if type(sol) == np.ndarray:
            for i in range(9):
                for j in range(9):
                    val = self.blocs[i, j].get_val()
                    if not val:
                        self.blocs[i, j].edit_chiffre(sol[i,j])
                        self.blocs[i, j].affiche_solution()
                    elif self.blocs[i, j].is_modifiable():
                        if val != sol[i,j]:
                            self.blocs[i, j].edit_chiffre(sol[i,j])
                            self.blocs[i, j].affiche_erreur()
            self.restart()
            self.nb_cases_remplies = 81

        elif sol[1]:
            i,j = sol[1]
            if self.blocs[i, j].get_val():
                self.blocs[i, j].affiche_erreur()
            one_button_box(self, _("Error"), _("The grid is wrong. It cannot be solved."),
                           image=self.im_erreur)
        else:
            one_button_box(self, _("Error"), _("Resolution failed."),
                           image=self.im_erreur)

    def resolution(self):
        if self.chrono_on:
            self.play_pause()
        rep = two_button_box(self, _("Confirmation"),
                             _("Do you really want to get the solution?"),
                             _("Yes"), _("No"), image=self.im_question)
        if rep == _("Yes"):
            grille = Grille()
            for i in range(9):
                for j in range(9):
                    val = self.blocs[i, j].get_val()
                    if val:
                        grille.ajoute_init(i, j, val)
            self.configure(cursor="watch")
            self.update()
            sol = grille.solve()
            self.configure(cursor="")
            if type(sol) == np.ndarray:
                for i in range(9):
                    for j in range(9):
                        val = self.blocs[i, j].get_val()
                        if not val:
                            self.blocs[i, j].edit_chiffre(sol[i,j])
                            self.blocs[i, j].affiche_solution()
                self.restart()
                self.b_restart.configure(state="normal")
                self.nb_cases_remplies = 81
            elif sol[1]:
                i,j = sol[1]
                if self.blocs[i, j].get_val():
                    self.blocs[i, j].affiche_erreur()
                i,j = 0,0
                while i < 9 and self.blocs[i, j].is_modifiable():
                    j += 1
                    if j == 9:
                        i += 1
                        j = 0
                if i < 9:
                    # il y a au moins une case de type "initial"
                    rep = two_button_box(self, _("Error"),
                                         _("The grid is wrong. It cannot be solved. Do you want the solution of the initial grid?"),
                                         _("Yes"), _("No"), image=self.im_erreur)
                    if rep == _("Yes"):
                        self.resolution_init()
                else:
                    one_button_box(self, _("Error"), _("The grid is wrong. It cannot be solved."),
                                   image=self.im_erreur)
            else:
                one_button_box(self, _("Error"), _("Resolution failed."),
                               image=self.im_erreur)

    def load_grille(self, file):
        gr = np.loadtxt(file, dtype=int)
        if gr.shape == (9,9):
            self.affiche_grille(gr)
            self.level = "unknown"
        else:
            one_button_box(self, _("Error"), _("This is not a 9x9 sudoku grid."),
                           image=self.im_erreur)

    def import_grille(self, fichier=None):
        """ importe une grille stockée dans un fichier txt sous forme de
            chiffres séparés par des espaces (0 = case vide) """
        if self.chrono_on:
            self.play_pause()
        rep = _("Yes")
        if self.debut:
            rep = two_button_box(self, _("Confirmation"),
                                 _("Do you want to abandon the current puzzle?"),
                                 _("Yes"), _("No"), self.im_question)
        if rep == _("Yes"):
            if not fichier:
                fichier = askopenfilename(initialdir=cst.INITIALDIR,
                                          defaultextension='.txt',
                                          filetypes=[('Text', '*.txt'), ('Tous les fichiers',"*")])
            if fichier:
                try:
                    self.load_grille(fichier)
                except (ValueError,UnicodeDecodeError):
                    one_button_box(self, _("Error"),
                                   _("The file does not have the right format. It should be a .txt file with cell values separated by one space. 0 means empty cell."),
                                   image=self.im_erreur)
                except FileNotFoundError:
                    one_button_box(self, _("Error"),
                                   _("The file %(file)r does not exist.") % fichier,
                                   image=self.im_erreur)
        elif self.debut:
            self.play_pause()

    def export_impression(self):
        """ exporte la grille en image (pour pouvoir l'imprimer) """
        if self.chrono_on:
            self.play_pause()
        fichier = asksaveasfilename(title=_("Export"),
                                    initialdir=cst.INITIALDIR,
                                    defaultextension='.png',
                                    filetypes=[('PNG', '*.png'),
                                               ('JPEG', 'jpg')])
        if fichier:
            grille = np.zeros((9,9), dtype=int)
            for i in range(9):
                for j in range(9):
                    grille[i,j] = self.blocs[i, j].get_val()
            font = ImageFont.truetype("arial.ttf", 64)
            im = Image.new("RGB",(748,748),"white")
            draw = ImageDraw.Draw(im)
            i = 0
            l = 1
            while i < 10:
                if i % 3 == 0:
                    w = 4
                else:
                    w = 2
                draw.line((l,1,l,748), width=w, fill="black")
                draw.line((1,l,748,l),width=w, fill="black")
                l += 80 + w
                i += 1

            for i in range(9):
                for j in range(9):
                    if grille[i,j]:
                        draw.text((26 + j*82 + 2*(j // 3),10 + i*82 + 2*(i // 3)),"%i" % grille[i,j],fill="black",font=font)

            del draw
            im.save(fichier)
