# -*- coding: utf-8 -*-
"""
Projet maths-info - Galerie d'art

Groupe 12 : MEYNIEL Arthur, FOUCHÉ Hugo, BOUY Hugo
"""


from shared import (angle_deux_points, determinant_3_points, dist, sc,
                    Point, Segment, intersection_segments,
                    point_appartient_segment)
import math

arrondi_angle = 4
arrondi_segment = 1


def calcul_intersections(centre, rayon, seg):
    """
    Renvoie les deux intersections entre la droite donnée par les points
    du segment seg et le cercle sous forme d'objet Point

    Arguments :
        - event : évenement, permet de récupérer la position de la souris

    Retourne
        - G1 et G2 : Intersections entre la droite correspondant au segment
                     et le cercle. G1 et G2 objets de type Point
        - (None, None) : Si il n'y a pas de points d'intersections entre
                         la droite et le cercle

    """

    A = seg.A
    B = seg.B
    ASB = determinant_3_points(A, centre, B)
    AB = dist(A, B)
    d = abs(ASB) / AB
    '''d étant la distance la plus proche entre le cercle et la droite AB
    si d est inférieure au rayon, il n'y a pas d'intersections possible'''
    if d < rayon:
        # Calcul à l'aide de la formule prouvée
        vAB = (B.x - A.x, B.y - A.y)
        vAS = (centre.x - A.x, centre.y - A.y)
        h = sc(vAS, vAB) / (AB**2)
        t = math.sqrt(rayon**2 - d**2) / AB

        # 1er point d'intersection
        a = 1 - h - t
        b = h + t
        xAG1 = (a * A.x + b * B.x)
        yAG1 = (a * A.y + b * B.y)

        # 2eme point
        a = 1 - h + t
        b = h - t
        xAG2 = (a * A.x + b * B.x)
        yAG2 = (a * A.y + b * B.y)

        return Point(xAG1, yAG1), Point(xAG2, yAG2)
    return None, None


def clip(cnv, proj1, proj2, centre, rayon, liste_segments):
    """
    Efface la partie à effacer lors du clipping et affiche le triangle de
    lumière à afficher par dessus
    """

    # Suppression des effets de clipping déjà existants
    cnv.delete("clip1")
    cnv.delete("clip2")
    cnv.delete("point")

    # Récupération des angles correspondants aux extrémités de la projection
    # lumineuse
    angle_proj1 = -angle_deux_points(proj1, centre, True)
    angle_proj2 = -angle_deux_points(proj2, centre, True)

    # Initialisation des variables et des listes
    nb_seg = len(liste_segments)
    A = list()
    angle_A = list()
    B = list()
    angle_B = list()
    inter1 = list()
    inter2 = list()
    angle_inter1 = list()
    angle_inter2 = list()

    for i in range(nb_seg):
        A.append(liste_segments[i].A)
        B.append(liste_segments[i].B)
        angle_A.append(None)
        angle_B.append(None)
        inter1.append(None)
        inter2.append(None)
        angle_inter1.append(None)
        angle_inter2.append(None)

    # Tri des angles dans le bon ordre -> angle_proj1 doit être le premier
    if angle_proj1 < 0:
        angle_proj1 += 360

    if angle_proj2 < 0:
        angle_proj2 += 360

    # Écart des angles de la projection lumineuse, si il est supérieur à 180
    # alors c'est que la projection passe par la limite 360 - 0 degré, on se
    # servira de cette information plus tard
    ecart_proj = abs(angle_proj2 - angle_proj1)

    # Tri des segments : on trie les segments à clipper en premier en
    # fonction de la distance entre le centre du cercle et le milieu du
    # segment. Note: cette méthode n'est pas optimale, elle ne fonctionne
    # pas tout le temps mais c'est la plus efficace que nous avons trouvée
    milieu_list = list()
    for i in range(nb_seg):
        if A[i] is not None and B[i] is not None:
            milieu_list.append(dist(Point((A[i].x + B[i].x) / 2,
                                    (A[i].y + B[i].y) / 2), centre))
        else:
            # si le segment n'est pas défini, on lui donne une valeur, afin
            # de ne pas avoir de problème
            milieu_list.append(100000)

    milieu_non_trie = True

    while milieu_non_trie:
        changement = False
        for i in range(nb_seg - 1):
            if milieu_list[i] < milieu_list[i + 1]:
                milieu_list[i], milieu_list[i + 1] = \
                    milieu_list[i + 1], milieu_list[i]
                A[i], A[i + 1] = A[i + 1], A[i]
                B[i], B[i + 1] = B[i + 1], B[i]
                changement = True
        if not changement:
            milieu_non_trie = False

    # Début du clipping dans le bon ordre pour tous les segments
    for i in range(nb_seg):
        if A[i] is not None and B[i] is not None:
            # On calcule AS et BS correspondant aux distances entre A et le
            # centre du cercle et B et le centre du cercle
            AS = dist(A[i], centre)
            BS = dist(B[i], centre)
            # On définit les segments seg21 et seg22 correspondant aux
            # segments entre le centre du cercle et les extrémités de la
            # projection lumineuse
            seg21 = Segment(proj1, centre)
            seg22 = Segment(proj2, centre)
            # On récupère les angles correspondants aux points A et B
            angle_A[i] = -angle_deux_points(A[i], centre, True)
            angle_B[i] = -angle_deux_points(B[i], centre, True)

            if angle_A[i] < 0:
                angle_A[i] += 360

            if angle_B[i] < 0:
                angle_B[i] += 360
            # On trie A et B afin que A soit placé avant B dans la rotation
            # autour du cercle. C'est-à-dire que lorsque l'on tourne dans le
            # sens trigonométrique, on verra toujours A avant B
            if angle_A[i] > angle_B[i]:
                A[i], B[i] = B[i], A[i]
                angle_A[i], angle_B[i] = \
                    angle_B[i], angle_A[i]
                AS, BS = BS, AS
            # On récupère l'écart en degré entre les angles de A et B, afin
            # de savoir si l'on doit les inverser (on les inverse si passe
            # par la limite 360 - 0 degrés)
            ecart_AB = abs(angle_B[i] - angle_A[i])
            if ecart_AB >= 180:
                angle_A[i], angle_B[i] = \
                    angle_B[i], angle_A[i]
                A[i], B[i] = B[i], A[i]
                AS, BS = BS, AS

            # On récupère les intersections entre la droite AB et le cercle
            # s'il n'y en a pas alors la droite AB ne passe pas par le
            # cercle et par conséquent le segment AB non plus, s'il n'y en
            # a pas alors pas besoin de faire le clipping.
            inter1[i], inter2[i] = calcul_intersections(centre, rayon,
                                                        Segment(A[i], B[i]))
            if inter1[i] is not None:
                # On récupère les angles correspondant aux intersections
                # entre la droite AB et le cercle, puis on les trie de
                # la même manière que pour A et B
                angle_inter1[i] = \
                    -angle_deux_points(inter1[i], centre, True)
                if angle_inter1[i] < 0:
                    angle_inter1[i] += 360

                angle_inter2[i] = \
                    -angle_deux_points(inter2[i], centre, True)
                if angle_inter2[i] < 0:
                    angle_inter2[i] += 360

                if angle_inter1[i] > angle_inter2[i]:
                    inter1[i], inter2[i] = inter2[i], \
                        inter1[i]
                    angle_inter1[i], angle_inter2[i] = \
                        angle_inter2[i], angle_inter1[i]

                # On récupère l'écart entre les angles de chaque
                # intersections, si l'écart est supérieur à 180 alors
                # l'écart des angles passe par la limite 360 - 0 degré, on
                # inverse alors inter1 et inter2 dans ce cas
                ecart = \
                    abs(angle_inter2[i] - angle_inter1[i])
                if ecart >= 180:
                    angle_inter2[i], angle_inter1[i] = \
                        angle_inter1[i], angle_inter2[i]
                    inter1[i], inter2[i] = \
                        inter2[i], inter1[i]
                segAB = Segment(A[i], B[i])

                # On teste s'il faut clip : il faut que soit le segment AB
                # soit dans le cercle (condition 1)
                # ou alors il faut que le segment AB passe par le cercle:
                # on regarde les intersections, si elles existent alors on
                # on vérifie qu'elles passent bien par la cone de lumière
                if BS < rayon or AS < rayon\
                    or (BS > rayon and AS > rayon
                        and (angle_inter2[i] < angle_proj2
                             or angle_inter1[i] > angle_proj1)
                        and (point_appartient_segment(inter1[i], segAB)
                             or point_appartient_segment(inter2[i], segAB)))\
                    or (BS > rayon and AS > rayon
                        and ecart_proj > 180
                        and ((angle_inter1[i] < angle_proj2
                              and point_appartient_segment(inter1[i], segAB))
                             or (angle_inter2[i] > angle_proj1
                                 and point_appartient_segment(inter2[i],
                                                              segAB)))):

                    clip = True

                    # Malgré la condition précédente, par test, on a
                    # remarqué que dans certains cas, le clipping se
                    # produisait quand même. L'étape suivante a donc été
                    # faite par tâtonnement et n'est donc surement pas
                    # optimisée. Ce qui n'a pas été fait par manque de temps
                    # Tous les tests suivants visent à annuler le clipping
                    # quand nécessaire.
                    if abs(BS - rayon) <= arrondi_segment \
                        and AS > rayon \
                        and intersection_segments(seg21, segAB) is None \
                        and intersection_segments(seg22, segAB) is None\
                        and angle_inter1[i] < angle_proj1\
                            and angle_inter2[i] > angle_proj2:

                        clip = False
                    if abs(AS - rayon) <= arrondi_segment \
                        and BS > rayon \
                        and intersection_segments(seg22, segAB) is None \
                        and intersection_segments(seg21, segAB) is None\
                        and angle_inter1[i] < angle_proj1\
                            and angle_inter2[i] > angle_proj2:

                        clip = False

                    if ecart_proj < 180 \
                        and intersection_segments(seg21, segAB) is None \
                        and intersection_segments(seg22, segAB) is None\
                        and ecart < 180\
                        and angle_inter1[i] > angle_proj2\
                            and angle_inter2[i] > angle_proj2:

                        clip = False
                    if ecart_proj > 180 \
                        and angle_inter2[i] < angle_proj1 \
                        and angle_inter1[i] > angle_proj2 \
                        and BS > rayon and ecart < 180 \
                            and angle_A[i] < angle_proj1:

                        clip = False

                    if ecart_proj < 180 \
                        and angle_B[i] > angle_proj1 \
                        and angle_A[i] > angle_proj2 \
                        and ecart_AB > 180 \
                        and angle_inter2[i] < angle_proj1\
                            and angle_inter1[i] > angle_proj2:

                        clip = False

                    if ecart_proj < 180 \
                        and angle_B[i] < angle_proj1 \
                        and angle_A[i] < angle_proj2 \
                        and ecart_AB > 180 \
                        and angle_inter2[i] < angle_proj1\
                            and angle_inter1[i] > angle_proj2:

                        clip = False

                    if ecart_proj < 180 \
                        and angle_B[i] > angle_proj2 \
                        and angle_A[i] < angle_proj2 \
                        and ecart_AB < 180 \
                        and angle_inter2[i] < angle_proj1\
                            and angle_inter1[i] > angle_proj2:

                        clip = False

                    if ecart_proj < 180 \
                        and angle_B[i] > angle_proj1 \
                        and angle_A[i] < angle_proj1 \
                        and ecart_AB < 180 \
                        and angle_inter2[i] < angle_proj1\
                            and angle_inter1[i] > angle_proj2:

                        clip = False

                    # Lorsque le clipping doit être fait, comme AB est un
                    # segment, il ne fait pas effacer plus que le nécessaire
                    # les conditions suivantes modifient les valeurs de
                    # inter1 et inter2 afin que la plus petite partie
                    # possible ne soit effacée
                    if ecart_proj < 180 and ecart < 180:
                        # Lorsqu'il n'y a pas de problèmes aux niveau de la
                        # limite 180-0 degré alors si B est contenu dans la
                        # projection lumineuse, on remplace inter2 par B
                        if angle_B[i] < angle_proj2 \
                            and angle_B[i] < angle_inter2[i] \
                                and BS < rayon:

                            inter2[i] = B[i]
                            angle_inter2[i] = angle_B[i]

                        # De même avec A, si A est dans la projection
                        # lumineuse, on remplace inter1 par A
                        if angle_A[i] > angle_proj1 \
                            and angle_A[i] > angle_inter1[i] \
                                and AS < rayon:

                            inter1[i] = A[i]
                            angle_inter1[i] = angle_A[i]
                    # Les conditions suivantes sont basées sur le même
                    # objectif, si A ou B est contenu dans la projection
                    # lumineuse, on remplace inter1 et/ou inter2 par
                    # A et/ou inter2.
                    elif ecart_proj < 180 and ecart >= 180:
                        if angle_B[i] < angle_proj2 \
                            and angle_B[i] < angle_inter2[i] \
                                and BS < rayon:

                            inter2[i] = B[i]
                            angle_inter2[i] = angle_B[i]

                        if angle_B[i] < angle_proj2 \
                            and angle_B[i] > angle_inter2[i] \
                            and angle_inter2[i] < angle_proj1\
                                and BS < rayon:

                            inter2[i] = B[i]
                            angle_inter2[i] = angle_B[i]

                        if angle_A[i] > angle_proj1 \
                            and angle_A[i] > angle_inter1[i] \
                                and AS < rayon:

                            inter1[i] = A[i]
                            angle_inter1[i] = angle_A[i]

                        if angle_A[i] > angle_proj1 \
                            and angle_A[i] < angle_inter1[i] \
                            and angle_inter1[i] > angle_proj2\
                                and AS < rayon:

                            inter1[i] = A[i]
                            angle_inter1[i] = angle_A[i]

                    if ecart_proj >= 180 and ecart < 180:
                        if angle_B[i] < angle_inter2[i] \
                                and BS < rayon:
                            inter2[i] = B[i]
                            angle_inter2[i] = angle_B[i]

                        if angle_A[i] > angle_proj1 \
                            and angle_A[i] > angle_inter1[i] \
                                and AS < rayon:

                            inter1[i] = A[i]
                            angle_inter1[i] = angle_A[i]

                        if angle_A[i] < angle_proj2 \
                                and AS < rayon:

                            inter1[i] = A[i]
                            angle_inter1[i] = angle_A[i]

                    if ecart_proj >= 180 and ecart >= 180:
                        if angle_B[i] < angle_proj2 \
                            and angle_B[i] < angle_inter2[i] \
                                and BS < rayon:

                            inter2[i] = B[i]
                            angle_inter2[i] = angle_B[i]

                        if angle_B[i] > angle_proj2 \
                            and angle_B[i] > angle_inter2[i] \
                            and angle_B[i] > angle_proj1\
                                and BS < rayon:

                            inter2[i] = B[i]
                            angle_inter2[i] = angle_B[i]

                        if angle_A[i] > angle_proj1 \
                            and angle_A[i] > angle_inter1[i] \
                                and AS < rayon:

                            inter1[i] = A[i]
                            angle_inter1[i] = angle_A[i]

                        if angle_A[i] < angle_proj1 \
                            and angle_A[i] < angle_inter1[i] \
                            and angle_A[i] < angle_proj2\
                                and AS < rayon:

                            inter1[i] = A[i]
                            angle_inter1[i] = angle_A[i]

                    # Comme précédemment, par test, on a
                    # remarqué que dans certains cas, le clipping se
                    # produisait quand même. L'étape suivante a donc été
                    # aussi faite par tâtonnement et n'est donc pas
                    # optimisée. Ce qui n'a pas été fait par manque de temps
                    # Tous les tests suivants visent à annuler le clipping
                    # quand nécessaire.
                    if ecart_proj < 180 \
                        and angle_B[i] < angle_proj1 \
                        and angle_A[i] < angle_proj1 \
                            and ecart_AB < 180:

                        clip = False
                    if ecart_proj < 180 \
                        and angle_B[i] > angle_proj2 \
                        and angle_A[i] > angle_proj2 \
                            and ecart_AB < 180:

                        clip = False
                    if ecart_proj < 180 \
                        and angle_B[i] < angle_proj1 \
                        and angle_A[i] > angle_proj2 \
                            and ecart_AB > 180:

                        clip = False
                    if ecart_proj > 180 \
                        and angle_B[i] > angle_proj2 \
                        and angle_A[i] > angle_proj2 \
                        and ecart_AB < 180\
                            and angle_B[i] < angle_proj1:

                        clip = False

                    if ecart_proj < 180 \
                        and angle_inter1[i] < angle_proj1 \
                        and angle_inter2[i] < angle_proj1 \
                            and ecart < 180:

                        clip = False

                    if abs(angle_A[i] - angle_B[i])\
                        <= arrondi_angle \
                            and angle_A[i]:

                        clip = False

                    # Quand tous les tests du clipping on été validé,
                    # on cherche s'il y a une intersection entre le segment
                    # correspondant à celui créé par inter1 et inter2 et un
                    # des segments correspondant aux extrêmités des
                    # projections du cône de lumière
                    if clip:
                        seg1 = Segment(inter1[i], inter2[i])

                        int1p = intersection_segments(seg1, seg21)
                        int2p = intersection_segments(seg1, seg22)

                        # Si les intersections ne sont pas comprisent dans
                        # la projection lumineuse, on les projette sur un
                        # des segments extrêmes de la projection
                        # lumineuse. Toutes les conditions suivantes ont
                        # cet objectif
                        if ecart_proj < 180 and ecart < 180:
                            if angle_proj1 > angle_inter1[i] \
                                    and int1p is not None:

                                angle_inter1[i] = angle_proj1
                                inter1[i] = int1p

                            if angle_proj2 < angle_inter2[i] \
                                    and int2p is not None:

                                angle_inter2[i] = angle_proj2
                                inter2[i] = int2p

                        if ecart_proj < 180 and ecart >= 180:
                            if angle_proj1 > angle_inter1[i] \
                                and angle_inter1[i] < \
                                    angle_proj2 and int1p is not None:

                                angle_inter1[i] = angle_proj1
                                inter1[i] = int1p

                            if angle_proj1 < angle_inter1[i] \
                                and angle_inter1[i] > \
                                    angle_proj2 and int1p is not None:

                                angle_inter1[i] = angle_proj1
                                inter1[i] = int1p

                            if angle_proj2 < angle_inter2[i] \
                                and angle_inter2[i] > \
                                    angle_proj1 and int2p is not None:

                                angle_inter2[i] = angle_proj2
                                inter2[i] = int2p

                            if angle_proj2 > angle_inter2[i] \
                                and angle_inter2[i] < \
                                    angle_proj1 and int2p is not None:

                                angle_inter2[i] = angle_proj2
                                inter2[i] = int2p

                        if ecart_proj > 180 and ecart < 180:
                            if angle_proj2 < angle_inter2[i] \
                                and angle_inter2[i] < \
                                    angle_proj1 and int2p is not None:

                                angle_inter2[i] = angle_proj2
                                inter2[i] = int2p

                            if angle_proj1 > angle_inter1[i] \
                                and angle_inter1[i] > \
                                    angle_proj2 and int1p is not None:

                                angle_inter1[i] = angle_proj1
                                inter1[i] = int1p

                        if ecart_proj > 180 and ecart > 180:
                            if angle_proj1 > angle_inter1[i] \
                                and angle_inter1[i] > \
                                    angle_proj2 and int1p is not None:

                                angle_inter1[i] = angle_proj1
                                inter1[i] = int1p

                            if angle_proj2 < angle_inter2[i] \
                                and angle_inter2[i] < \
                                    angle_proj1 and int2p is not None:

                                angle_inter2[i] = angle_proj2
                                inter2[i] = int2p

                        # Afin d'effacer une partie de l'arc lumineux, on
                        # doit connaitre, l'angle de départ et un angle à
                        # effacer à partir du départ. On calcule diff,
                        # l'angle à effacer à partir du départ: celui de
                        # inter1
                        diff = abs(angle_inter2[i] -
                                   angle_inter1[i])

                        if diff >= 180:
                            diff = abs(360 - angle_inter1[i]
                                       + angle_inter2[i])
                        if diff >= 1:
                            # Afin d'éviter des problèmes, si l'angle est
                            # plus petit que 1, pas besoin de faire le
                            # clipping, on ne le verrait pas à l'oeil nu
                            # Ensuite, on efface l'arc à effacer et on
                            # trace le polygone à afficher par dessus.
                            cnv.create_arc(centre.x - rayon,
                                           centre.y - rayon,
                                           centre.x + rayon,
                                           centre.y + rayon,
                                           fill="white",
                                           tag="clip1",
                                           start=angle_inter1[i],
                                           extent=diff,
                                           outline="white")

                            cnv.create_polygon(centre.return_tuple(),
                                               inter1[i].return_tuple(),
                                               inter2[i].return_tuple(),
                                               fill="yellow",
                                               outline="yellow",
                                               tag="clip2")
