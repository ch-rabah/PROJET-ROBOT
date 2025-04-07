import time
from tkinter import Tk
from view.affichage_Tkinter import SimulationView
from model.robot import Robot
from model.environnement import Environnement
from model.obstacle import Rectangle, Cercle, Triangle
from strategy.strategy import StrategyAvancer, StrategyTourner, StrategyConditionnelledistance, StrategySequentielle
from adapter.adapter import RobotAdapterSimulation, RobotAdapterReel
from RobotReel.Robot2I013 import Robot2I013


def main():
    # Initialisation de l'environnement et du robot
    environnement = Environnement((0, 800), (0, 600))

    # Positionnement du robot dans le coin inférieur gauche
    robot = Robot(50, 550, environnement=environnement, direction=0, vitesse_gauche=0, vitesse_droite=0)

    # Ajout des obstacles alignés
    environnement.ajouter_obstacle(Rectangle((350, 300), (100, 50)))  # Rectangle au centre
    environnement.ajouter_obstacle(Cercle((400, 100), 50))            # Cercle en haut au milieu
    environnement.ajouter_obstacle(Triangle((350, 500), (400, 550), (450, 500)))  # Triangle en bas au milieu

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


        

    liste = [StrategyConditionnelledistance(robot_adapter,(tourner,180),(avancer, 20))]*10

    strategy_sequence = StrategySequentielle(robot_adapter, liste)

    while True:
        current_time = time.time()
        dt = current_time - previous_time
        previous_time = current_time
        tempsecouler += dt

         # Exécuter la stratégie actuelle
        if current_strategy_index < len(strategies1):
            current_strategy, param = strategies1[current_strategy_index]
            current_strategy(param)
            current_strategy.execute()

            # Vérifier si la stratégie est terminée
            if current_strategy.est_terminee():
                current_strategy_index += 1

        # Exécuter la stratégie conditionnelle une fois que les stratégies fixes sont terminées
        elif not strategy_sequence.est_terminee():
            print("strategie sequentielle")
            strategy_sequence.execute()
        
        
        elif not strategy_conditionnelle.est_terminee():
            print("strategie conditionnelle")
            strategy_conditionnelle.execute()

        # Mettre à jour l'environnement et l'affichage
        environnement.update(robot, dt)
        simulation.mise_a_jour(tempsecouler)
        time.sleep(1 / 60)


if __name__ == "__main__":
    main()