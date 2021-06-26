# -*- coding: utf-8 -*-
"""
Projet maths-info - Galerie d'art

Groupe 12 : MEYNIEL Arthur, FOUCHÉ Hugo, BOUY Hugo
"""

import tkinter as tk
import math
from shared import Point, projection_point_cercle, dist
from point_in_polygon import point_in_polygon
from intersections_rayons_obstacles import intersections_rayons_obstacles
from generateur_map import generateur


class Gardien:
    def __init__(self, Point, direction, puissance, identite, app,
                 comportement, amplitude):
        """
        Arguments :
        - Point : objet de classe 'Point' représentant la position du
                    gardien
        - direction : int representant la rotation du gardien dans le sens
                        trigonometrique
        - puissance : distance d'éclairage de la lampe torche
        - cnv : objet de type tkinter.Canvas dans lequel le polygone sera
                dessiné
        - identite : int représentant le numero d'identification du gardien
        - app : objet de type 'Application'
        - comportement : 'immobile', 'toupie', 'ronde' definissant le
                            comportement du gardien
        - amplitude : definit l'amplitude du gardien dans le cas ronde
        """
        self.position = Point  # Position en pixels
        self.direction = direction  # En degrés
        self.angle = 60  # En degrés
        self.puissance = puissance    # Puissance de la torche en pixels
        self.vitesse = 5
        self.identite = identite
        self.app = app
        self.comportement = comportement
        self.amplitude = amplitude
        self.tick = 0
        taille = 3
        self.app.cnv.create_oval(self.position.x - taille,
                                 self.position.y - taille,
                                 self.position.x + taille,
                                 self.position.y + taille,
                                 fill="black", tag=f'Gardien{identite}')
        self.eclaire()

    def reculer(self):
        """
        Permet de reculer le gardien
        """
        rad = self.direction * math.pi / 180
        self.position.move(round(math.sin(rad - math.pi / 2) * self.vitesse),
                           round(math.cos(rad - math.pi / 2) * self.vitesse))
        if not point_in_polygon(self.position.return_tuple(),
                                self.app.liste_points):
            self.position.move(round(math.sin(rad - math.pi / 2)
                                     * - self.vitesse),
                               round(math.cos(rad - math.pi / 2)
                                     * - self.vitesse))
        else:
            self.app.cnv.move(f'Gardien{self.identite}',
                              round(math.sin(rad - math.pi / 2)
                                    * self.vitesse),
                              round(math.cos(rad - math.pi / 2)
                                    * self.vitesse))

        self.eclaire()

    def avancer(self):
        """
        Permet d'avancer le gardien
        """
        rad = self.direction * math.pi / 180
        self.position.move(int(math.sin(rad - math.pi / 2) * - self.vitesse),
                           int(math.cos(rad - math.pi / 2) * - self.vitesse))
        if not point_in_polygon(self.position.return_tuple(),
                                self.app.liste_points):
            self.position.move(int(math.sin(rad - math.pi / 2) * self.vitesse),
                               int(math.cos(rad - math.pi / 2) * self.vitesse))
        else:
            self.app.cnv.move(f'Gardien{self.identite}',
                              int(math.sin(rad - math.pi / 2)
                                  * - self.vitesse),
                              int(math.cos(rad - math.pi / 2)
                                  * - self.vitesse))
        self.eclaire()

    def turn_right(self):
        """
        Permet de faire pivoter le gardien sur sa droite
        """
        self.direction -= 10
        if self.direction <= 0:
            self.direction = 360
        self.eclaire()

    def turn_left(self):
        """
        Permet de faire pivoter le gardien sur sa gauche
        """
        self.direction += 10
        if self.direction >= 360:
            self.direction = 0
        self.eclaire()

    def eclaire(self):
        """
        Crée l'éclairage
        """
        self.app.cnv.delete(f'Lumiere_gardien_{self.identite}')
        self.torche_tuple = []
        torche_infinie = intersections_rayons_obstacles(self.app.cnv,
                                                        self.position,
                                                        5, self.angle,
                                                        self.direction,
                                                        self.app.
                                                        liste_segments,
                                                        demo=False,
                                                        return_inter=True)
        for point in torche_infinie:
            if dist(self.position, point) <= self.puissance:
                self.torche_tuple.append(point.return_tuple())
            else:
                self.torche_tuple.append(
                    projection_point_cercle(self.position, point,
                                            self.puissance).return_tuple())

        self.torche_tuple.append(self.position.return_tuple())
        self.app.cnv.create_polygon(self.torche_tuple, fill="yellow",
                                    tag=f'Lumiere_gardien_{self.identite}')

    def agir(self):
        """
        Lance l'action du gardien en fonction de son comportement
        """
        if self.comportement == "toupie":
            self.toupie()
        elif self.comportement == "ronde":
            self.ronde()

    def toupie(self):
        """
        Fait tourner le gardien sur lui meme
        """
        if self.app.in_game:
            self.turn_left()
            self.app.voleur.test_defaite()
            self.app.cnv.after(50, self.toupie)

    def ronde(self):
        """
        Fait avancer le gardien sur une certaine amplitude puis faire demi-tour
        """
        if self.app.in_game:
            self.tick += 1
            if self.tick < self.amplitude / self.vitesse:
                self.avancer()
            else:
                self.tick = 0
                self.direction += 180
                if self.direction >= 360:
                    self.direction -= 360
            self.app.voleur.test_defaite()
            self.app.cnv.after(50, self.ronde)


class Voleur:
    def __init__(self, Point, app):
        """
        Arguments :
            - Point : objet de classe 'Point' représentant la position du
                      voleur
            - app : objet de type 'Application'
        """
        self.position = Point
        self.vitesse = 10
        self.score = 0
        self.inventaire = list()
        self.nb_tableaux_restants = app.nb_tableaux
        self.app = app
        taille = 3
        self.app.cnv.create_oval(self.position.x - taille,
                                 self.position.y - taille,
                                 self.position.x + taille,
                                 self.position.y + taille,
                                 fill='blue', tag='voleur')

    def avancer(self, event):
        """
        Permet de déplacer le gardien au clavier
        """
        if self.app.in_game:
            for i in range(self.vitesse):
                self.position.move(0, -self.vitesse / self.vitesse)
                if not point_in_polygon(self.position.return_tuple(),
                                        self.app.liste_points):
                    self.position.move(0, +self.vitesse / self.vitesse)
                else:
                    self.app.cnv.move('voleur', 0,
                                      -self.vitesse / self.vitesse)
                self.test_defaite()

    def reculer(self, event):
        """
        Permet de déplacer le gardien au clavier
        """
        if self.app.in_game:
            for i in range(self.vitesse):
                self.position.move(0, self.vitesse / self.vitesse)
                if not point_in_polygon(self.position.return_tuple(),
                                        self.app.liste_points):
                    self.position.move(0, -self.vitesse / self.vitesse)
                else:
                    self.app.cnv.move('voleur', 0, self.vitesse / self.vitesse)
                self.test_defaite()

    def droite(self, event):
        """
        Permet de déplacer le gardien au clavier
        """
        if self.app.in_game:
            for i in range(self.vitesse):
                self.position.move(+self.vitesse / self.vitesse, 0)
                if not point_in_polygon(self.position.return_tuple(),
                                        self.app.liste_points):
                    self.position.move(-self.vitesse / self.vitesse, 0)
                else:
                    self.app.cnv.move('voleur', +self.vitesse / self.vitesse,
                                      0)
                self.test_defaite()

    def gauche(self, event):
        """
        Permet de déplacer le gardien au clavier
        """
        if self.app.in_game:
            for i in range(self.vitesse):
                self.position.move(-self.vitesse / self.vitesse, 0)
                if not point_in_polygon(self.position.return_tuple(),
                                        self.app.liste_points):
                    self.position.move(self.vitesse / self.vitesse, 0)
                else:
                    self.app.cnv.move('voleur', -self.vitesse / self.vitesse,
                                      0)
                self.test_defaite()

    def interagir(self, event):
        """
        Permet au voleur d'interagir avec son environement
        """
        if self.app.in_game:
            self.victoire()
            self.voler()
            self.bouton()

    def bouton(self):
        """
        Permet d'activer un boutton
        """
        for Bouton in self.app.liste_boutons:
            if abs(self.position.x - Bouton.position.x) <= 5 and \
               abs(self.position.y - Bouton.position.y) <= 5:
                Bouton.switch()

    def voler(self):
        """
        Permet de voler un tableau
        """
        liste_a_suppr = list()
        for i in range(self.nb_tableaux_restants):
            if abs(self.position.x - self.app.liste_tableaux[i].
                   localisation.x) <= self.app.liste_tableaux[i].\
                taille + 1 and\
                    abs(self.position.y - self.app.liste_tableaux[i].
                        localisation.y) <= self.app.liste_tableaux[i].\
                    taille + 1:
                liste_a_suppr.append(i)

        for i_tableau in liste_a_suppr:
            self.app.liste_tableaux[i_tableau].vol()
            self.inventaire.append(self.app.liste_tableaux[i_tableau])
            self.app.liste_tableaux.pop(i_tableau)
            self.nb_tableaux_restants -= 1

    def victoire(self):
        """
        Teste si le voleur a gagné ou non la partie
        """
        if abs(self.position.x - self.app.emplacement_victoire[0]) <= 5 \
            and abs(self.position.y - self.app.emplacement_victoire[1] <= 5)\
                and len(self.inventaire) == self.app.nb_tableaux:
            self.app.in_game = False
            tk.Label(self.app.frm, text="Vous avez gagné",
                     fg="red", font=(None, 16)).pack()

    def defaite(self):
        """
        Stoppe le jeu et annonce la défaite
        """
        self.app.in_game = False
        tk.Label(self.app.frm, text="Vous avez perdu",
                 fg="red", font=(None, 16)).pack()

    def test_defaite(self):
        if self.app.in_game:
            lose = False
            for lampe in self.app.liste_lampes:
                if lampe.etat:
                    if point_in_polygon(self.position.return_tuple(),
                                        lampe.torche_tuple):
                        lose = True
            for gardien in self.app.liste_gardiens:
                if point_in_polygon(self.position.return_tuple(),
                                    gardien.torche_tuple):
                    lose = True
            if lose:
                self.defaite()


class Bouton:
    def __init__(self, Point, lien, cnv, identifiant):
        """
        Arguments :
            - Point : objet de classe 'Point' représentant la position du
                      bouton
            - etat : booleen représentant l'activation ou non du bouton
                     (True : allumé, False : éteint)
            - lien : objet de la carte pouvant etre activé a l'aide d'un
                     bouton (lampe)
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera
                    deplacé
            - identifiant : int représentant le numero d'identification
                            du gardien
        """
        self.position = Point
        self.etat = True
        self.lien = lien
        self.identifiant = identifiant
        self.cnv = cnv
        taille = 3
        couleur = 'green'
        self.cnv.create_rectangle(self.position.x - taille,
                                  self.position.y - taille,
                                  self.position.x + taille,
                                  self.position.y + taille,
                                  fill=couleur,
                                  tag=f'Bouton_{identifiant}')

    def switch(self):
        """
        Permet d'allumer ou d'éteindre un bouton
        """
        if self.etat:
            self.etat = False
            self.cnv.itemconfigure(f'Bouton_{self.identifiant}', fill='red')
            self.lien.switch()
        else:
            self.etat = True
            self.cnv.itemconfigure(f'Bouton_{self.identifiant}', fill='green')
            self.lien.switch()


class Lampe:
    def __init__(self, Point, puissance, identifiant, app):
        """
        Arguments :
            - Point : objet de classe 'Point' représentant la position de la
                      lampe
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera
                    deplacé
            - puissance : distance d'eclairage de la lampe
            - identifiant : int représentant le numero d'identification
                            de la lampe
        """
        self.localisation = Point
        self.identifiant = identifiant
        self.app = app
        self.puissance = puissance
        self.etat = True
        taille = 3
        couleur = "yellow"
        self.app.cnv.create_oval(self.localisation.x - taille,
                                 self.localisation.y - taille,
                                 self.localisation.x + taille,
                                 self.localisation.y + taille,
                                 fill=couleur,
                                 tag=f'Lampe_{identifiant}')
        self.allume()

    def switch(self):
        """
        Allume/éteint la lampe
        """
        if self.etat:
            self.etat = False
            self.eteindre()
        else:
            self.etat = True
            self.allume()

    def eteindre(self):
        """
        Éteint la lampe
        """
        self.app.cnv.itemconfigure(f'Lampe_{self.identifiant}', fill="black")
        self.app.cnv.delete(f'Lumiere_lampe_{self.identifiant}')

    def allume(self):
        """
        Crée l'éclairage
        """
        self.torche_tuple = []
        torche_infinie = intersections_rayons_obstacles(self.app.cnv,
                                                        self.localisation,
                                                        20, 360,
                                                        0,
                                                        self.app.
                                                        liste_segments,
                                                        demo=False,
                                                        return_inter=True)
        for point in torche_infinie:
            if dist(self.localisation, point) <= self.puissance:
                self.torche_tuple.append(point.return_tuple())
            else:
                self.torche_tuple.append(
                    projection_point_cercle(self.localisation, point,
                                            self.puissance).return_tuple())

        self.app.cnv.create_polygon(self.torche_tuple, fill="yellow",
                                    tag=f'Lumiere_lampe_{self.identifiant}')


class Tableau:
    def __init__(self, Point, cnv, identifiant):
        """
        Arguments :
            - Point : objet de classe 'Point' représentant la position du
                      tableau
            - cnv : objet de type tkinter.Canvas dans lequel le voleur sera
                    deplacé
            - identifiant : int représentant le numero d'identification
                            du tableau
        """
        self.localisation = Point
        self.identifiant = identifiant
        self.cnv = cnv
        self.taille = 4
        couleur = "orange"
        cnv.create_rectangle(self.localisation.x - self.taille,
                             self.localisation.y - self.taille,
                             self.localisation.x + self.taille,
                             self.localisation.y + self.taille,
                             fill=couleur,
                             tag=f'Tableau_{identifiant}')

    def vol(self):
        self.cnv.delete(f'Tableau_{self.identifiant}')


class Application:
    def __init__(self, width, height):
        """
        Arguments :
            - width : largeur du canvas
            - height : hauteur du canvas
        """
        self.width_canvas, self.height_canvas = width, height
        self.width_frame, self.height_frame = 100, height

        self.wnd = tk.Tk()
        self.cnv = tk.Canvas(self.wnd, width=self.width_canvas,
                             height=self.height_canvas)
        self.cnv.pack(side=tk.LEFT)
        self.frm = tk.Frame(self.wnd, width=self.width_frame,
                            height=self.height_frame)
        self.frm.pack(side=tk.RIGHT)

        # bouton rejouer
        tk.Button(self.frm, text="Rejouer", command=self.rejouer).pack()

        # creation de la carte
        self.liste_segments, self.liste_points, self.emplacement_victoire,\
            self.emplacements_gardiens, self.emplacements_lampes,\
            self.emplacements_boutons,\
            self.emplacements_tableaux = generateur(self.cnv, 0)
        self.in_game = True

        # initialisation de variables
        self.liste_tableaux = list()
        self.liste_gardiens = list()
        self.liste_boutons = list()
        self.liste_lampes = list()

        # Création des tableaux
        self.nb_tableaux = len(self.emplacements_tableaux)
        for i in range(self.nb_tableaux):
            self.liste_tableaux.append(
                Tableau(Point(self.emplacements_tableaux[i][0],
                              self.emplacements_tableaux[i][1]),
                        self.cnv, i))

        # Création des gardiens
        for i in range(len(self.emplacements_gardiens)):
            self.liste_gardiens.append(
                Gardien(Point(self.emplacements_gardiens[i][0],
                              self.emplacements_gardiens[i][1]),
                        self.emplacements_gardiens[i][2],
                        100,
                        i,
                        self,
                        self.emplacements_gardiens[i][3],
                        self.emplacements_gardiens[i][4]))

        # Création des lampes et des boutons
        for i in range(len(self.emplacements_lampes)):
            self.liste_lampes.append(
                Lampe(Point(self.emplacements_lampes[i][0],
                            self.emplacements_lampes[i][1]),
                      self.emplacements_lampes[i][2], i, self))

            self.liste_boutons.append(
                Bouton(Point(self.emplacements_boutons[i][0],
                             self.emplacements_boutons[i][1]),
                       self.liste_lampes[i], self.cnv, i))

        # Création du voleur
        self.voleur = Voleur(Point(self.emplacement_victoire[0],
                             self.emplacement_victoire[1]), self)

        # lancement de l'animation des gardiens
        for gardien in self.liste_gardiens:
            gardien.agir()

        # liaison des actions de deplacement avec les flèches directionnelles
        self.wnd.bind("<Up>", lambda event: self.voleur.avancer(event))
        self.wnd.bind("<Down>", lambda event: self.voleur.reculer(event))
        self.wnd.bind("<Right>", lambda event: self.voleur.droite(event))
        self.wnd.bind("<Left>", lambda event: self.voleur.gauche(event))
        self.wnd.bind("<e>", lambda event: self.voleur.interagir(event))

        self.wnd.mainloop()

    def rejouer(self):
        """
        Permet de stopper le jeu et de relancer une partie
        """
        if not self.in_game:
            self.wnd.destroy()
            self.__init__(self.width_canvas, self.height_canvas)


if __name__ == '__main__':
    Application(600, 400)
