import pygame
import math
from Model.Obstacle import *
from functools import singledispatch

ROBOT_COLOR = (255, 0, 0)

COLOR_OBSTACLE = (255,5,200)

def afficher_robot(screen, robot):
    """
    Dessine le robot sous forme d'un triangle avec deux roues.
    Les deux roues sont au sommet du triangle et le troisième sommet est à l'arrière.
    """

    # Obtenir la position et la direction du robot
    x, y = robot.x, robot.y
    direction = robot.direction

    # Convertir la position en pixels
    screen_x = int(x)
    screen_y = int(y)

    # Taille du triangle (robot)
    taille_triangle = robot.taille_robot   

    # Calculer les trois points du triangle (les roues aux sommets)
    point1_x = screen_x + taille_triangle * math.cos(direction - math.pi / 2)  # roue gauche
    point1_y = screen_y + taille_triangle * math.sin(direction - math.pi / 2)
    
    point2_x = screen_x + taille_triangle * math.cos(direction + math.pi / 2)  # roue droite
    point2_y = screen_y + taille_triangle * math.sin(direction + math.pi / 2)

    # Le troisième sommet est derrière les roues, donc à l'opposé de la direction
    point3_x = screen_x + taille_triangle * math.cos(direction + math.pi)  # sommet du triangle, opposé à la direction
    point3_y = screen_y + taille_triangle * math.sin(direction + math.pi)

    # Points pour le triangle
    points = [(point1_x, point1_y), (point2_x, point2_y), (point3_x, point3_y)]

    # Dessiner le triangle représentant le robot
    pygame.draw.polygon(screen, ROBOT_COLOR, points)

    # Dessiner les roues aux sommets du triangle
    pygame.draw.circle(screen, (0, 0, 0), (int(point1_x), int(point1_y)), robot.taille_robot // 5)  # roue gauche
    pygame.draw.circle(screen, (0, 0, 0), (int(point2_x), int(point2_y)), robot.taille_robot // 5)  # roue droite

    # Dessiner une ligne indiquant la direction (optionnel, juste pour visualiser la direction)
    pygame.draw.line(screen, (255, 255, 255), (screen_x, screen_y), (int(point3_x), int(point3_y)), 2)


# Définition de la fonction principale avec @singledispatch
# Cette fonction est appelée si aucun type enregistré ne correspond
@singledispatch
def afficher_obstacle(obstacle, screen):
    """ Fonction générique pour afficher un obstacle.
    Si le type de l'obstacle n'est pas reconnu, une erreur est levée.
    """
    raise TypeError(f"Type d'obstacle non pris en charge: {type(obstacle)}")

@afficher_obstacle.register
def _(obstacle: Cercle, screen):
    """
    Affiche un obstacle de type Cercle sur l'écran.
    :param obstacle: Instance de la classe Cercle.
    :param screen: Surface Pygame sur laquelle dessiner.    
    """
    pygame.draw.circle(screen, COLOR_OBSTACLE, obstacle.position, obstacle.rayon)

@afficher_obstacle.register
def _(obstacle: Rectangle, screen):
    """
    Affiche un obstacle de type Rectangle sur l'écran.
    :param obstacle: Instance de la classe Rectangle.
    :param screen: Surface Pygame sur laquelle dessiner.     
    """
    pygame.draw.rect(screen, COLOR_OBSTACLE, (obstacle.position[0], obstacle.position[1], obstacle.dimensions[0], obstacle.dimensions[1]))

def afficher_obstacles(screen, obstacles):
    """
    :param screen: Surface Pygame sur laquelle dessiner.
    :param obstacles: Liste contenant des objets de type Cercle ou Rectangle.
    """
    for obstacle in obstacles:
        afficher_obstacle(obstacle, screen)

def afficher_infos(screen, robot, temps):
    """
    Affiche l'horloge et les vitesses des roues sur l'écran.
    """
    font = pygame.font.Font(None, 30)  # Police par défaut, taille 30
    texte_horloge = font.render(f"Temps: {temps:.2f} s", True, (255, 255, 255))
    texte_vitesse_gauche = font.render(f"Vitesse Gauche: {robot.vitesse_gauche:.2f}", True, (255, 255, 255))
    texte_vitesse_droite = font.render(f"Vitesse Droite: {robot.vitesse_droite:.2f}", True, (255, 255, 255))

    screen.blit(texte_horloge, (10, 10))  # Position en haut à gauche
    screen.blit(texte_vitesse_gauche, (10, 40))  # Juste en dessous
    screen.blit(texte_vitesse_droite, (10, 70))  # Encore en dessous
