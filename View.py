import pygame
import math

ROBOT_COLOR = (255, 0, 0)

COLOR_OBSTACLE = (255,5,200)


def afficher_robot(screen, robot):
    """
    Dessine le robot sous forme d'un cercle avec une direction.
    """

    # Obtenir la position et la direction du robot
    x, y = robot.x,robot.y
    direction = robot.direction

    # Convertir la position en pixels
    screen_x = int(x)
    screen_y = int(y)

    # Dessiner le robot
    pygame.draw.circle(screen, ROBOT_COLOR, (screen_x, screen_y), robot.taille_robot)

    # Dessiner une ligne indiquant la direction
    ligne_x = int(screen_x + robot.taille_robot * math.cos(direction))
    ligne_y = int(screen_y + robot.taille_robot * math.sin(direction))
    pygame.draw.line(screen, (255, 255, 255), (screen_x, screen_y), (ligne_x, ligne_y), 2)