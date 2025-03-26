from vpython import *
import time
from view.camera_orbitale import CameraOrbitale
from model.obstacle import Rectangle, Sphere, Triangle, Ligne
from functools import singledispatchmethod
import math

class SimulationView3D:
    def __init__(self, environnement, robot):
        self.environnement = environnement
        self.robot = robot
        self.scene = canvas(title="Simulation 3D Robot", width=800, height=600, center=vector(0, 0, 0), background=color.gray(0.2))

        # Dimensions de l'environnement
        x_min, x_max = self.environnement.dimensions_x
        y_min, y_max = self.environnement.dimensions_y
        size_x = x_max - x_min
        size_z = y_max - y_min
        center_x = (x_max + x_min) / 2
        center_z = (y_max + y_min) / 2

        # Créer un sol quadrillé qui correspond à la taille de l'environnement
        self.sol = box(pos=vector(center_x, -0.1, center_z), size=vector(size_x, 0.1, size_z), color=color.white, opacity=0.5)

        # Initialisation de la caméra orbitale centrée sur le sol
        self.camera_orbitale = CameraOrbitale(scene=self.scene, target=vector(center_x, 0, center_z))

        # Texte d'information (en haut à gauche de l'écran, en dehors de la scène 3D)
        self.info_label = wtext(text='', style={'font-family': 'sans-serif', 'color': 'white', 'font-size': '14px'})
        self.scene.append_to_caption("\n")

        self.obstacle_entities = []
        self.afficher_obstacles()

    def afficher_infos(self, temps):
        texte = f"Temps écoulé : {temps:.2f} s\n"
        texte += f"Vitesse gauche : {self.robot.vitesse_gauche:.2f}\n"
        texte += f"Vitesse droite : {self.robot.vitesse_droite:.2f}"
        self.info_label.text = texte.replace('\n', '<br>')

    def afficher_robot(self):
        if hasattr(self, 'objet_robot'):
            self.objet_robot.visible = False

        taille = self.robot.taille_robot * 0.3
        angle = self.robot.direction

        # Définir les 3 sommets du triangle
        p1 = vector(self.robot.x + taille * math.cos(angle), 0.2, self.robot.y + taille * math.sin(angle))
        p2 = vector(self.robot.x + taille * math.cos(angle + 2.5), 0.2, self.robot.y + taille * math.sin(angle + 2.5))
        p3 = vector(self.robot.x + taille * math.cos(angle - 2.5), 0.2, self.robot.y + taille * math.sin(angle - 2.5))

        self.objet_robot = triangle(
            v0=vertex(pos=p1, color=color.blue),
            v1=vertex(pos=p2, color=color.blue),
            v2=vertex(pos=p3, color=color.blue)
        )

    @singledispatchmethod
    def afficher_obstacle(self, obstacle):
        raise TypeError(f"Type d'obstacle non géré: {type(obstacle)}")

    @afficher_obstacle.register
    def _(self, obstacle: Rectangle):
        x, y = obstacle.position
        l, h = obstacle.dimensions
        obj = box(pos=vector(x + l/2, 0.5, y + h/2), size=vector(l, 1, h), color=color.magenta)
        self.obstacle_entities.append(obj)

    @afficher_obstacle.register
    def _(self, obstacle: Sphere):
        x, y = obstacle.position
        r = obstacle.rayon
        obj = sphere(pos=vector(x, r, y), radius=r, color=color.magenta)
        self.obstacle_entities.append(obj)

    @afficher_obstacle.register
    def _(self, obstacle: Ligne):
        x1, y1 = obstacle.point1
        x2, y2 = obstacle.point2
        dx, dz = x2 - x1, y2 - y1
        obj = cylinder(pos=vector(x1, 0.5, y1), axis=vector(dx, 0, dz), radius=obstacle.largeur / 2, color=color.magenta)
        self.obstacle_entities.append(obj)

    @afficher_obstacle.register
    def _(self, obstacle: Triangle):
        p1, p2, p3 = [vector(x, 0.01, y) for x, y in obstacle.get_sommets()]
        tri = triangle(v0=vertex(pos=p1, color=color.magenta),
                       v1=vertex(pos=p2, color=color.magenta),
                       v2=vertex(pos=p3, color=color.magenta))
        self.obstacle_entities.append(tri)

    def afficher_obstacles(self):
        for obs in self.environnement.obstacles:
            self.afficher_obstacle(obs)

    def mise_a_jour(self, temps):
        self.afficher_infos(temps)
        self.camera_orbitale.update()
        self.afficher_robot()

    def run(self):
        t0 = time.time()
        while True:
            rate(60)
            t = time.time() - t0
            self.mise_a_jour(t)