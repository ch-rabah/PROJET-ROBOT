
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

    souris = Robot(50, 550, environnement=environnement, direction=0, vitesse_gauche=0, vitesse_droite=0)
    chat = Robot(100, 500, environnement=environnement, direction=0, vitesse_gauche=0, vitesse_droite=0)
    environnement.ajouter_obstacle(Rectangle((0, 0), (200, 50)))
    environnement.ajouter_obstacle(Rectangle((350, 250), (200, 50)))
    environnement.ajouter_obstacle(Rectangle((600, 500), (200, 50)))

    # Création du robot réel (mock-up dans ce cas)
    robot2 = Robot2I013()

    # Création de l'adaptateur pour interagir avec le robot réel
    robot_reel = RobotAdapterReel(robot2)

    robot_adapter_souris = RobotAdapterSimulation(souris)  # Utilisation de l'adaptateur simulation
    robot_adapter_chat = RobotAdapterSimulation(chat)

    simulation = SimulationView(Tk(), environnement, souris, chat)

    # Variables de gestion des stratégies
    current_strategy_index = 0
    previous_time = time.time()
    tempsecouler = 0

    avancer = StrategyAvancer(robot_adapter_souris)
    tourner = StrategyTourner(robot_adapter_souris)

    # Liste des stratégies
    strategies1 = [
        
       
    ]

    # Stratégie conditionnelle
    strategy_conditionnelle = StrategyConditionnelle(
        robot_adapter_souris,
        
        (StrategyTourner,180),
        (StrategyAvancer,600), 
        robot_adapter_souris.get_distance()
    )


    # Création d'une séquence de stratégies pour dessiner le carré
    strategy_sequence = StrategySequentielle(
        robot_adapter_souris, 
        [
            
        ]
    )

    # Boucle principale
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
            strategy_sequence.execute()
        
        
        elif not strategy_conditionnelle.est_terminee():
            strategy_conditionnelle.execute()
        

        
        # Mettre à jour l'environnement et l'affichage
        environnement.update(souris,chat, dt)
        simulation.mise_a_jour(tempsecouler)
        time.sleep(1 / 60)


if __name__ == "__main__":
    main()
