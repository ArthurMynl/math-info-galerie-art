# -*- coding: utf-8 -*-
"""
Projet maths-info - Galerie d'art

Groupe 12 : MEYNIEL Arthur, FOUCHÉ Hugo, BOUY Hugo
"""

from shared import Point, Segment
import random


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
                 (219, 124)],
                [(217, 119), (165, 93), (160, 47), (207, 15), (282, 15),
                (314, 40), (314, 84), (277, 117), (277, 141), (330, 140),
                (419, 32), (475, 26), (474, 16), (563, 17), (566, 113),
                (523, 113), (522, 207), (588, 324), (458, 328), (478, 292),
                (428, 231), (342, 229), (341, 330), (242, 329), (186, 281),
                (106, 277), (63, 242), (57, 163), (24, 122), (22, 73),
                (60, 34), (102, 34), (126, 61), (124, 102), (102, 120),
                (96, 153), (97, 225), (127, 235), (175, 234), (207, 200),
                (335, 177), (337, 196), (425, 192), (459, 205), (493, 252),
                (495, 207), (490, 117), (469, 118), (472, 56), (426, 64),
                (340, 160), (280, 165), (215, 165)]]

    database_victoire = [(156, 153), (77, 63)]

    database_gardiens = [[(322, 230, 90, "ronde", 50),
                          (75, 246, 225, "toupie", 0)],
                         [(268, 263, 90, "toupie", 0),
                          (511, 248, 90, "ronde", 175),
                          (243, 77, 90, "toupie", 0)]]

    database_lampes = [[(291, 45, 40)],
                       [(579, 318, 100)]]

    database_boutons = [[(152, 328)],
                        [(244, 325)]]

    database_tableaux = [[(146, 273), (369, 37), (100, 395), (505, 314),
                          (537, 40)],
                         [(208, 204), (522, 284), (561, 64), (243, 71)]]

    if numero_predefini is None:
        numero_predefini = random.randint(0, len(database) - 1)

    canvas.delete('all')

    transformed_database = list()
    for elem in database[numero_predefini]:
        transformed_database.append(Point(elem[0], elem[1]))

    # memorisation des segments
    liste_segments = list()
    for i in range(1, len(transformed_database)):
        A = transformed_database[i]
        B = transformed_database[i - 1]
        liste_segments.append(Segment(A, B))
    A = transformed_database[0]
    B = transformed_database[-1]
    liste_segments.append(Segment(A, B))

    # dessiner le polygone
    canvas.create_polygon(database[numero_predefini], fill='grey')
    canvas.create_rectangle(database_victoire[numero_predefini][0] - 5,
                            database_victoire[numero_predefini][1] - 5,
                            database_victoire[numero_predefini][0] + 5,
                            database_victoire[numero_predefini][1] + 5,
                            fill="red")

    return (liste_segments, database[numero_predefini],
            database_victoire[numero_predefini],
            database_gardiens[numero_predefini],
            database_lampes[numero_predefini],
            database_boutons[numero_predefini],
            database_tableaux[numero_predefini])
