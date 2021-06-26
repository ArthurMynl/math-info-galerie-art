# -*- coding: utf-8 -*-
"""
Projet maths-info - Galerie d'art

Groupe 12 : MEYNIEL Arthur, FOUCHÉ Hugo, BOUY Hugo
"""

import tkinter as tk
from shared import Point
from polygone_predefini import polygone_predefini
from polygone_aléatoire import polygone_aleatoire
from algorithme_genetique import entrainement
from polygon_eclairage import polygon_eclairage
from point_in_polygon import point_in_polygon
from aire_multi_polygones import aire_multi_polygones
from aire_polygone import aire_polygone


class Application():
    """Crée la fenêtre de l'application"""

    def __init__(self, width, height):
        """Prend en argument :
            width : largeur de la fenêtre
            height : hauteur de la fenêtre
        """
        # Création de la fenêtre, du canvas et de la frame de commande
        self.width, self.height = width, height
        self.wnd = tk.Tk()
        self.wnd.title("Jeu de la zone maximale")
        self.cnv = tk.Canvas(self.wnd, width=self.width, height=self.height)
        self.cnv.pack()
        self.frm = tk.Frame(self.wnd, width=self.width, height=100, pady=10,
                            relief='ridge', bd=10)
        self.frm.pack(side=tk.BOTTOM)

        self.frm.columnconfigure(1, minsize=50)

        # Différents paramètres
        tk.Label(self.frm, text="REGLAGES DU JEU")\
            .grid(row=0, column=1, columnspan=5, ipadx=10, ipady=10,
                  sticky='new')

        tk.Label(self.frm, text="Réglages de jeu :")\
            .grid(row=1, column=1, ipadx=10, sticky='n')

        tk.Label(self.frm, text="Reglages de l'IA :")\
            .grid(row=1, column=3, ipadx=10, sticky='n')

        self.map_aleatoire_boutton = tk.IntVar()
        tk.Checkbutton(self.frm, text='carte prédéfinie',
                       variable=self.map_aleatoire_boutton) \
            .grid(row=3, column=1, ipadx=10, sticky='n')

        self.mode_1v1_boutton = tk.IntVar()
        tk.Checkbutton(self.frm, text='mode_1v1',
                       variable=self.mode_1v1_boutton) \
            .grid(row=4, column=1, ipadx=10, sticky='n')

        # Réglage du nombre de générations
        tk.Label(self.frm, text="Nombre de générations :") \
            .grid(row=2, column=2, ipadx=10, sticky='n')

        self.nombre_generation_scale = tk.Scale(self.frm, from_=1, to=100,
                                                orient=tk.HORIZONTAL)
        self.nombre_generation_scale.set(20)
        self.nombre_generation_scale.grid(row=2, column=3,
                                          ipadx=10, sticky='n')

        # Réglage du nombre de gardiens
        tk.Label(self.frm, text="Nombre de gardiens :")\
            .grid(row=3, column=2, ipadx=10, sticky='n')

        self.nombre_gardien_scale = tk.Scale(self.frm, from_=1, to=6,
                                             orient=tk.HORIZONTAL)
        self.nombre_gardien_scale.set(1)
        self.nombre_gardien_scale.grid(row=3, column=3, ipadx=10, sticky='n')

        # Réglage du nombre d'individu
        tk.Label(self.frm, text="Nombre d'individus :")\
            .grid(row=4, column=2, ipadx=10, sticky='n')

        self.nombre_individus_scale = tk.Scale(self.frm, from_=1, to=25,
                                               orient=tk.HORIZONTAL)
        self.nombre_individus_scale.set(10)
        self.nombre_individus_scale.grid(row=4, column=3, ipadx=10, sticky='n')

        # Réglage du taux de mutation
        tk.Label(self.frm, text="Taux de mutation (%) :")\
            .grid(row=5, column=2, ipadx=10, sticky='n')

        self.taux_mutation_scale = tk.Scale(self.frm, from_=0, to=20,
                                            orient=tk.HORIZONTAL)
        self.taux_mutation_scale.set(10)
        self.taux_mutation_scale.grid(row=5, column=3, ipadx=10, sticky='n')

        # Bouton créer map
        tk.Button(self.frm, text="Créer map", command=self.creer_map) \
            .grid(row=5, column=1, ipadx=10, pady=5, sticky='n')

        # Écriture des scores
        self.aire_joueur, self.aire_ia = tk.StringVar(), tk.StringVar()
        self.aire_joueur.set('Aire joueur : 0')
        self.aire_ia.set('Aire IA : 0')
        self.aire_joueur_label = tk.Label(self.wnd,
                                          textvariable=self.aire_joueur)\
            .pack(side=tk.BOTTOM)
        self.aire_ia_label = tk.Label(self.wnd, textvariable=self.aire_ia)\
            .pack(side=tk.BOTTOM)

        # Créer une map par defaut
        self.segments, self.sommets = polygone_predefini(self.cnv, 0)

        # Définition des variables
        self.aire_totale = aire_polygone(self.sommets)
        self.seuil_maximal = 1
        self.gardien_actuels = 0
        self.liste_polygones = []
        self.taille_point = 3

        self.cnv.bind('<Button-1>', self.jouer)

        self.wnd.mainloop()

    def creer_map(self):
        self.cnv.delete('all')
        self.map_aleatoire = self.map_aleatoire_boutton.get()
        if self.map_aleatoire == 0:
            self.segments, self.sommets = polygone_aleatoire(None, self.cnv)
            self.aire_totale = aire_polygone(self.sommets)
        else:
            self.segments, self.sommets = polygone_predefini(self.cnv, None)
            self.aire_totale = aire_polygone(self.sommets)

    def jouer(self, event):
        # Récuperer les données de la fenêtre paramètres
        self.nombre_gardien = self.nombre_gardien_scale.get()
        self.taux_mutation = self.taux_mutation_scale.get() / 100
        self.nombre_individus = self.nombre_individus_scale.get()
        self.generations_maximum = self.nombre_generation_scale.get()

        # Vérification du statut de la partie en cours
        if self.gardien_actuels == 0:
            self.liste_polygones.clear()
            self.cnv.delete('joueur')
            self.cnv.delete('ia')
            self.cnv.delete('lumiere')
            self.aire_ia.set('Aire IA : 0')

        gardien = Point(event.x, event.y)
        if point_in_polygon(gardien.return_tuple(), self.sommets, self.cnv):
            self.gardien_actuels += 1

            # création du gardien
            self.cnv.create_oval(gardien.x - self.taille_point,
                                 gardien.y - self.taille_point,
                                 gardien.x + self.taille_point,
                                 gardien.y + self.taille_point,
                                 fill='blue', tag='joueur')

            polygone_lumiere = polygon_eclairage(gardien.return_tuple(),
                                                 self.sommets, self.cnv)

            self.liste_polygones.append(polygone_lumiere)
            score_joueur = aire_multi_polygones(self.liste_polygones)
            self.aire_joueur.set(f'Aire joueur : {int(score_joueur)}   '
                        f'({round(score_joueur/self.aire_totale * 100, 2)}'
                                 f'%)')

            self.wnd.update()

            if self.gardien_actuels == self.nombre_gardien:
                self.gardien_actuels = 0

                # calculer un positionnement meilleur que le joueur
                self.mode_1v1 = self.mode_1v1_boutton.get()
                if self.mode_1v1 == 1:
                    self.generations_maximum = self.nombre_gardien * 30
                    self.seuil_maximal = score_joueur / self.aire_totale \
                        * 1.0001
                else:
                    self.seuil_maximal = 1

                indiv, _, _, liste_sommets, score_ia = entrainement(
                    self.nombre_individus,
                    self.nombre_gardien,
                    self.taux_mutation,
                    self.seuil_maximal,
                    self.generations_maximum,
                    self.wnd,
                    self.cnv,
                    self.sommets)

                self.aire_ia.set(f'Aire IA : {int(score_ia)}   '
                    f'({round(score_ia/self.aire_totale * 100, 2)}'
                    f'%)')

                # afficher le resultat
                if type(indiv[0]) is list:
                    for gardien in indiv:
                        self.cnv.create_polygon(
                            polygon_eclairage(gardien, liste_sommets,
                                              self.cnv), fill='yellow',
                            tag='lumiere')
                    for gardien in indiv:
                        self.cnv.create_oval(gardien[0] - self.taille_point,
                                             gardien[1] - self.taille_point,
                                             gardien[0] + self.taille_point,
                                             gardien[1] + self.taille_point,
                                             fill='red', tag='ia')
                else:
                    self.cnv.create_polygon(polygon_eclairage(indiv,
                                                              liste_sommets,
                                                              self.cnv),
                                            fill='yellow', tag='lumiere')

                    self.cnv.create_oval(indiv[0] - self.taille_point,
                                         indiv[1] - self.taille_point,
                                         indiv[0] + self.taille_point,
                                         indiv[1] + self.taille_point,
                                         fill='red', tag='ia')

                self.cnv.tag_raise('joueur')


if __name__ == '__main__':
    Application(600, 400)
