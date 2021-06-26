# -*- coding: utf-8 -*-
"""
Projet maths-info - Galerie d'art

Groupe 12 : MEYNIEL Arthur, FOUCHÉ Hugo, BOUY Hugo
"""

import tkinter as tk
import tkinter.filedialog
import random

import point_in_polygon as pip
import polygon_eclairage as pe
import intersections_rayons_obstacles as iro
import clipping as cl

from shared import Point, Segment, intersection_droites,\
    rotation, projection_point_cercle, angle_deux_points


class Application():
    """Crée la fenêtre de l'application de démonstration"""
    nbrayons = 60  # Nombre de rayon partants de la source lumineuse pour la
    # demo 2 et 4
    sommets_polygon = list()  # Liste contenant les futurs sommets du polygon
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                'Y', 'Z']
    fichier_config = "config.txt"  # Fichier contenant les chemins des presets
    puissance = 100  # Rayon du cercle
    angle = 30  # Angle du clipping pour la demo 6

    def __init__(self, width, height):
        """Prend en argument :
            width : largeur de la fenêtre
            height : hauteur de la fenêtre
        """

        # Création de la fenêtre, du canvas et de la frame de commande
        self.width, self.height = width, height
        self.wnd = tk.Tk()
        self.wnd.title("Galerie d'art - Demonstrateur")
        self.cnv = tk.Canvas(self.wnd, width=self.width, height=self.height,
                             bg='white')
        self.cnv.pack()
        self.frm = tk.Frame(self.wnd, width=self.width, height=100, pady=10,
                            relief='ridge', bd=10)
        self.frm.pack(side=tk.BOTTOM)

        self.frm.columnconfigure(1, minsize=50)

        # Configuration des widgets graphiques
        tk.Label(self.frm, text="CONFIGURATION DEMONSTRATIONS")\
            .grid(row=0, column=0, columnspan=5, ipadx=10, ipady=10,
                  sticky='new')

        tk.Label(self.frm, text="Modes de démo :")\
            .grid(row=1, column=0, ipadx=10, sticky='n')

        tk.Label(self.frm, text="Options :")\
            .grid(row=1, column=3, ipadx=10, sticky='n')

        tk.Button(self.frm, text="[DEMO 1] Intersection deux droites",
                  command=self.demo1)\
            .grid(row=2, column=0, ipadx=10, pady=5, sticky='n')

        tk.Button(self.frm, text="[DEMO 2] Rayons et obstacles",
                  command=self.demo2)\
            .grid(row=3, column=0, ipadx=10, pady=5, sticky='n')

        tk.Button(self.frm, text="[DEMO 3] Dessiner un polygone",
                  command=self.demo3)\
            .grid(row=4, column=0, ipadx=10, pady=5, sticky='n')

        tk.Button(self.frm, text="[DEMO 4] Lancer de rayons",
                  command=lambda: self.demo4_5_6(4))\
            .grid(row=5, column=0, ipadx=10, pady=5, sticky='n')

        tk.Button(self.frm, text="[DEMO 5] Polygon éclairage",
                  command=lambda: self.demo4_5_6(5))\
            .grid(row=6, column=0, ipadx=10, pady=5, sticky='n')

        tk.Button(self.frm, text="[DEMO 6] Clipping",
                  command=lambda: self.demo4_5_6(6))\
            .grid(row=7, column=0, ipadx=10, pady=5, sticky='n')

        tk.Button(self.frm, text="Reset", command=self.reset)\
            .grid(row=2, column=3, ipadx=10, pady=5, sticky='n')

        tk.Label(self.frm, text="Nombre d'obstacles :")\
            .grid(row=3, column=2, ipadx=10, sticky='n')
        self.nb_obstacles = tk.Scale(self.frm, from_=1, to=10,
                                     orient=tk.HORIZONTAL)
        self.nb_obstacles.set(1)
        self.nb_obstacles.grid(row=3, column=3, ipadx=10, sticky='n')

        tk.Button(self.frm, text="Sauvegarder polygon/Modifier preset",
                  command=self.save_polygon)\
            .grid(row=4, column=3, ipadx=10, pady=5, sticky='n')

        self.preset = tk.IntVar()
        a = tk.Radiobutton(self.frm, text='Preset 1', variable=self.preset,
                           value=1)
        a.grid(row=5, column=2, ipadx=10, sticky='n')
        a.select()
        tk.Radiobutton(self.frm, text='Preset 2', variable=self.preset,
                       value=2)\
            .grid(row=5, column=3, ipadx=10, sticky='n')
        tk.Radiobutton(self.frm, text='Preset 3', variable=self.preset,
                       value=3)\
            .grid(row=5, column=4, ipadx=10, sticky='n')

        tk.Label(self.frm, text="Angle de la torche :")\
            .grid(row=6, column=2, ipadx=10, sticky='n')
        self.angle_torche = tk.Scale(self.frm, from_=0, to=360,
                                     orient=tk.HORIZONTAL)
        self.angle_torche.set(180)
        self.angle_torche.grid(row=6, column=3, ipadx=10, sticky='n')

        self.mode_demo = tk.IntVar()
        tk.Checkbutton(self.frm, text="Mode demo", variable=self.mode_demo)\
            .grid(row=6, column=4, ipadx=10, sticky='n')

        self.error_label = tk.Label(self.frm, text="")
        self.error_label.grid(row=7, column=3, ipadx=10, sticky='n')

        self.wnd.mainloop()

    # Fonctions utilisés par plusieurs modes de démo

    def reset(self):
        """Reset du canvas. Suppression de tous les éléments de dessin"""

        self.cnv.unbind('<Button-1>')
        self.cnv.delete(tk.ALL)
        self.error_label.config(text="")

    def get_polygon_preset(self):
        """Fonction permettant de récupérer le polygon correspondant
        au preset sélectionné par l'utilisateur"""

        try:
            # On ouvre le fichier config
            with open(self.fichier_config, 'r') as f:
                for i in range(self.preset.get()):
                    line = f.readline()
                # On lit l'adresse du fichier du preset
                line = line[8:-1]
                if not line:
                    string = "Aucun fichier enregistré sur le preset " +\
                        str(self.preset.get())
                    self.error_label.config(text=string, fg='red')
                    return None
            # On lit le polygon dans le fichier correspondant
            with open(line, 'r') as f:
                line = eval(f.readline())
            return(line)
        except FileNotFoundError:
            # Si un des fichier n'est pas trouvé
            string = "Fichier d'accès du preset" + str(self.preset.get())\
                + " invalide. Ou fichier config inexistant"
            self.error_label.config(text=string, fg='red')

    def lancement_preset(self, type_demo, demo=False):
        """Dessin du polygon dans le canvas et mémorisation des segments
        Arguments:
            type_demo: numéro de la demo (de 4 à 6)"""

        size = 4
        self.d_to_check = list()
        self.cnv.delete(tk.ALL)
        color = 'grey'
        if type_demo == 6:
            color = 'white'
        # Création du polygon
        self.cnv.create_polygon(self.sommets_polygon, fill=color)

        # Mémorisation des segments
        for i in range(len(self.sommets_polygon)):
            A = self.sommets_polygon[i]
            if i > 0:
                B = self.sommets_polygon[i - 1]
                self.d_to_check.append(
                    Segment(Point(B[0], B[1]), Point(A[0], A[1])))
            if demo:
                # Si le mode démo est activé on affiche les sommets du polygon
                self.cnv.create_oval(A[0] - size, A[1] - size, A[0] + size,
                                     A[1] + size, fill='black')
        A = self.sommets_polygon[0]
        B = self.sommets_polygon[-1]
        self.d_to_check.append(Segment(Point(B[0], B[1]), Point(A[0], A[1])))
        # Bind du clic gauche suivant les différents modes de démo
        if type_demo == 6:
            for segment in self.d_to_check:
                # Affichage d'une bordure du polygon pour le clipping
                self.cnv.create_line(segment.A.x, segment.A.y,
                                     segment.B.x, segment.B.y,
                                     width=1, tag='polygon')
        if type_demo == 4:
            self.cnv.bind('<Button-1>', self.clic_rayons_polygon_demo)

        elif type_demo == 5:
            self.cnv.bind('<Button-1>', self.polygone_eclairage)

        elif type_demo == 6:
            self.cnv.bind('<Button-1>', self.clipping)

    def demo4_5_6(self, id_demo):
        """Fonction appellée par les boutons demo 4, 5, 6"""

        self.reset()
        # Récupération du polygon sélectionné par le preset
        self.sommets_polygon = self.get_polygon_preset()
        if self.sommets_polygon is not None:
            self.lancement_preset(id_demo)

    # Fonctions utilisés par le mode de démonstration 6

    def clipping(self, event):
        """Fonction appelant le clipping lorsque l'utilisateur clic dans
        le polygon"""

        # Si le point est dans le polygon
        if pip.point_in_polygon((event.x, event.y), self.sommets_polygon):
            # On supprime le précédent clip
            self.cnv.delete("cone")
            self.cnv.delete("clip1")
            self.cnv.delete("clip2")
            self.cnv.delete("cercle")

            direction = self.angle_torche.get()

            position = Point(event.x, event.y)
            C = Point(position.x + self.puissance + 50, position.y)
            C = rotation(position, C, direction)
            C1 = rotation(position, C, -self.angle)
            C2 = rotation(position, C, self.angle)

            # On veut l'intersection sur le cercle
            # Projection 1
            proj1 = projection_point_cercle(position, C1, self.puissance)

            # Projection 2
            proj2 = projection_point_cercle(position, C2, self.puissance)
            # Cone de lumière
            self.cnv.create_arc(position.x - self.puissance,
                                position.y - self.puissance,
                                position.x + self.puissance,
                                position.y + self.puissance,
                                start=-angle_deux_points(proj1, position,
                                                         True),
                                extent=2 * self.angle,
                                tag="cone",
                                fill="yellow", outline="yellow")

            cl.clip(self.cnv, proj1, proj2, position, self.puissance,
                    self.d_to_check)
            self.cnv.tag_raise('polygon')

    # Fonctions utilisés par le mode de démonstration 5

    def polygone_eclairage(self, event):
        """Fonction affichant le polygon d'éclairage lorsque
        l'utilisateur clic dans le polygon"""

        if pip.point_in_polygon((event.x, event.y), self.sommets_polygon):
            self.cnv.delete('light')
            polygon = pe.polygon_eclairage((event.x, event.y),
                                           self.sommets_polygon,
                                           self.cnv, self.mode_demo.get())
            self.cnv.create_polygon(polygon, fill='yellow', tag='light')
            self.cnv.tag_raise('demo')

    # Fonctions utilisés par le mode de démonstration 4

    def clic_rayons_polygon_demo(self, event):
        """Fonction affichant les rayons envoyés depuis le clic
        de l'utilisateur dans le polygon"""

        point = Point(event.x, event.y)
        if pip.point_in_polygon((event.x, event.y), self.sommets_polygon):
            iro.intersections_rayons_obstacles(self.cnv, point, self.nbrayons,
                                               360, 0, self.d_to_check,
                                               self.mode_demo.get())

    # Fonctions utilisés par le mode de démonstration 3

    def demo3(self):
        """Lancement de la demo 3 : Dessiner un polygon"""

        self.reset()
        # Liste des sommets du polygon
        self.sommets_polygon = list()
        self.cnv.delete(tk.ALL)
        self.cnv.bind('<Button-1>', self.dessin_polygone_demo)
        self.cnv.bind('<Button-3>', self.fin_dessin_polygone)

    def dessin_polygone_demo(self, event):
        """Pour chaque clic, on dessine le point correspondant"""

        # Taille des points du polygon
        size = 4
        # A chaque clic, au affiche le point correspondant
        self.cnv.create_oval(event.x - size, event.y - size, event.x + size,
                             event.y + size, fill='black', tag='pts')
        # On l'ajoute à la liste des sommets du polygon
        self.sommets_polygon.append((event.x, event.y))
        # On affiche une lettre à côté du point
        i = (len(self.sommets_polygon) - 1) // 26
        # On ajoute un ' à chaque tour d'alphabet
        lettre = self.alphabet[(len(self.sommets_polygon) % 26) - 1] + i * "'"
        self.cnv.create_text(event.x, event.y - 10,
                             text=lettre, tag='lettre')

    def fin_dessin_polygone(self, event, getpartern=False):
        """Dessine le polygon avec les points déssinés par l'utilisateur
        Prend un paramètre facultatif supplémentaire en argument :
        getpatern : si True, affiche dans la console la liste des points
        du polygon"""

        # Si le polygon ne contient pas au moins 3 points
        if len(self.sommets_polygon) < 3:
            return
        # Dessin du polygon
        self.cnv.create_polygon(self.sommets_polygon, fill='grey')
        # Réhaussement des lettres au premier plan
        self.cnv.tag_raise('lettre')
        if getpartern:
            print(self.sommets_polygon)
        self.cnv.delete('pts')
        self.cnv.unbind('<Button-1>')

    def save_polygon(self):
        """Ouvre le menu de sauvegarde du polygon et de modification
        des presets"""

        if self.sommets_polygon is not None:
            if len(self.sommets_polygon) < 3:
                Save_popup(self.wnd)
                return
        Save_popup(self.wnd, self.sommets_polygon)

    # Fonctions utilisés par le mode de démonstration 2

    def demo2(self):
        """Lancement de la demo 2 : Rayons contre obstacles"""

        nbobstacle = self.nb_obstacles.get()
        self.reset()

        # Liste des segments à vérifier. L'algorithme cherchera les points
        # d'intersection des droites définies par deux points dans cette liste
        # Au lancement de la demo, seul les 4 coins de la fenêtre sont
        # renseignés
        self.polygones = list()
        self.d_to_check = [Segment(Point(0, 0), Point(self.width, 0)),
                           Segment(Point(0, 0), Point(0, self.height)),
                           Segment(Point(self.width, 0), Point(self.width,
                                                               self.height)),
                           Segment(Point(0, self.height), Point(self.width,
                                                                self.height))]

        self.cnv.bind('<Button-1>', self.rayon_obsatcles_demo)

        # On dessine le nombre obstable demandé
        for i in range(nbobstacle):
            self.draw_obstacle()

    def draw_obstacle(self):
        """Dessine un obsacle rectangulaire quelconque sur le canas"""

        # Choix aléatoire de la hauteur et largeur de l'obstacle
        width, height = random.randint(10, 60), random.randint(100, 200)
        # Choix aléatoire de ses coordonnées
        maxi = max(width, height)
        x, y = random.randint(maxi, self.width - maxi),\
            random.randint(maxi, self.height - maxi)
        # Choix aléatoire de son angle d'inclinaison
        angle = random.randint(0, 360)
        # Définition des 4 points de l'obstacle
        x1, y1 = x + width, y + height
        A, B, C, D = Point(x, y), Point(x1, y),\
            Point(x1, y1), Point(x, y1)
        # Rotation autour du premier point des autres
        B, C, D = rotation(A, B, angle), rotation(A, C, angle),\
            rotation(A, D, angle)
        self.polygones.append([(A.x, A.y), (B.x, B.y), (C.x, C.y), (D.x, D.y)])
        # Chaque côtés de l'obstacle est un nouveau segment à contrôler
        self.d_to_check.append(Segment(A, B))
        self.d_to_check.append(Segment(B, C))
        self.d_to_check.append(Segment(C, D))
        self.d_to_check.append(Segment(D, A))
        # Création du rectangle
        self.cnv.create_polygon(A.return_tuple(), B.return_tuple(),
                                C.return_tuple(), D.return_tuple(),
                                fill='green')

    def rayon_obsatcles_demo(self, event):
        """Fonction appellée dans le mode demo2 en cas de clic"""

        point = Point(event.x, event.y)
        for polygone in self.polygones:
            if pip.point_in_polygon((event.x, event.y), polygone):
                return
        iro.intersections_rayons_obstacles(self.cnv, point, self.nbrayons,
                                           360, 0, self.d_to_check,
                                           self.mode_demo.get())

    # Fonctions utilisés par le mode de démonstration 1

    def demo1(self):
        """Lancement de la demo 1 : Intersection simple entre deux droites"""

        self.reset()
        # Variables utilisé pour le mode de démonstration 1
        self.state = 1  # Utilisé par la machine à état
        self.nbd = 0
        self.A, self.B = None, None
        self.d = list()

        self.cnv.delete(tk.ALL)
        self.cnv.bind('<Button-1>', self.intersection_deux_droites_demo)
        self.cnv.unbind('<Button-3>')

    def intersection_deux_droites_demo(self, event):
        """Demo : Machine à état pour le dessin des droites"""

        size = 4  # Taille des points dessinés
        # Clic gauche : dessin du point sur le clic
        self.cnv.create_oval(event.x - size, event.y - size, event.x + size,
                             event.y + size, fill='black')
        # State 1 : Premier point du segment
        if self.state == 1:
            self.A = Point(event.x, event.y)
            self.state = 2  # En attente du second point

        # State 2 : Deuxième point du segment
        elif self.state == 2:
            self.B = Point(event.x, event.y)
            # On trace la droite
            self.cnv.create_line(self.A.x, self.A.y, self.B.x, self.B.y,
                                 fill='black')
            # On attend une nouvelle droite
            self.state = 1
            # Compte le nombre de droite en cours de dessin
            self.nbd += 1
            # On mémorise la droite
            self.d.append(Segment(self.A, self.B))

        # Si l'utilisateur a dessiné deux segments
        if self.nbd == 2:
            # On cherche le point d'intersection des deux droites
            I = intersection_droites(self.d[0], self.d[1])
            # On reset la mémoire des deux droites
            self.d = []
            if I is not None:
                # Si un point d'intersection est trouvé on le dessine
                # Condition : le point d'intersection se trouve sur au moins
                # un des deux segments.
                self.cnv.create_oval(I.x - size, I.y - size, I.x + size,
                                     I.y + size, fill='red')
            self.nbd = 0


class Save_popup(tk.Toplevel):
    """Crée une fenêtre popup permettant de sauvegarder le polygon dessiné"""

    width, height = 500, 300
    fichier_config = "config.txt"

    def __init__(self, parent, polygon=None):
        """Prend en argument la fenêtre parent"""

        super().__init__(parent)
        self.title("Gestionnaire de fichiers")
        self.bg = 'white'
        self.lift()
        self.minsize(self.width, self.height)

        if polygon:
            tk.Label(self, text="Sauvegarder le polygon ci-dessous :")\
                .pack(pady=10)
            self.polygon = polygon

            # On récupère le point le plus proche de x=0 et le point le plus
            # proche de y = 0
            min_x, max_x = min(polygon)[0], max(polygon)[0]
            min_y, max_y = min(polygon, key=lambda t: t[1])[1],\
                max(polygon, key=lambda t: t[1])[1]

            # On translate le polygon dans le coin supérieur gauche et
            # redimensionne le polygon par 0.5
            polygonr = list()
            for i in range(len(polygon)):
                polygonr.append(((polygon[i][0] - min_x) * 0.5,
                                (polygon[i][1] - min_y) * 0.5))

            # On affiche le polygon réduit dans un canvas
            self.cnv = tk.Canvas(self, width=(max_x - min_x) * 0.5,
                                 height=(max_y - min_y) * 0.5, bg='white')
            self.cnv.pack()
            self.cnv.create_polygon(polygonr, fill='grey')

        # Création de la zone de commande
        self.frm = tk.Frame(self, width=self.width, height=100, pady=10,
                            relief='ridge', bd=10)
        self.frm.pack(side=tk.BOTTOM)

        if polygon:
            tk.Label(self.frm, text="Options d'enregistrement :")\
                .grid(row=0, column=0, columnspan=3, ipadx=10, ipady=5,
                      sticky='new')

            tk.Button(self.frm, text="Enregistrer le polygon sous",
                      command=self.save_as)\
                .grid(row=1, column=1, ipadx=10, sticky='n', ipady=5)

        self.reponse_b1 = tk.Label(self.frm, text="")
        self.reponse_b1.grid(row=2, column=1, ipadx=10, sticky='n', ipady=5)

        tk.Label(self.frm, text="Modifier le polygon d'un preset :")\
            .grid(row=3, column=1, ipadx=10, sticky='n', ipady=5)

        self.preset = tk.IntVar()
        a = tk.Radiobutton(self.frm, text='Preset 1', variable=self.preset,
                           value=1)
        a.grid(row=4, column=0, ipadx=10, sticky='n', ipady=5)
        a.select()
        tk.Radiobutton(self.frm, text='Preset 2', variable=self.preset,
                       value=2)\
            .grid(row=4, column=1, ipadx=10, sticky='n', ipady=5)
        tk.Radiobutton(self.frm, text='Preset 3', variable=self.preset,
                       value=3)\
            .grid(row=4, column=2, ipadx=10, sticky='n', ipady=5)
        tk.Button(self.frm, text="Modifier le preset", command=self.edit)\
            .grid(row=5, column=1, ipadx=10, sticky='n', ipady=5)

        self.reponse_b2 = tk.Label(self.frm, text="")
        self.reponse_b2.grid(row=6, column=1, ipadx=10, sticky='n', ipady=5)

        tk.Button(self.frm, text="OK", command=self.destroy)\
            .grid(row=7, column=1, ipadx=10, sticky='n', ipady=5)

    def save_as(self):
        """Sauvegarde le polygon dans le fichier demandé par l'utilisateur"""
        # Types de fichier acceptés : seulement .txt dans notre cas
        LST_Types = [("Fichier texte", ".txt")]
        # On ouvre l'explorateur de fichier windows
        emplacement_fichier = tkinter.\
            filedialog.asksaveasfilename(title="Enregistrer sous",
                                         filetypes=LST_Types,
                                         defaultextension=".txt")
        if emplacement_fichier:
            # Si un fichier a été sauvegardé par l'utilisateur
            # On y écrit le polygon dessiné
            with open(emplacement_fichier, 'w') as f:
                f.write(str(self.polygon))
            # On affiche un message de confirmation
            self.reponse_b1.config(text="Fichier correctement enregistré",
                                   fg='green')
        else:
            # Sinon on affiche un message d'erreur
            self.reponse_b1.config(text="Aucun fichier enregistré",
                                   fg='red')
        self.lift()

    def edit(self):
        """Modifie le preset demandé par l'utilisateur"""

        # Types de fichier acceptés : seulement .txt dans notre cas
        LST_Types = [("Fichier texte", ".txt")]
        # On ouvre l'explorateur de fichier windows
        emplacement_fichier = tkinter.\
            filedialog.askopenfilename(title="Ouvrir",
                                       filetypes=LST_Types,
                                       defaultextension=".txt")
        if emplacement_fichier:
            # Si un fichier a été sélectionné, on essaie d'ouvrir le fichier
            # config.tkt
            try:
                # Si ce dernier existe
                lignes_fichier = list()
                with open(self.fichier_config, 'r') as f:
                    # On lis et sauvegarde son contenu
                    for line in f:
                        lignes_fichier.append(line)
                # On modifie la ligne demandée
                string = "Preset" + str(self.preset.get()) + (":") +\
                    emplacement_fichier + "\n"
                lignes_fichier[self.preset.get() - 1] = string
                # On réécrit le fichier
                with open(self.fichier_config, 'w') as f:
                    for line in lignes_fichier:
                        f.write(line)

            except FileNotFoundError:
                # Si config.tkt n'existe pas
                # On le crée
                with open(self.fichier_config, 'w') as f:
                    # On renseigne la valeur du preset sélectionné
                    for i in range(1, 4):
                        emplacement = str()
                        if i == self.preset.get():
                            emplacement = emplacement_fichier
                        string = "Preset" + str(i) + (":") + emplacement + "\n"
                        f.write(string)
            # On affiche un message de confirmation
            self.reponse_b2.config(text="Preset correctement modifié",
                                   fg='green')
        else:
            # Sinon on affiche un message d'erreur
            self.reponse_b2.config(text="Aucun preset modifié",
                                   fg='red')
        self.lift()


Application(1000, 500)
