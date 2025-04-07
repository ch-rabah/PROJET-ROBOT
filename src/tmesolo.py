import time
import tkinter as tk
from view.affichage_Tkinter import SimulationView
from model.robot import Robot
from model.environnement import Environnement
from model.obstacle import Rectangle

from adapter.adapter import RobotAdapterSimulation

def q1_1():
    root = tk.Tk()
    env = Environnement((0, 800), (0, 600))

    # Ajout des obstacles alignés
    env.ajouter_obstacle(Rectangle((375, 100), (50, 50)))  # Haut
    env.ajouter_obstacle(Rectangle((375, 275), (50, 50)))  # Centre
    env.ajouter_obstacle(Rectangle((375, 450), (50, 50)))  # Bas

    # Création du robot dans le coin inférieur gauche
    robot = Robot(x=50, y=550, environnement=env, direction=0)

    # Vue de la simulation
    view = SimulationView(root, env, robot)
    view.mise_a_jour(0)

    root.mainloop()

if __name__ == "__main__":
    q1_1()
 
