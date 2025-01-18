import pygame

# Dimensions de la fenêtre et de la matrice
WINDOW_SIZE = 400  # Taille de la fenêtre (400x400 pixels)
WORLD_SIZE = 20  # Taille de la matrice (20x20)
CELL_SIZE = WINDOW_SIZE // WORLD_SIZE  # Taille d'une cellule

# Couleurs
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)

class Environment:
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = [[0 for _ in range(grid_size)] for _ in range(grid_size)]

    def draw(self, screen):
        """Dessine la matrice sur l'écran"""
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                color = WHITE
                pygame.draw.rect(screen, color, 
                                 (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, GRAY, 
                                 (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

# Initialisation de Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("Projet")
clock = pygame.time.Clock()

# Création de l'environnement
env = Environment(WORLD_SIZE)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dessin de la matrice
    screen.fill(WHITE)
    env.draw(screen)
    
    pygame.display.flip()
    clock.tick(30)

pygame.quit()
