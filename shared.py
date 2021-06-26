# -*- coding: utf-8 -*-
"""
Projet maths-info - Galerie d'art

Groupe 12 : MEYNIEL Arthur, FOUCHÉ Hugo, BOUY Hugo
"""

import math

# Présion demandée la validation des calculs
precision = 0.01


class Point():
    """Classe correspondant à un point"""

    def __init__(self, x, y):
        """Prend en argument les coordonées x et y du point"""
        self.x, self.y = x, y

    def __str__(self):
        string = "(" + str(self.x) + "," + str(self.y) + ")"
        return string

    def __eq__(self, other):
        return (self.x, self.y) == other

    def return_tuple(self):
        return (self.x, self.y)

    def move(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y


class Segment():
    """Classe correspondant à un segment"""

    def __init__(self, point1, point2):
        """Prend en argument deux points (de classe 'point')
        définissants un segment"""
        self.A, self.B = point1, point2

    def __str__(self):
        string = "[" + str(self.A) + "," + str(self.B) + "]"
        return string

    def return_tuple(self):
        return [self.A.return_tuple(), self.B.return_tuple()]


def det2(mat):
    """Argument :
        - mat : matrice 2*2
    Retourne le déterminant en dimension 2 de mat"""

    return(mat[0][0] * mat[1][1] - mat[1][0] * mat[0][1])


def sc(u, v):
    """Argument :
        - u, v : tupple
    Retourne le produit scalaire u.v"""

    return(u[0] * v[0] + u[1] * v[1])


def det3(mat):
    """Argument :
        - mat : matrice 3*3
    Retourne le déterminant en dimension 3 de mat"""

    a = mat[0][0] * det2([[mat[1][1], mat[1][2]], [mat[2][1], mat[2][2]]])
    b = mat[0][1] * det2([[mat[1][0], mat[1][2]], [mat[2][0], mat[2][2]]])
    c = mat[0][2] * det2([[mat[1][0], mat[1][1]], [mat[2][0], mat[2][1]]])
    return a - b + c


def dist(point1, point2):
    """Arguments :
        - point1, point2 : objets de classe 'point'
    Retourne la distance entre 'point1' et 'point2'"""

    return(math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2))


def vect(u, v):
    """Renvoie le produit vectoriel de deux vecteurs u et v passés en arguments
    en dimension 2"""
    return(u[0] * v[1] - u[1] * v[0])


def angle_deux_points(A, O, deg=False):
    """
    Arguments :
        - A : objet de classe 'Point'
        - O : objet de classe 'Point'
    Retourne :
        - L'angle en radians entre le point A et la droite horizontale
        passant par O
    """
    angle = math.atan2(A.y - O.y, A.x - O.x)
    if deg:
        return angle * 180 / math.pi
    return angle


def determinant_3_points(point1, point2, point3):
    """Arguments :
        - point1, point2, point3 : objets de classe 'point'
    Retourne le déterminant de 3 points"""

    mat = [[point1.x, point2.x, point3.x], [point1.y, point2.y, point3.y],
           [1, 1, 1]]
    return det3(mat)


def point_appartient_segment(point, segment):
    """Arguments :
        - point : objet de classe 'point'
        - segment : objet de classe 'segment'
    Retourne True si 'point' appartient à 'segment' (bornes incluses).
    False sinon"""

    if abs(determinant_3_points(point, segment.A, segment.B)) < precision:
        if abs(dist(point, segment.A) + dist(point, segment.B) -
               dist(segment.A, segment.B)) < precision:
            return True
    return False


def point_egaux(point1, point2):
    """Arguments :
        - point1, point2 : objets de classe 'point'
    Retourne True si les points sont égaux à precision près
    False sinon"""

    if abs(point1.x - point2.x) < precision and\
            abs(point1.y - point2.y) < precision:
        return True
    return False


def signe(n):
    """Argument :
        - n : Nombre dont on souhaite connaitre le signe
    Retourne 0 si n=0, 1 si n>0 ou -1 si n<0"""

    if abs(n) < precision:
        return 0
    if n > 0:
        return 1
    return -1


def intersection_droites(droite1, droite2):
    """Arguments :
        - droite1, droite2 : objet de classe 'segment'
    Retourne le point d'intersection de deux droites. None si les droites
    sont //."""

    a = determinant_3_points(droite2.A, droite2.B, droite1.B)
    b = determinant_3_points(droite2.B, droite2.A, droite1.A)

    # Si les droites sont parallèles
    if a + b == 0:
        return None

    x = (a * droite1.A.x + b * droite1.B.x) / (a + b)
    y = (a * droite1.A.y + b * droite1.B.y) / (a + b)
    I = Point(x, y)

    return I


def intersection_segments(segment1, segment2):
    """Arguments :
        - segment1, segment2 : objets de classe 'segment'
    Retourne le point d'intersection des deux segments. None si les
    deux segments n'ont pas de point d'intersection. "Infinite" si ils en ont
    une infinité"""

    a = determinant_3_points(segment2.A, segment2.B, segment1.B)
    b = determinant_3_points(segment2.B, segment2.A, segment1.A)
    # Si tous les points sont alignés
    if a == 0 and b == 0:
        # Il y a une infinité de points d'intersection
        return 'Infinite'
    # Si un des segment est nul ou si les segments sont parallèles
    if a + b == 0:
        return None
    x = (a * segment1.A.x + b * segment1.B.x) / (a + b)
    y = (a * segment1.A.y + b * segment1.B.y) / (a + b)
    I = Point(x, y)
    # Si le point d'intersection appartient aux deux segments
    if point_appartient_segment(I, segment1) and\
            point_appartient_segment(I, segment2):
        # On retourne le point d'intersection trouvé
        return I
    return None


def point_appartient_demi_droite(point, demi_droite):
    """Arguments :
        - point : objet de classe 'Point'
        - demi_droite : objet de classe 'Segment'
    Retourne True si le point appartient à la demi droite définie par
    [demi_droite.A, demi_droite.B). False sinon"""

    # Vecteurs directeurs de la demi-droite et de la demi_droite formée
    # par demi_droite.A et le point
    u = (demi_droite.B.x - demi_droite.A.x, demi_droite.B.y - demi_droite.A.y)
    v = (point.x - demi_droite.A.x, point.y - demi_droite.A.y)
    # Si les vecteurs sont colinéaires
    if abs(u[0] * v[1] - u[1] * v[0]) < precision:
        # Si ils sont colinéaires de même signe
        if signe(u[0]) == signe(v[0]) and signe(u[1]) == signe(v[1]):
            return True
    return False


def intersection_demi_droite_segment(demi_droite, segment):
    """Arguments :
        - demi_droite, segment : objet de classe 'Segment'
    Retourne le point d'intersection entre la demi_droite
    [demi_droite.A, demi_droite.B) et le segment. None si ils n'en ont pas."""

    a = determinant_3_points(demi_droite.A, demi_droite.B, segment.B)
    b = determinant_3_points(demi_droite.B, demi_droite.A, segment.A)

    # Si a=0 et b=0, alors tous les points sont alignés
    if a == 0 and b == 0:
        liste = [[dist(demi_droite.A, segment.A), segment.A],
                 [dist(demi_droite.A, segment.B), segment.B]]
        # On retourne le point le plus proche de demi_droite.A si il
        # appartient à la demi-droite
        I = min(liste)[1]
        if point_appartient_demi_droite(I, demi_droite):
            return I
        return None

    # Si a+b=0, cela signifie que la demi-droite ou le segment
    # est nul ou qu'ils sont parallèles
    if a + b == 0:
        return None

    # Si a=0 ou b=0, cela signifie qu'au moins un point du segment
    # appartient à la droite (3 points alignés)
    if a == 0:
        # On retourne le point concerné si il appartient à la demi-droite
        if point_appartient_demi_droite(segment.B, demi_droite):
            return segment.B
        return None

    if b == 0:
        if point_appartient_demi_droite(segment.A, demi_droite):
            return segment.A
        return None

    # Si le point I appartient à la demi_droite et au segment
    if signe(a) == signe(b):
        x = (a * segment.A.x + b * segment.B.x) / (a + b)
        y = (a * segment.A.y + b * segment.B.y) / (a + b)
        I = Point(x, y)
        if point_appartient_demi_droite(I, demi_droite):
            return I
    return None


def rotation(O, M, angle):
    """
    Arguments :
        - O : objet de classe 'Point'
        - M : objet de classe 'Point'
        - angle : angle donné en degrés
    Retourne :
        - Un objet de classe 'Point' étant la rotation du point M
        autour du centre O et d'angle 'angle'
    """

    # Angle converti en radian
    angle = angle * math.pi / 180
    # calcul de la rotation
    xM = M.x - O.x
    yM = M.y - O.y
    x = xM * math.cos(angle) + yM * math.sin(angle) + O.x
    y = - xM * math.sin(angle) + yM * math.cos(angle) + O.y
    return (Point(x, y))


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
