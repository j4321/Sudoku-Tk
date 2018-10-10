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


Non GUI sudoku puzzle class used to solve / generate puzzles
"""
#TODO: speed up puzzle generation

import numpy as np
from pickle import Pickler

class Grille:
    """ Grille de sudoku avec fonction de résolution """

    def __init__(self, grille=np.ones((9,9,9), dtype=int)):
        self.grille = grille.copy()
        self.initiale = grille.copy() # grille initiale
        self.position = np.zeros((9,9), dtype=int)

    def affiche(self):
        ch = ""
        for i in range(9):
            for j in range(9):
                case = ["%i" % (k + 1) for k in range(9) if self.grille[i,j,k]]
                ch += "".join(case) + (9 - len(case))*" "
                if j % 3 == 2 and j!=8:
                    ch += "|"
                else:
                    ch += " "
            if i % 3 == 2 and i!=8:
                ch += "\n" + 2*(29*"-" + "|") + 29*"-" + "\n"
            else:
                ch += "\n"
        print(ch)

    def get_grille(self):
        return self.grille

    def get_initiale(self):
        return self.initiale

    def nb_cases_remplies(self):
        """ Renvoie le nombre de cases ne contenant qu'une possibilité """
        nb = 0
        for i in range(9):
            for j in range(9):
                if self.grille[i,j,:].sum() == 1:
                    nb += 1
        return nb

    def ajoute(self,i,j,val):
        """ met val dans la case (i,j) (et donc supprime les autres possibilités)
            et simplifie """
        self.grille[i,j,:] = np.zeros(9, dtype=int)
        self.grille[i,j,val-1] = 1
        self.simplifie(i,j)

    def enleve(self,i,j):
        """ Enlève le chiffre contenu dans la case (i,j) (qui ne contient qu'une
            seule possibilité) dans la grille et la grille initiale et l'ajoute
            dans les possibilités des autres cases de la ligne / colonne / bloc
            (seulement si elles contiennent plusieurs possibilités) """
        val = self.grille[i,j,:].argmax()
        # réinitialisation des possibilités de la case
        self.grille[i,j,:] = np.ones(9, dtype=int)
        self.initiale[i,j,:] = np.ones(9, dtype=int)
        # ajout de val dans les possibilités des autres cases
        for k in range(9):
            # ligne
            if self.grille[i,k,:].sum() != 1:
                self.grille[i,k,val] = 1
            if self.initiale[i,k,:].sum() != 1:
                self.initiale[i,k,val] = 1
            # colonne
            if self.grille[k,j,:].sum() != 1:
                self.grille[k,j,val] = 1
            if self.initiale[k,j,:].sum() != 1:
                self.initiale[k,j,val] = 1
        # bloc
        a, b = i//3, j//3
        for x in range(3*a,3*(a+1)):
            for y in range(3*b,3*(b+1)):
                if self.grille[x,y,:].sum() != 1:
                    self.grille[x,y,val] = 1


    def ajoute_init(self, i, j, val):
        """ met val dans la case (i,j) de la grille initiale (et dans la grille
            pour que les deux soient cohérentes)
            et simplifie """
        self.ajoute(i,j,val)
        self.initiale[i,j,:] = np.zeros(9, dtype=int)
        # ligne
        self.initiale[i,:,val-1] = np.zeros(9, dtype=int)
        # colonne
        self.initiale[:,j,val-1] = np.zeros(9, dtype=int)
        # bloc
        a, b = i//3, j//3
        self.initiale[3*a:3*(a+1),3*b:3*(b+1),val-1] = np.zeros((3,3), dtype=int)
        # on remet la valeur dans la case (i,j)
        self.initiale[i,j,val-1] = 1

    def sauve(self,fichier):
        """ enregistre la grille dans fichier """
        with open(fichier,"wb") as f:
            p = Pickler(f)
            p.dump(self)

    def get_sudoku(self):
        """ renvoie un tableau 9x9 dont les cases contiennent 0 si elles
            correspondent à une case contenant plusieurs possibilités,
            le chiffre correspondant sinon. """
        tab = np.zeros((9,9), dtype=int)
        for i in range(9):
            for j in range(9):
                if self.grille[i,j,:].sum() == 1:
                    tab[i,j] = self.grille[i,j,:].argmax()+1
        return tab

    def __repr__(self):
        """ affiche seulement les cases ne contenant qu'un chiffre """
        ch = ""
        for i in range(9):
            for j in range(9):
                if self.grille[i,j,:].sum() == 1:
                    ch += "%i" % (self.grille[i,j,:].argmax()+1)
                else:
                    ch += " "
                if j % 3 == 2 and j<8:
                    ch += "|"
            ch += "\n"
            if i % 3 == 2 and i<8:
                ch += "---|---|---\n"
        return ch

    def est_remplie(self):
        """ renvoie True ssi la grille est remplie """
        for i in range(9):
            for j in range(9):
                if self.grille[i,j,:].sum() != 1:
                    return False
        return True

    def case_remplie(self,i,j):
        """ Renvoie True ssi la case (i,j) ne contient qu'une valeur """
        return self.grille[i,j,:].sum() == 1

    def simplifie(self,i,j):
        """ La case (i,j) ne doit contenir qu'une valeur.
            Cette valeur est enlevée dans les autres cases de la ligne,
            de la colonne et du bloc """
        val = self.grille[i,j,:].argmax()
        # ligne
        self.grille[i,:,val] = np.zeros(9, dtype=int)
        # colonne
        self.grille[:,j,val] = np.zeros(9, dtype=int)
        # bloc
        a, b = i//3, j//3
        self.grille[3*a:3*(a+1),3*b:3*(b+1),val] = np.zeros((3,3), dtype=int)
        # on remet la valeur dans la case (i,j)
        self.grille[i,j,val] = 1

    def case_vide(self):
        """ Renvoie les coordonnées de la première case vide (que des 0)
            rencontrée s'il y en a, ne renvoie rien sinon """
        for i in range(9):
            for j in range(9):
                if self.grille[i,j,:].sum() == 0:
                    return (i,j)

    def nettoie(self):
        """ Nettoie la grille en suivant les règles :

            - Si une case ne contient qu'une seule valeur, on l'enlève des autres
              cases de la ligne / colonne / bloc

            - Si 2 cases de la même ligne / colonne / bloc ne peuvent contenir
              que les 2 mêmes valeurs, on enlève ces valeurs des autres case de
              la ligne / colonne / bloc

            - Si une valeur de peut être mise que dans une seule case de la
              ligne / colonne / bloc, on enlève les autres valeurs de cette case

            - Si 2 valeurs ne peuvent être mises que dans les 2 mêmes cases d'une
              ligne / colonne / bloc, on enlève les autres valeurs de ces cases

            - Si sur une ligne / colonne, une valeur ne peut aller que dans 2
              cases qui sont dans le même bloc, on enlève cette valeur des autres
              cases du bloc

            - Si dans un bloc, une valeur ne peut aller que dans 2 cases qui
              sont sur la même ligne / colonne, on l'enlève des autres cases de
              la ligne / colonne
        """

        # nombre de posibilités dans chaque case :
        nb_possibilites = self.grille.sum(2)

        # recherche de chiffres seuls et de paires du type deux cases qui
        # ne peuvent contenir que les deux mêmes chiffres
        for i in range(9):
            for j in range(9):
                n = nb_possibilites[i,j]
                if n == 1:
                    self.simplifie(i,j)
                elif n == 2:
                    case = self.grille[i,j,:]
                    val1, val2 = case.argsort()[7:9]
                    # recherche de paires dans la ligne
                    k = j + 1
                    while k < 9 and list(case) != list(self.grille[i,k,:]):
                        k += 1
                    if k < 9:
                        # il y a une paire,
                        # il faut enlever ces chiffres des autres cases
                        self.grille[i,:,(val1,val2)] = np.zeros((2,9), dtype=int)
                        self.grille[i,j,(val1,val2)] = np.ones(2, dtype=int)
                        self.grille[i,k,(val1,val2)] = np.ones(2, dtype=int)

                    # recherche de paires dans la colonne
                    k = i + 1
                    while k < 9 and list(case) != list(self.grille[k,j,:]):
                        k += 1
                    if k < 9:
                        # il y a une paire,
                        # il faut enlever ces chiffres des autres cases
                        self.grille[:,j,(val1,val2)] = np.zeros((9,2), dtype=int)
                        self.grille[i,j,(val1,val2)] = np.ones(2, dtype=int)
                        self.grille[k,j,(val1,val2)] = np.ones(2, dtype=int)

                    # recherche de paires dans le bloc
                    a, b = i//3, j//3
                    x, y = 3*a, 3*b
                    while x < 3*(a+1) and (list(case) != list(self.grille[x,y,:]) or (x == i and y == j)):
                        y += 1
                        if y == 3*(b+1):
                            y = 3*b
                            x += 1
                    if x < 3*(a+1):
                        # il y a une paire,
                        # il faut enlever ces chiffres des autres cases
                        self.grille[3*a:3*(a+1),3*b:3*(b+1),(val1,val2)] = np.zeros((3,3,2), dtype=int)
                        self.grille[i,j,(val1,val2)] = np.ones(2, dtype=int)
                        self.grille[x,y,(val1,val2)] = np.ones(2, dtype=int)

        # lignes

        # occurences de chaque chiffre par ligne :
        occ_lignes = self.grille.sum(1)

        for i in range(9):
            # liste des chiffres qui ne peuvent être mis que dans deux cases de la ligne :
            paires = []
            for val in range(9):
                # nb d'occurences de val dans la ligne i
                ligne = self.grille[i,:,val]
                nb = occ_lignes[i,val]
                if nb == 1:
                    j = ligne.argmax()
                    self.grille[i,j,:] = np.zeros(9, dtype=int)
                    self.grille[i,j, val] = 1
                    self.simplifie(i,j)

                elif nb == 2:
                    j1, j2 = ligne.argsort()[7:9]
                    paires.append((val,(j1,j2)))
                    if j1//3 == j2//3:
                        # les 2 possibilités sont dans le même bloc
                        a, b = i//3, j1//3
                        self.grille[3*a:3*(a+1),3*b:3*(b+1),val] = np.zeros((3,3), dtype=int)
                        self.grille[i,(j1,j2),val] = np.ones(2, dtype=int)
            n = len(paires)
            for k in range(n -1):
                l = k + 1
                p = paires[k]
                while l < n and p[1] != paires[l][1]:
                    l += 1
                if l < n:
                    # il y a une paire (ici deux chiffres qui ne peuvent aller
                    # que dans les deux mêmes cases)
                    # il faut enlever les autres possibilités de ces deux cases
                    self.grille[i,p[1],:] = np.zeros((2,9), dtype=int)
                    self.grille[i,p[1],p[0]] = np.ones(2, dtype=int)
                    self.grille[i,p[1],paires[l][0]] = np.ones(2, dtype=int)

        # colonnes

        # occurences de chaque chiffre par colonne :
        occ_colonnes = self.grille.sum(0)

        for j in range(9):
            # liste des chiffres qui ne peuvent être mis que dans deux cases de la colonne :
            paires = []
            for val in range(9):
                # nb d'occurences de val dans la colonne j
                colonne = self.grille[:,j,val]
                nb = occ_colonnes[j,val]
                if nb == 1:
                    i = colonne.argmax()
                    self.grille[i,j,:] = np.zeros(9, dtype=int)
                    self.grille[i,j, val] = 1
                    self.simplifie(i,j)

                elif nb == 2:
                    i1,i2 = colonne.argsort()[7:9]
                    paires.append((val,(i1,i2)))
                    if i1//3 == i2//3:
                        # les 2 possibilités sont dans le même bloc
                        a, b = i1//3, j//3
                        self.grille[3*a:3*(a+1),3*b:3*(b+1),val] = np.zeros((3,3), dtype=int)
                        self.grille[(i1,i2),j,val] = np.ones(2, dtype=int)

            n = len(paires)
            for k in range(n -1):
                l = k + 1
                p = paires[k]
                while l < n and p[1] != paires[l][1]:
                    l += 1
                if l < n:
                    # il y a une paire (ici deux chiffres qui ne peuvent aller
                    # que dans les deux mêmes cases)
                    # il faut enlever les autres possibilités de ces deux cases
                    self.grille[p[1],j,:] = np.zeros((2,9), dtype=int)
                    self.grille[p[1],j,p[0]] = np.ones(2, dtype=int)
                    self.grille[p[1],j,paires[l][0]] = np.ones(2, dtype=int)

        # blocs

        for a in range(3):
            for b in range(3):
                # liste des chiffres qui ne peuvent être mis que dans deux cases du bloc :
                paires = []
                for val in range(9):
                    # nb d'occurences de val dans le bloc
                    bloc = self.grille[3*a:3*(a+1),3*b:3*(b+1),val].flatten()
                    nb = bloc.sum()
                    if nb == 1:
                        k = bloc.argmax()
                        i,j = 3*a + k//3, 3*b + k % 3
                        self.grille[i,j,:] = np.zeros(9, dtype=int)
                        self.grille[i,j,val] = 1
                        self.simplifie(i,j)

                    elif nb == 2:
                        k1, k2 = bloc.argsort()[7:9]
                        p1 = 3*a + k1//3, 3*b + k1 % 3
                        p2 = 3*a + k2//3, 3*b + k2 % 3
                        paires.append((val,(p1,p2)))

                        if p1[0] == p2[0]:
                            # les deux possibilités sont sur la même ligne
                            self.grille[p1[0],:,val] = np.zeros(9, dtype=int)
                            self.grille[(p1[0],p2[0]),(p1[1],p2[1]),val] = np.ones(2, dtype=int)
                        elif p1[1] == p2[1]:
                            # les deux possibilités sont sur la même colonne
                            self.grille[:,p1[1],val] = np.zeros(9, dtype=int)
                            self.grille[(p1[0],p2[0]),(p1[1],p2[1]),val] = np.ones(2, dtype=int)
                n = len(paires)
                for k in range(n -1):
                    l = k + 1
                    v, (p1, p2) = paires[k]
                    while l < n and (p1, p2) != paires[l][1]:
                        l += 1
                    if l < n:
                        # il y a une paire (ici deux chiffres qui ne peuvent aller
                        # que dans les deux mêmes cases)
                        # il faut enlever les autres possibilités de ces deux cases
                        self.grille[(p1[0],p2[0]),(p1[1], p2[1]),:] = np.zeros((2,9), dtype=int)
                        self.grille[(p1[0],p2[0]),(p1[1], p2[1]),v] = np.ones(2, dtype=int)
                        self.grille[(p1[0],p2[0]),(p1[1], p2[1]),paires[l][0]] = np.ones(2, dtype=int)

    def nettoie_singlets(self):
        """ Nettoie la grille en suivant les règles :

            - Si une case ne contient qu'une seule valeur, on l'enlève des autres
              cases de la ligne / colonne / bloc

            - Si une valeur de peut être mise que dans une seule case de la
              ligne / colonne / bloc, on enlève les autres valeurs de cette case
        """

        # nombre de posibilités dans chaque case :
        nb_possibilites = self.grille.sum(2)

        # recherche de chiffres seuls et de paires du type deux cases qui
        # ne peuvent contenir que les deux mêmes chiffres
        for i in range(9):
            for j in range(9):
                n = nb_possibilites[i,j]
                if n == 1:
                    self.simplifie(i,j)
        # lignes

        # occurences de chaque chiffre par ligne :
        occ_lignes = self.grille.sum(1)

        for i in range(9):
            # liste des chiffres qui ne peuvent être mis que dans deux cases de la ligne :
            for val in range(9):
                # nb d'occurences de val dans la ligne i
                ligne = self.grille[i,:,val]
                nb = occ_lignes[i,val]
                if nb == 1:
                    j = ligne.argmax()
                    self.grille[i,j,:] = np.zeros(9, dtype=int)
                    self.grille[i,j, val] = 1
                    self.simplifie(i,j)

        # colonnes

        # occurences de chaque chiffre par colonne :
        occ_colonnes = self.grille.sum(0)

        for j in range(9):
            # liste des chiffres qui ne peuvent être mis que dans deux cases de la colonne :
            for val in range(9):
                # nb d'occurences de val dans la colonne j
                colonne = self.grille[:,j,val]
                nb = occ_colonnes[j,val]
                if nb == 1:
                    i = colonne.argmax()
                    self.grille[i,j,:] = np.zeros(9, dtype=int)
                    self.grille[i,j, val] = 1
                    self.simplifie(i,j)
        # blocs

        for a in range(3):
            for b in range(3):
                # liste des chiffres qui ne peuvent être mis que dans deux cases du bloc :
                for val in range(9):
                    # nb d'occurences de val dans le bloc
                    bloc = self.grille[3*a:3*(a+1),3*b:3*(b+1),val].flatten()
                    nb = bloc.sum()
                    if nb == 1:
                        k = bloc.argmax()
                        i,j = 3*a + k//3, 3*b + k % 3
                        self.grille[i,j,:] = np.zeros(9, dtype=int)
                        self.grille[i,j,val] = 1
                        self.simplifie(i,j)


    def solve(self):
        """ résolution de la grille : renvoie la première possibilité trouvée.
            couple les techniques de résolution humaine au backtracking """
        # méthodes humaines : 20 tours
        compt = 0
        vide = self.case_vide()
        if vide:#la grille de départ est erronée
            return "erreur", vide
        else:
            for compteur in range(20):
                self.nettoie()
            vide = self.case_vide()
            if vide:#la grille de départ est erronée
                return "erreur", vide
            elif self.est_remplie(): # la grille est remplie
                return self.get_sudoku()
            else :
                # on fini de remplir la grille par backtracking

                # indices de la case dans laquelle on va tester une valeur :
                i,j = 0,0
                # grille de référence pour pouvoir revenir en arrière lors du backtracking :
                reference = self.grille.copy()
                while compt < 2000:
                    compt +=1
                    # simplification de la grille
                    self.nettoie()
                    self.nettoie()
                    # vérification de la grille
                    if not self.case_vide():
                        # pas de case vide
                        case = self.grille[i,j,:]
                        n = case.sum()
                        if n > self.position[i,j]:
                            # il y a plus d'une possibilité dans la case et il est
                            # possible de tester la possibilité n° self.position[i,j]
                            possibilites = (-case).argsort()[:n]
                            self.ajoute(i,j,possibilites[self.position[i,j]] + 1)
                        # on passe à la case suivante
                        j += 1
                        if j == 9:
                            i += 1
                            j = 0
                        if i == 9:
                            # la grille est remplie
                            return self.get_sudoku()

                    else:
                        # vérification de la grille : cases vides -> mauvaise possibilité
                        # recherche de la case posant problème :
                        # on revient en arrière jusqu'à la dernière case où
                        # toutes les possibilités n'ont pas été testés
                        while self.position[i,j] >= reference[i,j,:].sum()-1:
                            self.position[i,j] = 0
                            j -= 1
                            if j < 0:
                                j = 8
                                i -= 1
                                if i < 0:
                                    # toutes les possibilités ont été testées,
                                    # la grille de départ était certainement erronée
                                    return "échec", None
                        # passage à la possibilité suivante dans la case posant problème
                        self.position[i,j] += 1

                        # réinitialistaion de la grille pour repartir sur des bases saines
                        self.grille[i+1:,:,:] = reference[i+1:,:,:].copy()
                        self.grille[i,j:,:] = reference[i,j:,:].copy()
                        self.nettoie()
                        self.nettoie()
                return "échec", None

def genere_grille_complete(nb_val=9):
    """
        Génère une grille de sudoku complète aléatoirement.
        On part d'une grille vide, puis on ajoute aléatoirement nb_val valeurs
        dans la grille puis on lance l'algorithme de résolution. Si la grille
        est invalide, on recommence.
    """
    grille = ()
    while not type(grille) is np.ndarray:
        g = Grille()
        for compteur in range(nb_val):
            val = np.random.randint(1,10)
            i,j = np.random.randint(9, size=2)
            while g.case_remplie(i,j):
                i,j = np.random.randint(9, size=2)
            g.ajoute_init(i,j,val)
        grille = g.solve()
    return g

def genere_grille():
    """ renvoie une grille de sudoku incomplète en enlevant aléatoirement des
        chiffres mais en s'assurant que la solution reste unique.
        La grille est renvoyée quand il n'est plus possible d'enlever de valeur
        sans perdre l'unicité """
    grille_complete = genere_grille_complete()
    grille = Grille(grille_complete.get_grille())
    nb = 0 # nombre de cases vides
    # liste des cases nécessaires pour assurer l'unicité de la solution
    val_necessaires = []
    while (len(val_necessaires) + nb) < 81:
        # on enlève une case au hasard, puis on vérifie que la solution est
        # toujours unique
        g = Grille(grille.get_grille()) # copie test de la grille
        i0, j0 = np.random.randint(9, size=2)
        while (i0, j0) in val_necessaires or not grille.case_remplie(i0, j0):
            i0, j0 = np.random.randint(9, size=2)
        g.enleve(i0, j0)
        for i in range(20):
            g.nettoie()
        if g.est_remplie():
            # la solution est toujours unique
            grille.enleve(i0, j0)
            nb += 1
        else:
            # il y a incertitude sur l'unicité de la solution
            sol = grille_complete.get_sudoku()
            g_grille = g.get_grille()
            test = []
            # liste des cases (i,j) contenant plusieurs possibilités
            coord = []
            # chaque case du tableau test (ici une liste de liste) contient la liste
            # des possibilités pour la case correspondante de la grille sauf
            # la valeur de la case dans la grille complète initiale
            for i in range(9):
                test.append([])
                for j in range(9):
                    case = [(k + 1) for k in range(9) if g_grille[i,j,k]]
                    if len(case) > 1:
                        coord.append((i,j))
                    case.remove(sol[i,j])
                    test[i].append(case)

            n = len(coord)
            k = 0
            i,j = coord[k]
            pos = 0 # indice de la possibilité testée
            sol2 = ()
            while k < n and not (type(sol2) is np.ndarray):
                g_tmp = Grille(g_grille)
                g_tmp.ajoute_init(i,j,test[i][j][pos])
                sol2 = g_tmp.solve()
                pos += 1
                if pos >= len(test[i][j]):
                    pos = 0
                    k += 1
                    if k < n:
                        i,j = coord[k]
            if k == n:
                # unicité de la solution
                grille.enleve(i0,j0)
                nb += 1
            else:
                # la solution n'est plus unique
                val_necessaires.append((i0,j0))

    return grille


def stats_grille(grille):
    g = Grille(grille.get_grille())
    singlets = 0
    total = 0
    nb = g.nb_cases_remplies()
    while singlets < 20 and not g.est_remplie():
        singlets += 1
        g.nettoie_singlets()
    if singlets == 20:
        g = Grille(grille.get_grille())
        while total < 20 and not g.est_remplie():
            total += 1
            g.nettoie()
    return nb, singlets, total


def difficulte_grille(grille):
    """Return puzzle level."""
    _, ns, nt = stats_grille(grille)
    if ns < 20:
        return "easy"
    elif nt < 20:
        return "medium"
    else:
        return "difficult"
