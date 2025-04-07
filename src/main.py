import time
from tkinter import Tk
from view.affichage_Tkinter import SimulationView
from model.robot import Robot
from model.environnement import Environnement
from model.obstacle import Rectangle, Cercle, Ligne, Triangle
from strategy.strategy import StrategyAvancer, StrategyTourner, StrategyConditionnelle, StrategySequentielle, StrategyZigZagObstacle
from adapter.adapter import RobotAdapterSimulation , RobotAdapterReel
from RobotReel.Robot2I013 import Robot2I013


def main():
    # Initialisation de l'environnement et du robot
    environnement = Environnement((0, 800), (0, 800))

    robot = Robot(30, 770, environnement=environnement, direction=0, vitesse_gauche=0, vitesse_droite=0)
    environnement.ajouter_obstacle(Rectangle((400-200/2, 400-50/2), (200, 50))) #au centre
    environnement.ajouter_obstacle(Cercle((400,100),50))
    environnement.ajouter_obstacle(Cercle((400,780),50))
    environnement.ajouter_obstacle(Ligne((0,0),(0,800),5))
    environnement.ajouter_obstacle(Ligne((0,0),(800,0),5))
    environnement.ajouter_obstacle(Ligne((800,0),(800,800),5))
    environnement.ajouter_obstacle(Ligne((0,800),(800,800),5))

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
        ]
    )

    strategie = StrategyZigZagObstacle(robot_adapter,environnement,simulation)


    tmp=0
    # Boucle principale
    while True:
        current_time = time.time()
        dt = current_time - previous_time
        previous_time = current_time
        tempsecouler += dt
        
        
        if not strategie.est_terminee():
            strategie.execute()
        
        # Mettre à jour l'environnement et l'affichage
        environnement.update(robot, dt)
        simulation.mise_a_jour(tempsecouler, True)
        time.sleep(1 / 60)
        if tmp==100:
            robot.rouge()
        tmp+=1



if __name__ == "__main__":
    main()
    """
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
        """