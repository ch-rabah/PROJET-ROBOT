import time
from tkinter import Tk
from src.view.affichage_Tkinter import SimulationView
from src.model.robot import Robot
from src.model.environnement import Environnement
from src.model.obstacle import Rectangle, Cercle, Ligne, Triangle
from src.strategy.strategy import StrategyAvancer, StrategyTourner, StrategyCarre
from adapter import RobotAdapter


def main():
    # Initialisation de l'environnement et du robot
    environnement = Environnement((0, 800), (0, 600))
    
    robot = Robot(400, 300, environnement=environnement, direction=0, vitesse_gauche=0, vitesse_droite=0)
    environnement.ajouter_obstacle(Rectangle((100, 100), (200, 50)))
    #environnement.ajouter_obstacle(Cercle((500, 200), 30))
    environnement.ajouter_obstacle(Triangle((600, 300), (650, 350), (700, 300)))
    
    robot_adapter = RobotAdapter(robot)
    simulation = SimulationView(Tk(), environnement, robot)

    # Variables de gestion des stratégies
    current_strategy_index = 0
    previous_time = time.time()
    tempsecouler = 0

    # Liste des stratégies : plusieurs carrés avec différentes tailles
    strategies = [
        StrategyCarre(robot_adapter, 100),  # Premier carré
        StrategyCarre(robot_adapter, 150),  # Deuxième carré
        """StrategyCarre(robot_adapter, 200),  # Troisième carré
        StrategyCarre(robot_adapter, 250),  # Quatrième carré"""
    ]
    
    # Boucle principale
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

        # Mettre à jour l'environnement et l'affichage
        environnement.update(robot, dt)
        simulation.mise_a_jour(tempsecouler)
        
        # Limiter la vitesse de mise à jour pour simuler 60 FPS
        time.sleep(1 / 60)


if __name__ == "__main__":
    main()

