from simulation import *
from affichage import *
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
        
        # Appeler la méthode qui fait avancer le robot en carré
        robot = simulation.robot  # Récupérer l'objet robot
        robot.suivre_carre(dt)  # Faire avancer le robot sur un parcours en carré
        
        # Mettre à jour l'état de la simulation
        simulation.step(dt)
        robot, environnement = simulation.get_state()
        
        # Mise à jour de l'affichage
        screen.fill((128, 128, 128))  # Fond gris
        afficher_robot(screen, robot)  # Afficher le robot
        afficher_obstacles(screen, environnement.obstacles)  # Afficher les obstacles
        pygame.display.flip()  # Rafraîchir l'écran
    
    pygame.quit()

if __name__ == "__main__":
    main()
