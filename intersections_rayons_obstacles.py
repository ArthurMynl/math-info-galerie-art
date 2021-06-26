# -*- coding: utf-8 -*-
"""
Projet maths-info - Galerie d'art

Groupe 12 : MEYNIEL Arthur, FOUCHÉ Hugo, BOUY Hugo
"""

from shared import Point, Segment,\
    intersection_demi_droite_segment, dist, rotation


def intersections_rayons_obstacles(canvas, point, nombre_rayons, angle_de_vue,
                                   direction, segments_verifs, demo=False,
                                   return_inter=False):
    """
    Arguments :
        - canvas : objet de type tkinter.Canvas dans lequel le polygone sera
                   dessiné
        - point : objet de classe 'Point'
        - nombre_rayons : integer, nombre de rayons projetés
        - angle_de_vue : integer, angle en degrés du projeté (360 = cercle)
        - direction : integer, en degrés suivant le cercle trigonometrique
        - segments_verifs : liste d'objets de classe 'segment', representant le
        obstacles ou murs du polygone
        - demo : affiche les points d'intersection pour le debug
    Affiche :
        - les points d'intersection si demo=True
        - les rayons de lumière
        - le gardien (surement à supprimer dans le futur)
    """

    # Taille des points d'intersection
    size = 4

    # Angle pour la rotation
    angle = angle_de_vue / nombre_rayons

    # Suppression de la précédente source lumineuse
    canvas.delete('light')

    # La fonction va chercher une intersection avec les segments
    # renseignés dans segments_verifs et le segment [pointB]. Celui-ci
    # de longeur 1 est le départ des rayons de la source

    # besoin de faire un changement pour avoir la mesure en degres entre A et
    # le placement de B.
    B = Point(point.x + 1, point.y)
    B = rotation(point, B, direction - angle_de_vue / 2)

    liste_inter = []

    # Pour le nombre de rayon demandés
    for i in range(nombre_rayons):
        # On cherche toutes les intersections avec les segments renseignés
        inter = []
        rayon_lumiere = Segment(point, B)
        for segment in segments_verifs:
            I = intersection_demi_droite_segment(rayon_lumiere, segment)
            # Si il y a un point d'intersection
            if I is not None:
                # On l'ajoute à la liste
                inter.append([dist(I, point), I])
        # Si aucun point d'intersection n'est trouvé
        if inter:
            # On cherche le point d'intersection le plus proche du point A
            I_p = min(inter)
            I = I_p[1]
            liste_inter.append(I)
            # Si le mode de demo est activé on dessine ce point
            # d'intersection
            if demo:
                if inter.count(I_p) > 1:
                    color = 'green'
                    canvas.create_oval(I.x - size, I.y - size, I.x + size,
                                       I.y + size, fill=color, tag='light')
                else:
                    color = 'red'
                    canvas.create_oval(I.x - size, I.y - size, I.x + size,
                                       I.y + size, fill=color, tag='light')

            if not return_inter:
                # Affichage de la source lumineuse en jaune
                canvas.create_oval(point.x - size, point.y - size, point.x +
                                   size, point.y + size, fill='yellow',
                                   tag='light')
                # Dans tous les cas on dessine le rayon lumineux jusqu'au
                # point d'intersection
                canvas.create_line(point.return_tuple(), I.return_tuple(),
                                   fill='yellow', tag='light')
        # On passe au rayon suivant en effectuant une rotation du point B
        B = rotation(point, B, angle)

    if return_inter:
        return liste_inter
