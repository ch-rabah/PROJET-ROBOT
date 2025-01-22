import pygame
import math
from Model import *

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation Robot")

# Couleur pour le robot (rouge)
ROBOT_COLOR = (255, 0, 0)

# Fonction pour afficher le robot (représenté par un cercle)
def afficher_robot(robot):
    """
    Affiche le robot sous forme d'un triangle orienté dans la direction du robot.
    """
    # Obtenir la position et la direction du robot
    x, y = robot.obtenir_position()
    direction = robot.obtenir_direction()

    # Convertir la position en pixels
    screen_x = int(x)
    screen_y = int(y)

    # Taille du triangle (en pixels)
    longueur = 20  # Longueur de la pointe
    largeur = 20   # Largeur de la base

    # Calculer les trois points du triangle
    # Pointe avant (dirigée selon `direction`)
    p1 = (
        screen_x + longueur * math.cos(-direction),
        screen_y - longueur * math.sin(-direction),
    )
    # Base arrière gauche (ajustée avec la largeur)
    p2 = (
        screen_x - (longueur / 2) * math.cos(-direction) + (largeur / 2) * math.sin(-direction),
        screen_y + (longueur / 2) * math.sin(-direction) + (largeur / 2) * math.cos(-direction),
    )
    # Base arrière droite (ajustée avec la largeur)
    p3 = (
        screen_x - (longueur / 2) * math.cos(-direction) - (largeur / 2) * math.sin(-direction),
        screen_y + (longueur / 2) * math.sin(-direction) - (largeur / 2) * math.cos(-direction),
    )

    # Dessiner le triangle
    pygame.draw.polygon(screen, ROBOT_COLOR, [p1, p2, p3])


# Création du robot
robot = Robot(x=400, y=300, vx=100, vy=0)  # Vitesse initiale vers la droite

# Variables pour contrôler la boucle d'action
actions_restantes = 4  # Le robot fera 4 cycles d'avancer et de tourner
temps_avance = 2  # Temps pour avancer (en secondes)
temps_tourne = 1  # Temps pour effectuer la rotation
mode = "avance"  # Le mode initial est "avance"
temps_ecoule = 0  # Temps accumulé dans l'action actuelle

# Boucle principale du jeu
clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60) / 1000  # Temps écoulé entre les frames en secondes

    # Gestion des événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Exécuter les actions du robot
    if actions_restantes > 0:
        temps_ecoule += dt

        if mode == "avance" and temps_ecoule >= temps_avance:
            # Passer au mode "tourne" après avoir avancé
            mode = "tourne"
            temps_ecoule = 0
            robot.tourner(90)  # Tourner de 90 degrés

        elif mode == "tourne" and temps_ecoule >= temps_tourne:
            # Passer au mode "avance" après avoir tourné
            mode = "avance"
            temps_ecoule = 0
            actions_restantes -= 1  # Réduire le nombre d'actions restantes

        if mode == "avance":
            # Faire avancer le robot
            robot.avancer(dt)

    # Effacer l'écran (fond noir)
    screen.fill((0, 0, 0))

    # Afficher le robot
    afficher_robot(robot)

    # Mettre à jour l'écran
    pygame.display.flip()

# Quitter pygame
pygame.quit()
