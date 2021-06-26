# -*- coding: utf-8 -*-
"""
Projet maths-info - Galerie d'art

Groupe 12 : MEYNIEL Arthur, FOUCHÉ Hugo, BOUY Hugo
"""

from shared import Point, Segment,\
    intersection_demi_droite_segment, dist,\
    point_egaux, point_appartient_segment, determinant_3_points, signe

# Taille des point affichés sur le canvas
size = 4
precision = 0.01


class calcul_polygon_eclairage():
    """Classe utilisée par le calcul du polygon d'éclairage"""

    def __init__(self, start_point, polygon, canvas, mode_demo=False):
        """Atributs :
            - start_point : Tuple ou liste sous la forme (x, y) ou [x, y]
            - polygon : Liste de sommets sous la forme  [(xA, yA), (xB, yB)...]
            - canvas : Canvas de dessin
            - mode_demo : Boolean, True pour activer le mode de démonstration
        """
        if not (type(start_point) == tuple or type(start_point) == list):
            return None
        if not (len(start_point) == 2):
            return None

        self.canvas, self.mode_demo = canvas, mode_demo

        self.canvas.delete("demo")

        # Création d'une liste contenant les segments du polygon
        self.liste_segments_polygon = list()
        A = Point(polygon[0][0], polygon[0][1])
        for i in range(1, len(polygon)):
            B = Point(polygon[i][0], polygon[i][1])
            self.liste_segments_polygon.append(Segment(A, B))
            A = B
        B = Point(polygon[0][0], polygon[0][1])
        self.liste_segments_polygon.append(Segment(A, B))

        # Création d'une liste contenant les sommets du polygon
        self.liste_sommets_polygon = list()
        for point in polygon:
            self.liste_sommets_polygon.append(Point(point[0], point[1]))

        # Le point O est le point où l'on souhaite connaître le polygon
        # d'éclairage
        self.O = Point(start_point[0], start_point[1])

        # Affichage de la source lumineuse en blanche
        self.canvas.create_oval(self.O.x - size, self.O.y - size,
                                self.O.x + size, self.O.y + size,
                                fill='white', tag='demo')

    def return_polygon(self):
        """Retourne le polygon d'éclairage avec les paramètres
        de la classe"""

        # Liste qui contiendra les intersections retenues (la plus proche
        # du point et les projections) avec leur status
        liste_intersections_def = list()

        # Pour chaque sommet du polygon, on va chercher son projeté le plus
        # proche
        for sommet in self.liste_sommets_polygon:
            # Liste des points d'intersections avec les segments du polygon
            liste_intersections = list()

            # Segment de référence du point O au sommet
            segment_sommet = Segment(self.O, sommet)

            # Pour chaque sommet : on parcours la liste de tous les segments
            # du polygon
            for segment in self.liste_segments_polygon:
                # On cherche les points d'intersection entre la demi droite
                # définie par O et le sommet et le segment considéré du polygon
                I = intersection_demi_droite_segment(segment_sommet, segment)

                # Si un point d'intersection existe
                if I is not None:
                    # Les sommets étant détectés deux fois,
                    # on ne les compte qu'une
                    if liste_intersections.count([dist(self.O, I), I,
                                                  self.liste_sommets_polygon
                                                  .index(sommet)]) == 1:
                        continue
                    # On l'ajoute à la liste des intersections détectés.
                    liste_intersections.append([dist(self.O, I), I,
                                                self.liste_sommets_polygon.
                                                index(sommet)])

            # Pour chaque sommet, une fois toutes les intersections trouvés,
            # on cherche la plus proche du point O
            liste_intersections.sort()
            min_intersection = liste_intersections[0]
            I = min_intersection[1]

            result = self.status_intersections(liste_intersections, sommet,
                                               list())
            for intersection in result:
                liste_intersections_def.append(intersection)

        # Dans le mode de démonstration, on affiche les intersections
        # définitives trouvés avec la couleur associée à son status.
        if self.mode_demo:
            for intersection in liste_intersections_def:
                I = intersection[0]
                # print(I)
                self.canvas.create_line(self.O.x, self.O.y, I.x,
                                        I.y, fill='red',
                                        tag='demo')
                if intersection[1] == 'AHEAD':
                    continue
                elif intersection[1] == 'EQUALS':
                    color = 'green'
                else:
                    color = 'blue'
                self.canvas.create_oval(I.x - size, I.y - size, I.x + size,
                                        I.y + size, fill=color, tag='demo')

        # Liste des intersections dans l'ordre
        liste_intersections_ordones = list()
        count = 0

        # Une fois toutes les intersections trouvés, il convient de les trier
        # pour en faire un polygon d'éclairage
        # On parcous la liste des segments du polygon dans l'ordre
        for segment in self.liste_segments_polygon:
            intersections_sur_segment = list()
            # On parcous la liste des intersections trouvés plus haut
            for intersection in liste_intersections_def:
                # print(intersection[0], intersection[1])
                I = intersection[0]
                # Si l'intersection est sur le segment considéré, on l'ajoute
                # dans une nouvelle liste.
                if point_appartient_segment(I, segment):
                    if not intersection[1] == "AHEAD":
                        intersections_sur_segment.append(
                            [dist(segment.A, I), intersection])
            # Une fois la liste tous les points d'intersections se trouvant sur
            # le segment considéré sont trouvés
            # On vérifie qu'il y en a au moins un
            if not intersections_sur_segment:
                continue
            # On les tris dans l'ordre croissant de leur distance avec
            # le premier point du segment
            intersections_sur_segment.sort()
            # Une fois dans l'ordre
            for intersection in intersections_sur_segment:
                I = (intersection[1][0].x, intersection[1][0].y)

                # Détection des doublons
                doublons = False
                for point in liste_intersections_ordones:
                    if abs(I[0] - point[0]) < precision and\
                            abs(I[1] - point[1]) < precision:
                        doublons = True

                if not doublons:
                    # On leur attribut leur numéro
                    count += 1
                    # On sauvegarde les coordonnées de l'intersections dans une
                    # nouvelle liste
                    liste_intersections_ordones.append(I)
                    liste_intersections_def.remove(intersection[1])
                    # Dans le mode de démo, on affiche leur numéro à côté
                    if self.mode_demo:
                        self.canvas.create_text(I[0], I[1] - 10, text=count,
                                                tag='demo')
        # On retourne la liste ordonnée des intersections
        # correspondant au polygon d'éclairage
        return liste_intersections_ordones

    def status_intersections(self, liste_intersections, sommet,
                             points_indentifies):
        """Arguments :
           - liste_intersections : liste
           - sommet : objet de type classe_point
           - points_indentifiées : liste contenant les points identifiés
           par la fonction, utilsiée par le recursif
         Retourne la liste des points identifiés avec leur statut (contenant
         l'intersection la plus proche et ses eventuels projetés"""

        liste_intersections.sort()
        I = liste_intersections[0][1]
        indice_sommet = liste_intersections[0][2]

        # Si la liste points_identifies n'est pas vide il s'agit d'un appel
        # récursif
        recursif = False
        if points_indentifies:
            recursif = True

        est_sommet = False

        # Si il s'agit du sommet en cours
        if point_egaux(I, sommet):
            est_sommet = True

        # Si il s'agit d'un autre sommet du polygon
        else:
            est_sommet, indice = self.sommet_du_polygon(I)
            if indice is not None:
                # On met à jour l'indice du sommet (dans le cas d'une
                # intersection se trouvant être un sommet)
                liste_intersections[0][2] = indice
                indice_sommet = indice

        if est_sommet:
            # On ajoute le statut du point indentifié
            status = "EQUALS"
            if recursif:
                status = "BEYOND"
            points_indentifies.append([I, status])

            # Si il ne s'agit pas d'une projection, fin de traitement
            if not self.verif_si_projection(sommet, indice_sommet):
                return points_indentifies
            # Sinon, on passe à l'intersection suivante
            del liste_intersections[0]

            if not liste_intersections:
                return points_indentifies
            # On rappelle la fonctions
            return self.status_intersections(liste_intersections, sommet,
                                             points_indentifies)

        status = "AHEAD"
        if recursif:
            status = "BEYOND"
        points_indentifies.append([I, status])
        return points_indentifies

    def verif_si_projection(self, sommet, indice_sommet):
        """Arguments :
            - sommet : objet de type classe_point
            - indice_sommet : indice du sommet dans le polygon
        Retourne True si le sommet passé en argument a une projection"""

        # Méthode basée sur le calcul de déterminant entre le point O, le
        # sommet i, i+1 et i-1. Si le sommet i+1 et i-1 sont tous deux
        # à droite ou à gauche du sommet i, alors il s'agit d'une projection.

        det1 = determinant_3_points(self.O, sommet,
                                    self.liste_sommets_polygon
                                    [indice_sommet - 1])

        if indice_sommet == len(self.liste_sommets_polygon) - 1:
            indice_sommet = -1

        det2 = determinant_3_points(self.O, sommet,
                                    self.liste_sommets_polygon
                                    [indice_sommet + 1])

        if signe(det1) == 0 or signe(det2) == 0:
            return False

        if signe(det1) == signe(det2):
            return True
        return False

    def sommet_du_polygon(self, I):
        """Arguments :
            - I : objet de type classe_point
        Retourne True et l'indice du sommet correspondant si le point I
        est un sommet du polygon. Renvoie False et None sinon"""

        # On parcours la liste des sommets du polygon et vérifie si il
        # s'agit du point I
        for sommet in self.liste_sommets_polygon:
            if point_egaux(I, sommet):
                return (True, self.liste_sommets_polygon.index(sommet))
        return (False, None)


def polygon_eclairage(start_point, polygon, canvas, mode_demo=False):
    """Arguments :
        - start_point : Tuple ou liste sous la forme (x, y) ou [x, y]
        - polygon : Liste de sommets sous la forme  [(xA, yA), (xB, yB) ...]
        - canvas : Canvas de dessin
        - mode_demo : Boolean, True pour activer le mode de démonstration
    Retourne le polygon d'éclairage sous la forme d'une liste de points
    au format tuple : [(xA, yA), (xB, yB) ...]"""
    per = calcul_polygon_eclairage(start_point, polygon, canvas, mode_demo)
    return per.return_polygon()


if __name__ == '__main__':
    import tkinter as tk
    import point_in_polygon as pip

    wnd = tk.Tk()
    cnv = tk.Canvas(wnd, width=600, height=400)
    cnv.pack()
    A = (490, 225)
    polygone = [(332, 291), (438, 335), (751, 286), (725, 107), (287, 88)]
    print(pip.point_in_polygon(A, polygone))
    cnv.create_polygon(polygone, fill='grey')
    lumiere = polygon_eclairage(A, polygone, cnv, True)
    # cnv.create_polygon(lumiere, fill='yellow')
    cnv.create_oval(A[0] - 3, A[1] - 3, A[0] + 3, A[1] + 3,
                    fill='blue')
    wnd.mainloop()
