import pygame
from Constante import *

class Robot:
    def __init__(self, x, y, image_path, environment):
        self.x = x
        self.y = y
        self.vitesse = 1  # Nombre de cellules par mouvement
        self.direction = "droite"  # Direction initiale
        self.image = pygame.image.load(image_path).convert_alpha()  
        self.image = pygame.transform.scale(self.image, (CELL_SIZE, CELL_SIZE))
        self.image.set_colorkey((255, 255, 255))  # Définit le blanc comme couleur transparente
        self.environment = environment

    def avancer(self):
        """Déplace le robot dans la direction actuelle, sauf si un obstacle bloque"""
        new_x, new_y = self.x, self.y

        if self.direction == "haut" and self.y > 0:
            new_y -= self.vitesse
        elif self.direction == "bas" and self.y < WORLD_SIZE - 1:
            new_y += self.vitesse
        elif self.direction == "droite" and self.x < WORLD_SIZE - 1:
            new_x += self.vitesse
        elif self.direction == "gauche" and self.x > 0:
            new_x -= self.vitesse

        if not self.environment.is_obstacle(new_x, new_y):
            self.x, self.y = new_x, new_y

    def tourner_a_droite(self):
        """Fait tourner le robot à droite"""
        directions = ["haut", "droite", "bas", "gauche"]
        index = directions.index(self.direction)
        self.direction = directions[(index + 1) % 4]

    def tourner_a_gauche(self):
        """Fait tourner le robot à gauche"""
        directions = ["haut", "droite", "bas", "gauche"]
        index = directions.index(self.direction)
        self.direction = directions[(index - 1) % 4]

    def draw(self, screen):
        """Dessine le robot sur l'écran avec un fond blanc"""
        # Dessiner un carré blanc derrière l'image du robot
        pygame.draw.rect(screen, WHITE, (self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        screen.blit(self.image, (self.x * CELL_SIZE, self.y * CELL_SIZE))