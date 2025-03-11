import time
from tkinter import Tk
from src.view.affichage_Tkinter import SimulationView
from src.model.robot import Robot
from src.model.environnement import Environnement
from src.model.obstacle import Rectangle, Cercle, Ligne, Triangle
from src.strategy.strategy import StrategyAvancer, StrategyTourner, StrategyCarre
from adapter import RobotAdapter


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
        robot.avancer(dt)

        # Mise à jour de la simulation (affichage, autres logiques)
        simulation.mise_a_jour(tempsecouler)

        # Ajouter un délai pour limiter la vitesse de la boucle (par exemple 60 FPS)
        time.sleep(1 / 60)  # ~60 FPS

if __name__ == "__main__":
    main()
