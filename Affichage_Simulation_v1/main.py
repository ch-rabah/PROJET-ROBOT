from simulation import *
from affichage import *
import pygame
import time
import sys
import select

def main():
    #pygame.init()
    #screen = pygame.display.set_mode((800, 600))
    #pygame.display.set_caption("Simulation Robot")

    simulation = Simulation()
    running = True
    
    last_time = time.time()  # Temps initial
    
    while running:
        current_time = time.time()
        dt = current_time - last_time  # Calcul du delta temps
        last_time = current_time  # Mise à jour du dernier temps

        # Vérifier si une touche a été entrée dans le terminal
        if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
            user_input = sys.stdin.read(1)  # Lire un caractère
            if user_input.strip().lower() == "s":
                print("Arrêt de la simulation.")
                running = False

        #for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        running = False

        simulation.step(dt)
        robot, environnement = simulation.get_state()

        # Affichage des coordonnées du robot dans le terminal
        print(f"Position du robot - X: {robot.x}, Y: {robot.y}, Direction: {robot.direction}")

        # Rafraîchissement de l'affichage
        #screen.fill((128, 128, 128))  # Fond gris
        #afficher_robot(screen, robot)
        #afficher_obstacles(screen, environnement.obstacles)
        #pygame.display.flip()

        # Limiter la fréquence d'exécution pour éviter une surconsommation CPU
        time.sleep(1/60)  # Simule une fréquence d'environ 60 FPS

    #pygame.quit()
    print("Fin de la simulation.")

if __name__ == "__main__":
    main()
