from simulation import *
from affichage import *
import pygame
import sys
import select

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Simulation Robot")
    clock = pygame.time.Clock()
    
    simulation = Simulation()
    running = True
    
    while running:
        dt = clock.tick(60) / 1000  # Temps écoulé en secondes
        
        # Vérifier si une touche a été entrée dans le terminal
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            user_input = sys.stdin.read(1)  # Lire un caractère
            if user_input.strip().lower() == "s":
                print("Arrêt de la simulation.")
                running = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        simulation.step(dt)
        robot, environnement = simulation.get_state()
        
        # Affichage des coordonnées du robot dans le terminal
        print(f"Position du robot - X: {robot.x}, Y: {robot.y}, Direction: {robot.direction}")
        
        #screen.fill((128, 128, 128))  # Fond gris
        #afficher_robot(screen, robot)
        #afficher_obstacles(screen, environnement.obstacles)
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
