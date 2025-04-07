import tkinter as tk
import math
from model.obstacle import Rectangle, Cercle, Ligne, Triangle
from functools import singledispatchmethod


ROBOT_COLOR = "red"
COLOR_OBSTACLE = "magenta"


class SimulationView:
    def __init__(self, root, environnement, robot, robot2 = None):
        self.root = root
        self.environnement = environnement
        self.robot = robot
        self.robot2 = robot2

        self.canvas = tk.Canvas(self.root, width=environnement.dimensions_x[1], height=environnement.dimensions_y[1], bg="lightgrey")
        self.canvas.pack()

        self.trajet = []  # Liste pour stocker les positions du robot

    def afficher_robot(self, robot):
        """
        Dessine le robot sous forme d'un triangle avec deux roues.
        """
        x, y = robot.x, robot.y
        direction = robot.direction
        taille_triangle = robot.taille_robot

        # Calcul des sommets du triangle
        point1_x = x + taille_triangle * math.cos(direction - math.pi / 2)
        point1_y = y + taille_triangle * math.sin(direction - math.pi / 2)

        point2_x = x + taille_triangle * math.cos(direction + math.pi / 2)
        point2_y = y + taille_triangle * math.sin(direction + math.pi / 2)

        point3_x = x + taille_triangle * math.cos(direction + math.pi)
        point3_y = y + taille_triangle * math.sin(direction + math.pi)

        points = [(point1_x, point1_y), (point2_x, point2_y), (point3_x, point3_y)]

        # Dessiner le triangle représentant le robot
        self.canvas.create_polygon(points, fill=ROBOT_COLOR)

        # Dessiner une ligne pour visualiser la direction
        self.canvas.create_line(x, y, point3_x, point3_y, fill="white")

    @singledispatchmethod
    def afficher_obstacle(self, obstacle):
        """Fonction générique, à définir pour chaque type d'obstacle"""
        raise TypeError(f"Type d'obstacle non géré: {type(obstacle)}")

    @afficher_obstacle.register
    def _(self, obstacle: Rectangle):
        x, y = obstacle.position
        largeur, hauteur = obstacle.dimensions
        self.canvas.create_rectangle(x, y, x + largeur, y + hauteur, fill=COLOR_OBSTACLE)

    @afficher_obstacle.register
    def _(self, obstacle: Cercle):
        x, y = obstacle.position
        r = obstacle.rayon
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=COLOR_OBSTACLE)

    @afficher_obstacle.register
    def _(self, obstacle: Ligne):
        x1, y1 = obstacle.point1
        x2, y2 = obstacle.point2
        self.canvas.create_line(x1, y1, x2, y2, fill=COLOR_OBSTACLE, width=obstacle.largeur)

    @afficher_obstacle.register
    def _(self, obstacle: Triangle):
        points = obstacle.get_sommets()
        self.canvas.create_polygon(points, fill=COLOR_OBSTACLE)

    def afficher_obstacles(self):
        """Affiche tous les obstacles de l'environnement"""
        for obstacle in self.environnement.obstacles:
            self.afficher_obstacle(obstacle)  # Appel à la fonction dispatchée

    def afficher_infos(self, temps):
        """
        Affiche les informations sur l'écran.
        """
        texte = f"Temps: {temps:.2f} s\n" \
                f"Vitesse Gauche: {self.robot.vitesse_gauche:.2f}\n" \
                f"Vitesse Droite: {self.robot.vitesse_droite:.2f}"
        self.canvas.create_text(10, 10, text=texte, anchor="nw", fill="white")

    def mise_a_jour(self, dt):
        self.canvas.delete("all")  # Effacer l'écran avant de redessiner
        self.afficher_infos(dt)
        self.afficher_obstacles()

        self.dessine(True, self.bleu())

        self.afficher_robot(self.robot)
        self.afficher_robot(self.robot2)
        self.root.update()

    def dessine(self, b, couleur):

        

        # Ajouter la position actuelle du robot à la trace
        self.trajet.append((self.robot.x, self.robot.y))

        if b:
            # Dessiner la trace du robot (lignes rouges)
            for i in range(1, len(self.trajet)):
                x1, y1 = self.trajet[i - 1]
                x2, y2 = self.trajet[i]
                self.canvas.create_line(x1, y1, x2, y2, fill=couleur, width=2)

    def bleu(self):
        
        return "blue"
    
    def rouge(self):
        return "red"
