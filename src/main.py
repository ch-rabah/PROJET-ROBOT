import time
from tkinter import Tk
from view.affichage_Tkinter import SimulationView
from model.robot import Robot
from model.environnement import Environnement
from model.obstacle import Rectangle, Cercle, Ligne, Triangle
from strategy.strategy import StrategyAvancer, StrategyTourner, StrategyConditionnelle, StrategySequentielle
from adapter.adapter import RobotAdapterSimulation , RobotAdapterReel
from RobotReel.Robot2I013 import Robot2I013


def main():
    # Initialisation de l'environnement et du robot
    environnement = Environnement((0, 800), (0, 600))

    robot = Robot(400, 300, environnement=environnement, direction=0, vitesse_gauche=0, vitesse_droite=0)
    environnement.ajouter_obstacle(Rectangle((100, 100), (200, 50)))
    environnement.ajouter_obstacle(Triangle((600, 300), (650, 350), (700, 300)))

    # Création du robot réel (mock-up dans ce cas)
    robot2 = Robot2I013()

    # Création de l'adaptateur pour interagir avec le robot réel
    robot_reel = RobotAdapterReel(robot2)

    robot_adapter = RobotAdapterSimulation(robot)  # Utilisation de l'adaptateur simulation

    simulation = SimulationView(Tk(), environnement, robot)

    # Variables de gestion des stratégies
    current_strategy_index = 0
    previous_time = time.time()
    tempsecouler = 0

    avancer = StrategyAvancer(robot_adapter)
    tourner = StrategyTourner(robot_adapter)

    # Liste des stratégies
    strategies1 = [
        (avancer, 25),
        (tourner, -90)
       
    ]

    # Stratégie conditionnelle
    strategy_conditionnelle = StrategyConditionnelle(
        robot_adapter,
        (StrategyAvancer,20), 
        (StrategyTourner,90),
        False
    )


    # Création d'une séquence de stratégies pour dessiner le carré
    strategy_sequence = StrategySequentielle(
        robot_adapter, 
        [
            (StrategyAvancer,40),
            (StrategyTourner, 90),
            (StrategyAvancer,40),
            (StrategyTourner, 90),
            (StrategyAvancer,40),
            (StrategyTourner, 90),
            (StrategyAvancer,40),
            (StrategyTourner, 90),
            (StrategyAvancer,40),
        ]
    )

    # Boucle principale
    while True:
        current_time = time.time()
        dt = current_time - previous_time
        previous_time = current_time
        tempsecouler += dt
        
        strategy_sequence.execute()

        # Mettre à jour l'environnement et l'affichage
        environnement.update(robot, dt)
        simulation.mise_a_jour(tempsecouler)
        time.sleep(1 / 60)


if __name__ == "__main__":
    main()