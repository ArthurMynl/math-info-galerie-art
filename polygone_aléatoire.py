# -*- coding: utf-8 -*-
"""
Projet maths-info - Galerie d'art

Groupe 12 : MEYNIEL Arthur, FOUCHÉ Hugo, BOUY Hugo
"""

from shared import Point, Segment, angle_deux_points
from point_in_polygon import point_in_polygon
import random


def polygone_aleatoire(nombre_de_points, canvas):
    """
    Arguments :
        - nombre_de_points : si None, le polygone à un nombre de points
                             aleatoire compris entre 3 et 50 sinon,
                             le polygone à un nombre defini de points
        - canvas : objet de type tkinter.Canvas dans lequel le polygone sera
                   dessiné
    Affiche :
        - un polygone connexe avec le nombre de points pris en argument
    Retourne :
        - Une liste d'objets de type 'segment' dans leur ordre d'apparition
    """

    liste_points, random_polygon, liste_points_tuple = [], [], []
    sommets_polygon, liste_segments = [], []

    width = canvas.winfo_width() - 6    # correction d'un comportement étrange
    height = canvas.winfo_height() - 6  # correction d'un comportement étrange

    canvas.delete('all')

    if nombre_de_points is None:
        nombre_de_points = random.randint(3, 50)

    for i in range(nombre_de_points):
        liste_points.append(Point(random.randint(1, width - 1),
                                  random.randint(1, height - 1)))
    for point in liste_points:
        liste_points_tuple.append(point.return_tuple())

    # centre du canvas
    C = Point(width // 2, height // 2)

    for point in liste_points:
        random_polygon.append(((angle_deux_points(point, C)), point))

    random_polygon.sort()
    for elem in random_polygon:
        sommets_polygon.append(elem[1])

    # memorisation des segments
    for i in range(1, len(sommets_polygon)):
        A = sommets_polygon[i]
        B = sommets_polygon[i - 1]
        liste_segments.append(Segment(A, B))
    A = sommets_polygon[0]
    B = sommets_polygon[-1]
    liste_segments.append(Segment(A, B))

    if not point_in_polygon(C.return_tuple(), liste_points_tuple, canvas):
        polygone_aleatoire(nombre_de_points, canvas)

    # changement du type des données
    sommets_tuple = list()
    for elem in sommets_polygon:
        sommets_tuple.append(elem.return_tuple())

    # dessiner le polygone
    canvas.create_polygon(sommets_tuple, fill='grey')

    return liste_segments, sommets_tuple
