# -*- coding: utf-8 -*-
"""
Projet maths-info - Galerie d'art

Groupe 12 : MEYNIEL Arthur, FOUCHÉ Hugo, BOUY Hugo
"""

from shared import Point, Segment, signe,\
    point_appartient_segment, point_egaux, intersection_demi_droite_segment

# Taille des point affichés sur le canvas
size = 4


def point_in_polygon(point_to_check, polygon, canvas=None, mode_demo=False):
    """Arguments :
        - point_to_check : Tuple ou liste sous la forme (x, y) ou [x, y]
        - polygon : Liste de sommets sous la forme [[xA, yA], [xB, yB] ...]
        - canvas : Canvas de dessin
        - mode_demo : Boolean, True pour activer le mode de démonstration
    Retourne True si 'point_to_check' se trouve à l'intérieur de
    'polygon'. False sinon (segments et sommets du polygon sont considérés
    comme à l'extérieur')
    Retourne None en cas d'erreur"""

    if mode_demo:
        canvas.delete("demo")
        # Récupération des informations de la fenêtre
        width = canvas.winfo_width()

    liste_segments_polygon = list()
    # Création d'une liste contenant les segments du polygon
    if not (type(point_to_check) is tuple or type(point_to_check) is list):
        A = point_to_check
        for i in range(1, len(polygon)):
            B = polygon[i]
            liste_segments_polygon.append(Segment(A, B))
            A = B
        B = polygon[0]
        liste_segments_polygon.append(Segment(A, B))
        # Le point 0 dans tout l'algorithme correspond au point
        # dont nous souhaitons savoir si il est dans le poylgon
        O = point_to_check
    else:
        A = Point(polygon[0][0], polygon[0][1])
        for i in range(1, len(polygon)):
            B = Point(polygon[i][0], polygon[i][1])
            liste_segments_polygon.append(Segment(A, B))
            A = B
        B = Point(polygon[0][0], polygon[0][1])
        liste_segments_polygon.append(Segment(A, B))

        # Le point 0 dans tout l'algorithme correspond au point
        # dont nous souhaitons savoir si il est dans le poylgon
        O = Point(point_to_check[0], point_to_check[1])

    # Cette fonction se base sur l'algorithme présenté dans cet article
    # https://towardsdatascience.com/is-the-point-inside-the-polygon-574b86472119

    # Winding number
    wn = 0
    # A et B : points définissants le segment horizontal de référence
    # Possèdent la même hauteur que O
    A = Point(0, O.y)
    B = Point(O.x, O.y)
    segment_horizontal = Segment(A, B)

    if mode_demo:
        canvas.create_oval(O.x - size, O.y - size, O.x + size, O.y + size,
                           fill='green', tag='demo')
        canvas.create_line((0, O.y), (width, O.y), fill='red', tag='demo')

    # Liste contenant les coordonnées des points d'intersections de la droite
    # horizontale avec les segments du polygon
    liste_intersections = list()

    # On parcours la liste des segments du polygon
    for segment in liste_segments_polygon:
        # Si le point appartient à un segment du polygon, il n'est donc pas
        # considéré comme appartenant au polygon

        if point_appartient_segment(O, segment):
            return False
        I = intersection_demi_droite_segment(segment_horizontal, segment)

        # Différents cas possibles

        # Si les deux segments sont alignés
        if I == "Infinite":
            # On considère les deux extrémités du segments comme deux
            # points d'intersection
            liste_intersections.append([segment.A, segment])
            liste_intersections.append([segment.B, segment])

        # Si un point d'intersection a été trouvé
        elif I is not None:
            liste_intersections.append([I, segment])
    # Un fois toutes les intersections trouvés, on les passe en revue une
    # par une
    i = 0
    while i < len(liste_intersections):
        intersection = liste_intersections[i][0]
        # Vecteur directeur du segment où se trouve l'intersection
        # Par similitude, on se permet de l'assimiler à une classe point
        u = Point(liste_intersections[i][1].B.x -
                  liste_intersections[i][1].A.x,
                  liste_intersections[i][1].B.y -
                  liste_intersections[i][1].A.y)
        # Dans le cas de la dernière intersection, il faut vérifier avec
        # la première
        if i == len(liste_intersections) - 1:
            indice = 0
        else:
            indice = i + 1
        ignore = False
        # Si l'intersection est un sommet
        if point_egaux(intersection, liste_intersections[indice][0]):
            if mode_demo:
                canvas.create_oval(intersection.x - size,
                                   intersection.y - size,
                                   intersection.x + size,
                                   intersection.y + size,
                                   fill='blue', tag='demo')
            v = Point(liste_intersections[indice][1].B.x -
                      liste_intersections[indice][1].A.x,
                      liste_intersections[indice][1].B.y -
                      liste_intersections[indice][1].A.y)
            # Si l'intersection n'est pas une entrée ou sortie du polygone
            # (une pointe par exemple), elle doit être ignoré
            # Les deux premiers if sont les cas où l'un des segments est
            # horizontal
            if signe(u.y) == 0:
                if signe(v.y) == 0 or signe(v.y) == 1:
                    ignore = True
            elif signe(v.y) == 0:
                if signe(u.y) == -1:
                    ignore = True
            elif signe(v.y) != signe(u.y):
                ignore = True
            # Dans tous les cas, on ignore l'indice suivant (étant une nouvelle
            # fois le sommet)
            i += 1
            # Si on est rendu au dernier indice, on quitte la boucle
            if i == len(liste_intersections):
                continue
        elif mode_demo:
            canvas.create_oval(intersection.x - size, intersection.y - size,
                               intersection.x + size, intersection.y + size,
                               fill='red', tag='demo')
        # Si l'intersection ne doit pas être ignorée
        result = 0
        if not ignore:
            # On met à jour le winding number
            if u.y < 1:
                # Croisement vers le haut
                if intersection.x > O.x:
                    wn += 1
                    result = 1
            else:
                # Croisement vers le bas
                if intersection.x > O.x:
                    wn -= 1
                    result = -1
        if mode_demo:
            canvas.create_text(intersection.x, intersection.y + 10,
                               text=result, tag='demo')
        i += 1
    if wn != 0:
        return True
    return False
