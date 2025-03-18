import time
from tkinter import Tk
from src.view.affichage_Tkinter import SimulationView
from src.model.robot import Robot
from src.model.environnement import Environnement
from src.model.obstacle import Rectangle, Cercle, Ligne, Triangle
from src.strategy.strategy import StrategyAvancer, StrategyTourner, StrategyCarre, StrategyConditionnel
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

    avancer = StrategyAvancer(robot_adapter)
    tourner = StrategyTourner(robot_adapter)
    carre = StrategyCarre(robot_adapter)

    def condition_tourner():
        """Condition pour activer la stratégie de rotation"""
        return robot.direction % 180 == 0  # Exemple : tourne si le robot est aligné avec les axes

    def condition_avancer():
        """Condition pour activer la stratégie d'avancer"""
        return robot.x < 500  # Exemple : avance tant qu'il est à gauche de x = 500

    def condition_carre():
        """Condition pour activer la stratégie du carré"""
        return robot.y > 400  # Exemple : fait un carré si y > 400
    
    strategies1 = [
        (avancer, 50),
        (tourner, -90),
    ]

    strategy_conditionnel = StrategyConditionnel(
        robot_adapter,
        distance_cible=100,
        angle_degrees=90,
        distance_cote=50,
        condition_tourner=False,
        condition_avancer=False,
        condition_carre=True,
    )

    while True:
        current_time = time.time()
        dt = current_time - previous_time
        previous_time = current_time
        tempsecouler += dt

        # Exécuter la stratégie actuelle
        if current_strategy_index < len(strategies1):
            current_strategy, param = strategies1[current_strategy_index]
            current_strategy(param)
            current_strategy.execute(dt)

            # Vérifier si la stratégie est terminée
            if current_strategy.est_terminee():
                current_strategy_index += 1

        # Exécuter la stratégie conditionnelle une fois que les stratégies fixes sont terminées
        elif not strategy_conditionnel.est_terminee():
            strategy_conditionnel.execute(dt)

        environnement.update(robot, dt)
        simulation.mise_a_jour(tempsecouler)
        time.sleep(1 / 60)


if __name__ == "__main__":
    main()
