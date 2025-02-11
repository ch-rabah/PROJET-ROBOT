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