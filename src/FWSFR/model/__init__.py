from .environnement import Environnement
from .robot import Robot
from .obstacle import Rectangle, Triangle, Ligne, Cercle
from .balise import Balise
from math import pi


def initialiser_environnement_robot():
    env = Environnement((0, 200), (0, 200))
    env.ajouter_obstacle(Rectangle((20, 20), (20, 10)))
    env.ajouter_obstacle(Cercle((60, 120), 5))
    env.ajouter_obstacle(Ligne((20, 160), (180, 160), largeur=1))
    env.ajouter_obstacle(Triangle((20, 70), (30, 90), (40, 70)))
    
    robot = Robot(x=150, y=100, environnement=env, direction=pi/2)

    env.ajouter_balise(Balise(position=(90, 130), taille=10, hauteur=5, rotation=-90))
    #env.ajouter_balise(Balise(position=(200, 50), taille=10, hauteur=5, rotation=90))

    
    return env,robot 
