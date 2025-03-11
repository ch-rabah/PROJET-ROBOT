import time
from tkinter import Tk
from src.view.affichage_Tkinter import SimulationView
from src.model.robot import Robot
from src.model.environnement import Environnement
from src.model.obstacle import Rectangle, Cercle, Ligne, Triangle
from src.strategy.strategy import StrategyAvancer, StrategyTourner, StrategyCarre
from adapter import RobotAdapter


def main():
    environnement = Environnement((0, 800), (0, 600))
    

    robot = Robot(400, 300, environnement=environnement, direction=0, vitesse_gauche=0, vitesse_droite=0)
    robot_adapter = RobotAdapter(robot)
    simulation = SimulationView(Tk(), environnement, robot)

    current_strategy_index = 0
    previous_time = time.time()
    tempsecouler = 0
    strategies = [
            StrategyCarre(robot_adapter, 100),
        ]
    """
    strategies = [
        StrategyAvancer(robot_adapter, 200),
        StrategyTourner(robot_adapter, 90),
        StrategyTourner(robot_adapter, -45),
        StrategyAvancer(robot_adapter, 200),
        StrategyTourner(robot_adapter, 360),       
    ]"""

    while True:
        current_time = time.time()
        dt = current_time - previous_time
        previous_time = current_time
        tempsecouler += dt

        # Exécuter la stratégie actuelle
        if current_strategy_index < len(strategies):
            current_strategy = strategies[current_strategy_index]
            if current_strategy(dt):
                # Passer à la stratégie suivante si la stratégie actuelle est terminée
                current_strategy_index += 1

        environnement.update(robot, dt)
        simulation.mise_a_jour(tempsecouler)
        time.sleep(1 / 60)


if __name__ == "__main__":
    main()
