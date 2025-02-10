from simulation import *
from View import *
import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Simulation Robot")
    clock = pygame.time.Clock()
    
    simulation = Simulation()
    running = True
    
    while running:
        dt = clock.tick(60) / 1000  # Temps écoulé en secondes
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        simulation.step(dt)
        robot, environnement = simulation.get_state()
        
        screen.fill((128, 128, 128))  # Fond gris
        afficher_robot(screen, robot)
        afficher_obstacles(screen, environnement.obstacles)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
