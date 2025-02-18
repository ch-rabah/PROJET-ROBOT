from tkinter import Tk
from View.Affichage_Tkinter import SimulationView
from Model.Robot import Robot
from Model.Environnement import Environnement
from Model.Obstacle import Rectangle, Cercle, Ligne, Triangle
from Controller.Control import evitemment
import time
import math
from pynput import keyboard

# Dictionnaire pour stocker l'état des touches
touches_actives = set()

def on_press(key):
    try:
        touches_actives.add(key.char)
    except AttributeError:
        if key == keyboard.Key.up:
            touches_actives.add('up')
        elif key == keyboard.Key.down:
            touches_actives.add('down')
        elif key == keyboard.Key.left:
            touches_actives.add('left')
        elif key == keyboard.Key.right:
            touches_actives.add('right')

def on_release(key):
    try:
        touches_actives.discard(key.char)
    except AttributeError:
        if key == keyboard.Key.up:
            touches_actives.discard('up')
        elif key == keyboard.Key.down:
            touches_actives.discard('down')
        elif key == keyboard.Key.left:
            touches_actives.discard('left')
        elif key == keyboard.Key.right:
            touches_actives.discard('right')

# Lancer l'écouteur dans un thread séparé
listener = keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()

def gerer_mouvement_robot(robot, dt):
    if 'up' in touches_actives:
        robot.appliquer_vitesse_gauche(10)
        robot.appliquer_vitesse_droite(10)
        if 'right' in touches_actives:
            robot.appliquer_vitesse_gauche(2)
        elif 'left' in touches_actives:
            robot.appliquer_vitesse_droite(2)
    elif 'down' in touches_actives:
        robot.appliquer_vitesse_gauche(-10)
        robot.appliquer_vitesse_droite(-10)
    elif 'right' in touches_actives:
        robot.appliquer_vitesse_gauche(-4)
        robot.appliquer_vitesse_droite(4)
    elif 'left' in touches_actives:
        robot.appliquer_vitesse_gauche(4)
        robot.appliquer_vitesse_droite(-4)
    elif 'z' in touches_actives:
        robot.appliquer_vitesse_gauche(0)
        robot.appliquer_vitesse_droite(8)
    elif 'a' in touches_actives:
        robot.appliquer_vitesse_gauche(8)
        robot.appliquer_vitesse_droite(0)

def gerer_collisions(robot, environnement, dt):
    """
    Gère les collisions avec les obstacles et empêche le robot de les traverser ou de quitter l'environnement.
    """
    for obstacle in environnement.obstacles:
        if obstacle.detecter_collision(robot):
            print("Collision détectée!")
            robot.arreter_robot()
            
            # Recul progressif avec plusieurs petites étapes
            for _ in range(5):  # Essayer de reculer en plusieurs petites étapes
                dx = math.cos(robot.direction) * -1
                dy = math.sin(robot.direction) * -1
                robot.x += dx
                robot.y += dy
                
                # Si le robot n'est plus en collision, on arrête le recul
                if not obstacle.detecter_collision(robot):
                    break
            
            # Vérification après recul, si toujours en collision, forcer l'arrêt
            if obstacle.detecter_collision(robot):
                robot.arreter_robot()
                touches_actives.discard('down')  # Bloquer la marche arrière
            return  # Stopper après la première collision détectée
    
    # Empêcher le robot de sortir des limites de l'environnement
    min_x, max_x = environnement.dimensions_x
    min_y, max_y = environnement.dimensions_y
    if robot.x < min_x:
        robot.x = min_x
        robot.arreter_robot()
    elif robot.x > max_x:
        robot.x = max_x
        robot.arreter_robot()
    if robot.y < min_y:
        robot.y = min_y
        robot.arreter_robot()
    elif robot.y > max_y:
        robot.y = max_y
        robot.arreter_robot()

def main():
    # Création de l'environnement avec des obstacles
    environnement = Environnement((0, 800), (0, 600))
    obstacle1 = Rectangle((100, 100), (200, 50))
    obstacle2 = Cercle((500, 200), 30)
    obstacle3 = Ligne((300, 400), (500, 400), 5)
    obstacle4 = Triangle((600, 300), (650, 350), (700, 300))
    environnement.ajouter_obstacle(obstacle1)
    environnement.ajouter_obstacle(obstacle2)
    environnement.ajouter_obstacle(obstacle3)
    environnement.ajouter_obstacle(obstacle4)

    # Initialisation du robot
    robot = Robot(400, 300, direction=180, vitesse_gauche=0, vitesse_droite=0)

    # Création de la vue de simulation
    simulation = SimulationView(Tk(), environnement, robot)

    # Gestion du temps
    previous_time = time.time()
    tempsecouler = 0

    # Boucle principale
    while True:
        current_time = time.time()
        dt = current_time - previous_time
        previous_time = current_time
        tempsecouler += dt

        # Appeler la fonction pour gérer les collisions
        gerer_collisions(robot, environnement, dt)

        gerer_mouvement_robot(robot, dt)
        #eviter les collisions
        evitemment(environnement,robot,dt)
        robot.avancer(dt)

        # Mise à jour de la simulation (affichage, autres logiques)
        simulation.mise_a_jour(tempsecouler)

        # Ajouter un délai pour limiter la vitesse de la boucle (par exemple 60 FPS)
        time.sleep(1 / 60)  # ~60 FPS

if __name__ == "__main__":
    main()
