import pygame
from Constante import *
from Environnement   import *
from Robot  import *

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Simulation Robot")
clock = pygame.time.Clock()

# Chemin de l'image du robot
robot_image_path = "RobotSmile.png"  # Remplacez par le chemin de votre image

# Liste des obstacles (exemple : obstacles à des positions spécifiques)
obstacles = [(5, 5), (6, 5), (7, 5), (10, 9), (15, 15)]

# Création de l'environnement et du robot
env = Environnement(WORLD_SIZE, obstacles)  
robot = Robot(x=10, y=10, image_path=robot_image_path, environment=env)  
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Gestion des touches pour contrôler le robot
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        robot.direction = "haut"
        robot.avancer()
    elif keys[pygame.K_DOWN]:
        robot.direction = "bas"
        robot.avancer()
    elif keys[pygame.K_LEFT]:
        robot.direction = "gauche"
        robot.avancer()
    elif keys[pygame.K_RIGHT]:
        robot.direction = "droite"
        robot.avancer()

    # Dessiner l'environnement et le robot
    env.draw(screen)
    robot.draw(screen)

    pygame.display.flip()
    clock.tick(10)  # Limiter à 10 FPS

pygame.quit()
