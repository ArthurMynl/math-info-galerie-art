# -*- coding: utf-8 -*-
"""
Projet maths-info - Galerie d'art

Groupe 12 : MEYNIEL Arthur, FOUCHÉ Hugo, BOUY Hugo
"""

import tkinter as tk
import random
import math
from shared import Point, Segment, determinant_3_points, sc,\
    angle_deux_points, rotation, dist
from clipping import clip
from point_in_polygon import point_in_polygon


def generateur(canvas, numero_predefini):
    """
    Arguments :
        - canvas : objet de type tkinter.Canvas dans lequel le polygone sera
                   dessiné
        - numero_preset : integer definissant quel polygone sera dessiné,
                          si il est egal à None la dataset sera selectionée
                          aleatoirement
    Affiche :
        - Un polygone predefini en fonction du numero_predefini
    Retourne :
        - Une liste de tous les segments du polygone
    """

    database = [[(221, 183), (221, 221), (90, 223), (91, 109),
                (140, 106), (143, 168), (173, 168), (176, 70),
                (46, 65), (50, 276), (223, 274), (225, 321),
                (81, 330), (82, 403), (116, 400), (112, 359),
                (224, 357), (275, 356), (272, 317), (415, 315),
                (415, 277), (481, 272), (482, 316), (530, 315),
                (528, 225), (413, 227), (406, 162), (463, 158),
                (460, 116), (495, 111), (496, 65), (542, 64),
                (541, 21), (456, 21), (457, 81), (416, 81),
                (416, 120), (369, 122), (319, 123), (315, 63),
                (373, 57), (372, 23), (266, 22), (272, 122),
                (219, 124)]]

    if numero_predefini is None:
        numero_predefini = random.randint(0, len(database) - 1)

    canvas.delete('all')

    transformed_database = list()
    for elem in database[numero_predefini]:
        transformed_database.append(Point(elem[0], elem[1]))

    # Memorisation des segments
    liste_segments = list()
    for i in range(1, len(transformed_database)):
        A = transformed_database[i]
        B = transformed_database[i - 1]
        liste_segments.append(Segment(A, B))
    A = transformed_database[0]
    B = transformed_database[-1]
    liste_segments.append(Segment(A, B))

    return liste_segments, database[numero_predefini]


def projection_point_cercle(centre, A, rayon):
    """

    Arguments :
        - centre : Centre du cercle de type Point
        - A : Point extérieur au cercle que l'on veut projeter dessus, de type
              Point
        - rayon : Rayon du cercle en pixel

    Retourne
        - G1 ou G2 : L'intersection entre la droite passant par A et le centre
                     du cercle et le cercle lui-même. L'intersection la plus
                     proche de A est renvoyée

    """

    ASB = determinant_3_points(A, centre, centre)
    AB = dist(A, centre)
    d = abs(ASB) / AB

    vAB = (centre.x - A.x, centre.y - A.y)
    vAS = (centre.x - A.x, centre.y - A.y)
    h = sc(vAS, vAB) / (AB ** 2)
    t = math.sqrt(rayon ** 2 - d ** 2) / AB

    # 1er point d'intersection
    a = 1 - h - t
    b = h + t
    xG1 = (a * A.x + b * centre.x)
    yG1 = (a * A.y + b * centre.y)

    G1 = Point(xG1, yG1)
    d1 = dist(A, G1)

    # 2eme point
    a = 1 - h + t
    b = h - t
    xG2 = (a * A.x + b * centre.x)
    yG2 = (a * A.y + b * centre.y)

    G2 = Point(xG2, yG2)
    d2 = dist(A, G2)
    """Comme le point est à l'extérieur du cercle, on prend l'intersection
    avec la distance la plus faible"""
    if d1 > d2:
        return G2
    return G1


class Gardien:
    def __init__(self, Point, direction, angle, puissance, vitesse, taille):
        """
         Arguments :
            - Point : objet de classe 'Point' représentant la position du
                      gardien
            - direction : int representant la rotation du gardien dans le sens
                          trigonometrique
            - angle : angle d'éclairage de la lampe torche
            - puissance : distance d'éclairage de la lampe torche
            - vitesse : int representant la vitesse de deplacement du gardien
            - cnv : objet de type tkinter.Canvas dans lequel le polygone sera
                    dessiné
            - taille : taille en pixel du point représentant le voleur
            - id : int représentant le numero d'identification du gardien
            - couleur : String contenant le code couleur tkinter
        """
        self.position = Point  # Position en pixels
        self.direction = direction  # En degrés
        self.angle = angle  # En degrés
        self.puissance = puissance    # Puissance de la torche en pixels
        self.vitesse = vitesse  # Vitesse de deplacement
        cnv.create_oval(self.position.x - taille,
                        self.position.y - taille,
                        self.position.x + taille,
                        self.position.y + taille,
                        fill="red", tag='Gardien')

    def reculer(self, event, cnv):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le gardien sera
                    deplacé
        """
        rad = self.direction * math.pi / 180
        self.position.move(round(math.sin(rad - math.pi / 2) * self.vitesse),
                           round(math.cos(rad - math.pi / 2) * self.vitesse))
        if not point_in_polygon(self.position.return_tuple(), liste_points):
            self.position.move(round(math.sin(rad - math.pi / 2)
                                     * -self.vitesse),
                               round(math.cos(rad - math.pi / 2)
                                     * -self.vitesse))
        else:
            cnv.move('Gardien',
                     round(math.sin(rad - math.pi / 2) * self.vitesse),
                     round(math.cos(rad - math.pi / 2) * self.vitesse))

        self.eclaire()

    def avancer(self, event, cnv):
        """
        Arguments :
            - liste_segments : liste d'objets de type segment représentant le
                               musée
            - cnv : objet de type tkinter.Canvas dans lequel le gardien sera
                    deplacé
        """
        rad = self.direction * math.pi / 180
        self.position.move(int(math.sin(rad - math.pi / 2) * -self.vitesse),
                           int(math.cos(rad - math.pi / 2) * -self.vitesse))
        if not point_in_polygon(self.position.return_tuple(), liste_points):
            self.position.move(int(math.sin(rad - math.pi / 2)
                                   * self.vitesse),
                               int(math.cos(rad - math.pi / 2)
                                   * self.vitesse))
        else:
            cnv.move('Gardien',
                     int(math.sin(rad - math.pi / 2) * -self.vitesse),
                     int(math.cos(rad - math.pi / 2) * -self.vitesse))
        self.eclaire()

    def turn_right(self):
        """
        Permet de faire pivoter le gardien
        """
        self.direction -= 10
        if self.direction <= 0:
            self.direction = 360
        self.eclaire()

    def turn_left(self):
        """
        Permet de faire pivoter le gardien
        """
        self.direction += 10
        if self.direction >= 360:
            self.direction = 0
        self.eclaire()

    def eclaire(self):
        cnv.delete("cone")
        cnv.delete("clip1")
        cnv.delete("clip2")
        cnv.delete("cercle")

        C = Point(self.position.x + self.puissance, self.position.y)
        C = rotation(self.position, C, self.direction)
        C1 = rotation(self.position, C, -self.angle)
        C2 = rotation(self.position, C, self.angle)

        # On veut l'intersection sur le cercle
        # Projection 1
        proj1 = projection_point_cercle(self.position, C1, self.puissance)

        # Projection 2
        proj2 = projection_point_cercle(self.position, C2, self.puissance)
        # Cone de lumière
        cnv.create_arc(self.position.x - self.puissance,
                       self.position.y - self.puissance,
                       self.position.x + self.puissance,
                       self.position.y + self.puissance,
                       start=-angle_deux_points(proj1,
                                                self.position, True),
                       extent=2 * self.angle,
                       tag="cone",
                       fill="yellow", outline="yellow")
        clip(cnv, proj1, proj2, self.position, self.puissance, liste_segments)
        cnv.tag_raise("segment")


# Parametres du jeu
width_canvas, height_canvas = 600, 400
width_frame, height_frame = 100, 400

# Création de l'interface graphique
wnd = tk.Tk()
cnv = tk.Canvas(wnd, width=width_canvas, height=height_canvas, bg="white")
cnv.pack(side=tk.LEFT)
frm = tk.Frame(wnd, width=width_frame, height=height_frame)
frm.pack(side=tk.RIGHT)
liste_segments, liste_points = generateur(cnv, 0)

for segment in liste_segments:
    cnv.create_line(segment.A.x, segment.A.y, segment.B.x, segment.B.y,
                    tag="segment")
gardien1 = Gardien(Point(300, 250), 180, 30, 100, 2, 4)
gardien1.eclaire()

wnd.bind("<Up>", lambda event: gardien1.avancer(event, cnv))
wnd.bind("<Down>", lambda event: gardien1.reculer(event, cnv))
wnd.bind("<Left>", lambda event: gardien1.turn_left())
wnd.bind("<Right>", lambda event: gardien1.turn_right())

wnd.mainloop()
