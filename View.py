import tkinter as tkimport math
from Model.Obstacle import *
from functools import singledispatch

ROBOT_COLOR = "red"

COLOR_OBSTACLE = "magenta"

class SimulationView:
    def __init__(self, root, environnement, robot):
        self.root = root
        self.environnement = environnement
        self.robot = robot

        self.canvas = tk.Canvas(self.root, width=environnement.dimensions_x[1], height=environnement.dimensions_y[1], bg="lightgrey")
        self.canvas.pack()

    def afficher_robot(self):
        """
        Dessine le robot sous forme d'un triangle avec deux roues.
        """
        x, y = self.robot.x, self.robot.y
        direction = self.robot.direction
        taille_triangle = self.robot.taille_robot

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
