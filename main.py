from tkinter import Tk
from View.Affichage_Tkinter import SimulationView
from Model.Robot import Robot
from Model.Environnement import Environnement
from Controller.Control import evitemment
from Model.Obstacle import Rectangle, Cercle
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
    Gère les collisions avec les obstacles et la sortie de l'environnement.
    """
    for obstacle in environnement.obstacles:
        collision = obstacle.detecter_collision(robot)
        if collision:
            print("Collision detectée!")
            robot.arreter_robot()

            dx = obstacle.position[0] - robot.x
            dy = obstacle.position[1] - robot.y
            angle_robot = robot.direction
            angle_obstacle = math.atan2(dy, dx)
            delta_angle = (angle_obstacle - angle_robot + math.pi) % (2 * math.pi) - math.pi

            if -math.pi / 2 <= delta_angle <= math.pi / 2:
                robot.appliquer_vitesse_gauche(-5)
                robot.appliquer_vitesse_droite(-5)
            else:
                robot.appliquer_vitesse_gauche(5)
                robot.appliquer_vitesse_droite(5)

            robot.avancer(dt)
            break

    if environnement.detecter_sorties(robot):
        print("Sortie du Monde dtectée!")
        robot.arreter_robot()
            

def main():
    # Création de l'environnement avec des obstacles
    environnement = Environnement((0, 800), (0, 600))
    obstacle1 = Rectangle((100, 100), (200, 50))
    obstacle2 = Cercle((500, 200), 30)
    environnement.ajouter_obstacle(obstacle1)
    environnement.ajouter_obstacle(obstacle2)

    # Initialisation du robot
    robot = Robot(400, 300, direction=180, vitesse_gauche=0, vitesse_droite=0)

    # Création de la vue de simulation
    simulation = SimulationView(Tk(),environnement, robot)

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

        evitemment(environnement,robot,dt)

        robot.avancer(dt)

        # Mise à jour de la simulation (affichage, autres logiques)
        simulation.mise_a_jour(tempsecouler)

        # Ajouter un délai pour limiter la vitesse de la boucle (par exemple 60 FPS)
        time.sleep(1 / 60)  # ~60 FPS



if __name__ == "__main__":
    main()

