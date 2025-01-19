import pygame
from Constante import *

class  Environnement:
    def __init__(self, grid_size, obstacles):
        self.grid_size = grid_size
        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        self.obstacles = obstacles  # Liste des coordonnées des obstacles

    def draw(self, screen):
        """Dessine l'arrière-plan uni et les obstacles"""
        screen.fill(BLACK)
        for obstacle in self.obstacles:
            ox, oy = obstacle
            pygame.draw.rect(screen, RED, (ox * CELL_SIZE, oy * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def is_obstacle(self, x, y):
        """Vérifie si une cellule contient un obstacle"""
        return (x, y) in self.obstacles
