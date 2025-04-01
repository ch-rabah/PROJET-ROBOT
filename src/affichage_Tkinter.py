from vpython import scene, vector, arrow, box, sphere, cylinder, color, triangle
import math
from model.obstacle import *
from functools import singledispatchmethod

ROBOT_COLOR = color.red
COLOR_OBSTACLE = color.magenta


class SimulationView:
    def __init__(self, environnement, robot):
        self.environnement = environnement
        self.robot = robot

        # Créer une scène VPython
        scene.background = color.lightgrey
        scene.width = 800
        scene.height = 600

        self.trajet = []  # Liste pour stocker les positions du robot

        # Créer un sol pour la scène 3D
        self.sol = box(pos=vector(400, 0, 300), size=vector(800, 1, 600), color=color.green)

        # Créer des variables pour les objets 3D
        self.robot_3d = None
        self.direction_arrow = None
        self.obstacles_3d = []

    def afficher_robot(self):
        """
        Dessine le robot sous forme d'un cylindre avec une flèche indiquant la direction.
        """
        # Supprimer l'ancien robot
        if self.robot_3d:
            self.robot_3d.delete()
        if self.direction_arrow:
            self.direction_arrow.delete()

        x, y = self.robot.x, self.robot.y
        direction = self.robot.direction
        taille_robot = self.robot.taille_robot

        # Le corps du robot (un cylindre)
        self.robot_3d = cylinder(pos=vector(x, 0, y), axis=vector(taille_robot * math.cos(direction), 0, taille_robot * math.sin(direction)),
                                 radius=10, color=ROBOT_COLOR)

        # La flèche indiquant la direction du robot
        self.direction_arrow = arrow(pos=vector(x, 0, y), axis=vector(20 * math.cos(direction), 0, 20 * math.sin(direction)), 
                                     color=color.white, shaftwidth=2)

    @singledispatchmethod
    def afficher_obstacle(self, obstacle):
        """Fonction générique, à définir pour chaque type d'obstacle"""
        raise TypeError(f"Type d'obstacle non géré: {type(obstacle)}")

    @afficher_obstacle.register
    def _(self, obstacle: Rectangle):
        x, y = obstacle.position
        largeur, hauteur = obstacle.dimensions
        # Rectangle en 3D (un box)
        self.rectangle_3d = box(pos=vector(x + largeur / 2, 0, y + hauteur / 2), size=vector(largeur, 1, hauteur), color=COLOR_OBSTACLE)
        self.obstacles_3d.append(self.rectangle_3d)

    @afficher_obstacle.register
    def _(self, obstacle: Cercle):
        x, y = obstacle.position
        r = obstacle.rayon
        # Cercle en 3D (une sphère)
        self.cercle_3d = sphere(pos=vector(x, 0, y), radius=r, color=COLOR_OBSTACLE)
        self.obstacles_3d.append(self.cercle_3d)

    @afficher_obstacle.register
    def _(self, obstacle: Ligne):
        x1, y1 = obstacle.point1
        x2, y2 = obstacle.point2
        # Ligne en 3D (utilisation d'un cylindre pour simuler la ligne)
        self.ligne_3d = cylinder(pos=vector(x1, 0, y1), axis=vector(x2 - x1, 0, y2 - y1), radius=obstacle.largeur / 2, color=COLOR_OBSTACLE)
        self.obstacles_3d.append(self.ligne_3d)

    @afficher_obstacle.register
    def _(self, obstacle: Triangle):
        points = obstacle.get_sommets()
        # Triangle en 3D (utilisation de "points" pour dessiner un triangle)
        self.triangle_3d = triangle(pos=[vector(p[0], 0, p[1]) for p in points],
                                     color=COLOR_OBSTACLE)
        self.obstacles_3d.append(self.triangle_3d)

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
        # Afficher les infos avec un texte flottant dans la scène 3D
        scene.caption = texte

    def mise_a_jour(self, dt):
        self.afficher_infos(dt)

        # Ajouter la position actuelle du robot à la trace
        self.trajet.append((self.robot.x, self.robot.y))

        # Dessiner la trace du robot (lignes rouges)
        for i in range(1, len(self.trajet)):
            x1, y1 = self.trajet[i - 1]
            x2, y2 = self.trajet[i]
            # Dessiner une ligne 3D pour la trajectoire
            line = cylinder(pos=vector(x1, 0, y1), axis=vector(x2 - x1, 0, y2 - y1), radius=5, color=color.red)

        # Mettre à jour le robot
        self.afficher_robot()

        # Mettre à jour la scène à chaque frame
        rate(60)  # Rafraîchissement de la scène à 60 FPS

