# -*- coding: utf-8 -*-
"""
Projet maths-info - Galerie d'art

Groupe 12 : MEYNIEL Arthur, FOUCHÉ Hugo, BOUY Hugo
"""

from polygon_eclairage import polygon_eclairage
from aire_multi_polygones import aire_multi_polygones
from point_in_polygon import point_in_polygon
import random


def aire_polygon(points_coords):
    sommeX_Y1 = 0
    sommeY_X1 = 0
    for i in range(len(points_coords)):
        if i + 1 == len(points_coords):
            sommeX_Y1 += points_coords[i][0] * points_coords[0][1]
            sommeY_X1 += points_coords[i][1] * points_coords[0][0]
        else:
            sommeX_Y1 += points_coords[i][0] * points_coords[i + 1][1]
            sommeY_X1 += points_coords[i][1] * points_coords[i + 1][0]
    return int(abs(0.5 * (sommeX_Y1 - sommeY_X1)))


def creer_pop(nombre_gardiens, pop_taille, liste_sommets, cnv):
    """
    Arguments :
        - nombre_gardiens : nombre de gardiens à placer
        - pop_taille : nombre d'individu généré par génération
        - liste_sommets : liste d'objets de type tuple représentant les sommets
                          du polygone dessinant le musée
        - cnv : objet de type tkinter.Canvas
    Retourne :
        - pop : liste de listes sous forme [x, y] représentant les
                individus de la génération
    """
    pop = []
    for i in range(pop_taille):
        individu = []
        # Création d'individus dans le polygone
        for j in range(nombre_gardiens):
            x = random.randint(0, 600)
            y = random.randint(0, 400)
            while not point_in_polygon((x, y), liste_sommets, cnv):
                x = random.randint(0, 600)
                y = random.randint(0, 400)
            individu.append([x, y])
        pop.append(individu)
    return pop


def classer_pop(pop, nombre_gardiens, liste_sommets, canvas):
    """
     Arguments :
        - pop : liste de listes sous forme [x, y] représentant les
                individus de la génération
        - nombre_gardiens : nombre de gardiens à placer
        - liste_sommets : liste d'objets de type tuple représentant les sommets
                          du polygone dessinant le musée
        - canvas : objets de type tkinter.Canvas
    Retourne :
        - pop_sorted : liste de tuples sous forme (int, [x, y]) représentant
        les individus de la génération et l'aire de leur polygone de lumière
    """
    if nombre_gardiens == 1:
        pop_sorted = []
        for indiv in pop:
            polygone_lumiere = polygon_eclairage(indiv[0],
                                                 liste_sommets,
                                                 canvas)
            aire = aire_polygon(polygone_lumiere)
            pop_sorted.append((aire, indiv[0]))
        pop_sorted.sort(reverse=True)
    else:
        pop_sorted = []
        for indiv in pop:
            polygone_lumiere = list()
            for gardien in indiv:
                polygone_lumiere.append(polygon_eclairage(gardien,
                                                          liste_sommets,
                                                          canvas))
            aire = aire_multi_polygones(polygone_lumiere)
            pop_sorted.append((aire, indiv))
        pop_sorted.sort(reverse=True)
    return pop_sorted


def moyenne_cross_over(pop_sorted, pop_taille, nombre_gardiens,
                       liste_sommets, cnv):
    """
    Arguments :
        - pop_sorted : liste de tuples sous forme (int, [x, y]) représentant
                       les individus de la génération et l'aire de leur
                       polygone de lumière
        - pop_taille : nombre d'individu généré par génération
        - nombre_gardiens : nombre de gardiens à placer
        - liste_sommets : liste d'objets de type tuple représentant les sommets
                          du polygone dessinant le musée
        - cnv : objet de type tkinter.Canvas
    Retourne :
        - pop : liste de listes sous forme [x, y] représentant les
                individus de la génération après cross_over
    """
    if nombre_gardiens == 1:
        pop = []
        # clonage du meilleur individu
        pop.append(pop_sorted[0][1])
        # crossover des meilleurs individus entre eux
        for i in range(pop_taille // 2 - 1):
            new_individu = [(pop_sorted[i][1][0] +
                             pop_sorted[i + 1][1][0]) // 2,
                            (pop_sorted[i][1][1] +
                             pop_sorted[i + 1][1][1]) // 2]
            # verification que le nouvel individu est bien dans le polygone
            if new_individu[0] < 600 and new_individu[1] < 400 and \
               new_individu[0] > 0 and new_individu[1] > 0:
                if point_in_polygon((new_individu[0], new_individu[1]),
                                    liste_sommets, cnv):
                    pop.append(new_individu)
                else:
                    pop.append(pop_sorted[i][1])
        return pop
    else:
        pop = []
        # clonage du meilleur individu
        pop.append(pop_sorted[0][1])
        # crossover des meilleurs individus entre eux
        for i in range(pop_taille // 2 - 1):
            new_individu = list()
            for j in range(nombre_gardiens):
                new_gardien = [(pop_sorted[i][1][j][0] +
                                pop_sorted[i + 1][1][j][0]) // 2,
                               (pop_sorted[i][1][j][1] +
                                pop_sorted[i + 1][1][j][1]) // 2]
                # verification que le nouvel individu est bien dans le polygone
                if new_gardien[0] < 600 and new_gardien[1] < 400 and \
                   new_gardien[0] > 0 and new_gardien[1] > 0:
                    if point_in_polygon((new_gardien[0], new_gardien[1]),
                                        liste_sommets, cnv):
                        new_individu.append(new_gardien)
                    else:
                        new_individu.append(pop_sorted[i][1][j])
                else:
                    new_individu.append(pop_sorted[i][1][j])
            pop.append(new_individu)
        return pop


def mutation(pop, mutation_proba, nombre_gardiens, liste_sommets, cnv):
    """
    Arguments :
        - pop : liste de listes sous forme [x, y] représentant les
                individus de la génération après cross_over
        - mutation_proba : float representant la probabilité de mutation
                           (pas plus de 0.1)
        - nombre_gardiens : nombre de gardiens à placer
        - liste_sommets : liste d'objets de type tuple représentant les sommets
                          du polygone dessinant le musée
        - cnv : objet de type tkinter.Canvas
    Retourne :
        - pop : liste de listes sous forme [x, y] représentant les
                individus de la génération après mutation
    """
    if nombre_gardiens == 1:
        for indiv in pop:
            if random.random() < mutation_proba:
                dirX = random.randint(0, 1)
                dirY = random.randint(0, 1)
                if dirX == 1 and dirY == 1:
                    if point_in_polygon((indiv[0] + 1, indiv[1] + 1),
                                        liste_sommets, cnv):
                        indiv[0] += 1
                        indiv[1] += 1
                elif dirX == 1 and dirY == 0:
                    if point_in_polygon((indiv[0] + 1, indiv[1] - 1),
                                        liste_sommets, cnv):
                        indiv[0] += 1
                        indiv[1] -= 1
                elif dirX == 0 and dirY == 1:
                    if point_in_polygon((indiv[0] - 1, indiv[1] + 1),
                                        liste_sommets, cnv):
                        indiv[0] -= 1
                        indiv[1] += 1
                else:
                    if point_in_polygon((indiv[0] - 1, indiv[1] - 1),
                                        liste_sommets, cnv):
                        indiv[0] -= 1
                        indiv[1] -= 1
        return pop
    else:
        for indiv in pop:
            for gardien in indiv:
                if random.random() < mutation_proba:
                    dirX = random.randint(0, 1)
                    dirY = random.randint(0, 1)
                    if dirX == 1 and dirY == 1:
                        if point_in_polygon((gardien[0] + 1, gardien[1] + 1),
                                            liste_sommets, cnv):
                            gardien[0] += 1
                            gardien[1] += 1
                    elif dirX == 1 and dirY == 0:
                        if point_in_polygon((gardien[0] + 1, gardien[1] - 1),
                                            liste_sommets, cnv):
                            gardien[0] += 1
                            gardien[1] -= 1
                    elif dirX == 0 and dirY == 1:
                        if point_in_polygon((gardien[0] - 1, gardien[1] + 1),
                                            liste_sommets, cnv):
                            gardien[0] -= 1
                            gardien[1] += 1
                    else:
                        if point_in_polygon((gardien[0] - 1, gardien[1] - 1),
                                            liste_sommets, cnv):
                            gardien[0] -= 1
                            gardien[1] -= 1
        return pop


def completer_pop(pop, pop_taille, nombre_gardiens, liste_sommets, cnv):
    """
    Arguments :
        - pop : liste de listes sous forme [x, y] représentant les
                individus de la génération après mutation
        - pop_taille : nombre d'individu généré par génération
        - nombre_gardiens : nombre de gardiens à placer
        - liste_sommets : liste d'objets de type tuple représentant les sommets
                          du polygone dessinant le musée
        - cnv : objet de type tkinter.Canvas
    Retourne :
        - new_pop : liste de listes sous forme [x, y] représentant les
                    individus de la nouvelle génération
    """
    if nombre_gardiens == 1:
        new_pop = []
        for indiv in pop:
            new_pop.append([indiv])
        nombre_manquant = pop_taille - len(pop)
        for i in range(nombre_manquant):
            x = random.randint(0, 400)
            y = random.randint(0, 400)
            while not point_in_polygon((x, y), liste_sommets, cnv):
                x = random.randint(0, 600)
                y = random.randint(0, 400)
            new_pop.append([[x, y]])
        return new_pop
    else:
        new_pop = []
        for indiv in pop:
            new_pop.append(indiv)
        nombre_manquant = pop_taille - len(pop)
        for i in range(nombre_manquant):
            individu = []
            for j in range(nombre_gardiens):
                x = random.randint(0, 600)
                y = random.randint(0, 400)
                while not point_in_polygon((x, y), liste_sommets, cnv):
                    x = random.randint(0, 600)
                    y = random.randint(0, 400)
                individu.append([x, y])
            new_pop.append(individu)
        return new_pop


def tester_pop(pop_sorted, seuil, nombre_gardiens, aire_totale):
    """
    Arguments :
        - pop_sorted : liste de tuples sous forme (int, [x, y]) représentant
                       les individus de la génération et l'aire de leur
                       polygone de lumière
        - seuil : float représentant le taux de remplissage de l'aire souhaité
        - nombre_gardiens : nombre de gardiens à placer
        - aire_totale : int répresentant l'aire de tout le musée
    Retourne :
        - True si le seuil est satisfait, False sinon
    """
    aire_meilleur = pop_sorted[0][0]
    if aire_meilleur / aire_totale > seuil:
        return True


def entrainement(pop_taille, nombre_gardiens, mutation_proba, seuil,
                 generation_max, wnd, canvas, liste_sommets):
    """
    Arguments :
        - pop_taille : nombre d'individu généré par génération
        - nombre_gardiens : nombre de gardiens à placer
        - mutation_proba : float representant la probabilité de mutation
                           (pas plus de 0.1)
        - seuil : float représentant le taux de remplissage de l'aire souhaité
        - generation_max : nombre de generations maximum durant l'entrainement
        - wnd : objet de type tkinter.Tk
        - cnv : objets de type tkinter.Canvas
    Retourne :
        - pop_sorted[1][0] : position du meilleur individu
        - wnd : objet de type tkinter.Tk
        - cnv : objets de type tkinter.Canvas
        - liste_sommets : liste d'objets de type tuple représentant les sommets
                          du polygone dessinant le musée
        - pop_sorted[0][0] : aire du meilleur individu
    """
    # préparation des données
    aire_totale = aire_polygon(liste_sommets)
    # création de la première population
    pop = creer_pop(nombre_gardiens, pop_taille, liste_sommets, canvas)
    # initialisation des variables
    termine = False
    generation = 1
    # lancement de l'entrainement
    for i in range(generation_max):
        print(f'generation n°{generation}')
        # classement de la population
        pop_sorted = classer_pop(pop, nombre_gardiens, liste_sommets, canvas)
        # vérification du score par rapport au seuil
        termine = tester_pop(pop_sorted, seuil, nombre_gardiens, aire_totale)

        # fin de l'entrainement (mission accomplie)
        if termine is True:
            print(f"Une solution satisfaisante à {pop_sorted[0][0]} "
                  f"({round((pop_sorted[0][0]/aire_totale)*100, 2)}%) "
                  f"a été obtenue à la {generation}ème "
                  f"generation: {pop_sorted[0][1]}")
            return pop_sorted[0][1], wnd, canvas,\
                liste_sommets, pop_sorted[0][0]

        # cross_over, mutation et création d'une nouvelle génération évoluée
        print(f'aire meilleur individu : {pop_sorted[0][0]} '
              f'({(pop_sorted[0][0]/aire_totale)*100}%)')
        pop_cross_over = moyenne_cross_over(pop_sorted, pop_taille,
                                            nombre_gardiens, liste_sommets,
                                            canvas)
        pop_mutation = mutation(pop_cross_over, mutation_proba,
                                nombre_gardiens, liste_sommets, canvas)
        pop = completer_pop(pop_mutation, pop_taille, nombre_gardiens,
                            liste_sommets, canvas)
        generation += 1

    # fin de l'entrainement (seuil non-atteint)
    print(f"Une solution satisfaisante à {pop_sorted[0][0]} "
          f"({round((pop_sorted[0][0]/aire_totale)*100, 2)}%) "
          f"a été obtenue à la {generation}ème "
          f"generation: {pop_sorted[0][1]}")
    return pop_sorted[0][1], wnd, canvas, liste_sommets, pop_sorted[0][0]
