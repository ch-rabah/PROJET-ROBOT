import pygame
from Model import *
from View import *

def main():
    environnement = Environnement((0, 800), (0, 600))
    obstacle1 = Obstacle("rectangle", (100, 100), (200, 50))
    obstacle2 = Obstacle("cercle", (500, 200), [30])
    environnement.ajouter_obstacle(obstacle1)
    environnement.ajouter_obstacle(obstacle2)

    # Initialisation de Pygame
    pygame.init()

    # Dimensions de la fenêtre
    WIDTH, HEIGHT = environnement.dimensions_x[1], environnement.dimensions_y[1]
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulation Robot Différentiel avec Obstacles")

    # Initialisation du robot
    robot = Robot(400, 300, direction=0, vitesse_gauche=0, vitesse_droite=0)

    # Boucle principale
    clock = pygame.time.Clock()
    running = True

    while running:
        dt = clock.tick(60) / 1000  # Temps écoulé entre les frames (en secondes)

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        

        # Contrôles clavier
        keys = pygame.key.get_pressed()

        # Modifier les vitesses des roues selon les touches
        if keys[pygame.K_UP]:
            robot.appliquer_vitesse_gauche(10)
            robot.appliquer_vitesse_droite(10)
            robot.avancer(dt) 
        elif keys[pygame.K_DOWN]:
            robot.appliquer_vitesse_gauche(-10)
            robot.appliquer_vitesse_droite(-10)
            robot.avancer(dt) 
        elif keys[pygame.K_RIGHT]:
            robot.appliquer_vitesse_gauche(-4)
            robot.appliquer_vitesse_droite(4)
            robot.avancer(dt) 
        elif keys[pygame.K_LEFT]:
            robot.appliquer_vitesse_gauche(4)
            robot.appliquer_vitesse_droite(-4)
            robot.avancer(dt) 
        else:
            robot.decelerer_robot()
            robot.avancer(dt) 

        # Vérifier les collisions avec les obstacles
        for obstacle in environnement.obstacles:
            if obstacle.detecter_collision(robot):
                print("Collision détectee!")
                robot.arreter_robot()  # Arrêter le robot si collision
                break  # Sortir dès qu'une collision est détectée
    
        if environnement.detecter_sorties(robot):
            print("Sortie du Monde detectee!")
            robot.arreter_robot()
        
        obstacle, distance = robot.cpadistance(environnement)
        if obstacle:
            print(f"Distance a l'obstacle : {distance}")

        # Remplir l'écran avec une couleur de fond
        screen.fill((128, 128, 128))  # Fond gris

        #afficher les informations
        temps = pygame.time.get_ticks() / 1000
        afficher_infos(screen, robot, temps)

        # Affichage des obstacles
        afficher_obstacles(screen, environnement.obstacles)

        # Affichage du robot
        afficher_robot(screen, robot)

        # Mettre à jour l'écran
        pygame.display.flip()

    # Quitter Pygame
    pygame.quit()


if __name__ == "__main__":
    main()
