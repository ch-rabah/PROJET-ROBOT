import time
from tkinter import Tk
from src.view.affichage_Tkinter import SimulationView
from src.model.robot import Robot
from src.model.environnement import Environnement
from src.model.obstacle import Rectangle, Cercle, Ligne, Triangle
from src.strategy.strategy import StrategyAvancer, StrategyTourner, StrategyCarre
from adapter import RobotAdapterSimulation


def main():
    environnement = Environnement((0, 800), (0, 600))

    robot = Robot(400, 300, environnement=environnement, direction=0, vitesse_gauche=0, vitesse_droite=0)
    environnement.ajouter_obstacle(Rectangle((100, 100), (200, 50)))
    environnement.ajouter_obstacle(Triangle((600, 300), (650, 350), (700, 300)))

    robot_adapter = RobotAdapterSimulation(robot)  # Utilisation de l'adaptateur simulation
    simulation = SimulationView(Tk(), environnement, robot)

    current_strategy_index = 0
    previous_time = time.time()
    tempsecouler = 0
    
    strategies = [
        StrategyCarre(robot_adapter, 50),
    ]

    while True:
        current_time = time.time()
        dt = current_time - previous_time
        previous_time = current_time
        tempsecouler += dt

        # Exécuter la stratégie actuelle
        if current_strategy_index < len(strategies):
            current_strategy = strategies[current_strategy_index]
            current_strategy.execute(dt)

            # Vérifier si la stratégie est terminée
            if current_strategy.est_terminee():
                current_strategy_index += 1

        environnement.update(robot, dt)
        simulation.mise_a_jour(tempsecouler)
        time.sleep(1 / 60)


if __name__ == "__main__":
    main()
