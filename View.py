import pygame
import math

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

def afficher_robot2(screen, robot):
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


def afficher_obstacles(screen, obstacles):
    """
    Affiche tous les obstacles sur l'écran.
    """
    for obstacle in obstacles:
        if obstacle.type_forme == "rectangle":
            pygame.draw.rect(screen, COLOR_OBSTACLE, (obstacle.position[0], obstacle.position[1],
                                                       obstacle.dimensions[0], obstacle.dimensions[1]))
        elif obstacle.type_forme == "cercle":
            pygame.draw.circle(screen, COLOR_OBSTACLE, obstacle.position, obstacle.dimensions[0])

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
