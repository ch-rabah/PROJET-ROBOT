import pygame
import math
from Model import Robot

# Initialisation de pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation Robot")

# Couleur pour le robot (rouge)
ROBOT_COLOR = (255, 0, 0)

# Fonction pour afficher le robot (représenté par un triangle orienté dans la direction du robot)
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
    screen.fill((0, 0, 0))
    pygame.draw.polygon(screen, ROBOT_COLOR, [p1, p2, p3])

def carrer(robot):
    # Boucle principale du jeu
    running = True
    actions_restantes = 4  # Le robot fera 4 cycles d'avancer et de tourner
    temps_avance = 2  # Temps pour avancer (en secondes)
    mode = "avance"  # Le mode initial est "avance"
    temps_ecoule = 0  # Temps accumulé dans l'action actuelle
    dt = 0  # Delta temps

    rotation_en_cours = False
    angle_cumule = 0  # Pour suivre l'angle cumulé pendant la rotation

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
                mode = "tourne"
                temps_ecoule = 0
                rotation_en_cours = True
                angle_cumule = 0  # Réinitialiser l'angle accumulé

            if mode == "tourne":
                rotation_terminee, angle_cumule = Robot.tourner(robot, 90, 1, dt, angle_cumule)
                if rotation_terminee:
                    mode = "avance"
                    actions_restantes -= 1
                    temps_ecoule = 0

            if mode == "avance":
                robot.avancer(dt)

        # Effacer l'écran et afficher le robot
        afficher_robot(robot)

        # Mettre à jour l'écran
        pygame.display.flip()



# Création du robot
robot = Robot(x=400, y=300, vx=100, vy=0)  # Vitesse initiale vers la droite

clock = pygame.time.Clock()

carrer(robot)


# Quitter pygame
pygame.quit()