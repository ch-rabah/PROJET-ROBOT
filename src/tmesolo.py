import time
from tkinter import Tk
from view.affichage_Tkinter import SimulationView
from model.robot import Robot
from model.environnement import Environnement
from model.obstacle import Rectangle, Cercle, Ligne, Triangle
from strategy.strategy import StrategyAvancer, StrategyTourner, StrategyConditionnelle, StrategySequentielle
from adapter.adapter import RobotAdapterSimulation , RobotAdapterReel
from RobotReel.Robot2I013 import Robot2I013


def q1_1():

    environnement.ajouter_obstacle(Rectangle((370, 80), (60, 40)))   
    environnement.ajouter_obstacle(Cercle((400, 300), 30))           
    environnement.ajouter_obstacle(Rectangle((370, 480), (60, 40)))

    # Initialisation
    environnement = Environnement((0, 800), (0, 600))
    robot = Robot(50, 550, environnement=environnement, direction=0)

    # Simulation
    robot_adapter = RobotAdapterSimulation(robot)
    simulation = SimulationView(Tk(), environnement, robot)

    # Nouvelle stratégie unique : aller-retour
    strategy_aller_retour = StrategyBoucleAllerRetour(
        robot_adapter,
        distance_max=200,
        seuil_proximite=50,
    )

    # Boucle principale
    previous_time = time.time()
    tempsecouler = 0

    while not strategy_aller_retour.est_terminee():
        current_time = time.time()
        dt = current_time - previous_time
        previous_time = current_time
        tempsecouler += dt

        strategy_aller_retour.execute()

        environnement.update(robot, dt)
        simulation.mise_a_jour(tempsecouler)
        time.sleep(1 / 60)

    print("Stratégie terminée.")



def q1_2():

    # Initialisation
    environnement = Environnement((0, 800), (0, 600))
    robot = Robot(50, 550, environnement=environnement, direction=0)

    environnement.ajouter_obstacle(Cercle((400, 300), 30))           


    # Simulation
    robot_adapter = RobotAdapterSimulation(robot)
    simulation = SimulationView(Tk(), environnement, robot)

    # Nouvelle stratégie unique : aller-retour
    strategy_aller_retour = StrategyBoucleAllerRetour(
        robot_adapter,
        distance_max=200,
        seuil_proximite=50,
    )

    # Boucle principale
    previous_time = time.time()
    tempsecouler = 0

    while not strategy_aller_retour.est_terminee():
        current_time = time.time()
        dt = current_time - previous_time
        previous_time = current_time
        tempsecouler += dt

        strategy_aller_retour.execute()

        environnement.update(robot, dt)
        simulation.mise_a_jour(tempsecouler, True)
        time.sleep(1 / 60)

    print("Stratégie terminée.")



def q1_3():

    def dessine(b: bool, robot: Robot):
        robot.trace_active = b; 



    def main():
        # Initialisation de l'environnement et du robot
        environnement = Environnement((0, 800), (0, 600))

        robot = Robot(400, 300, environnement=environnement, direction=0, vitesse_gauche=0, vitesse_droite=0)
        environnement.ajouter_obstacle(Rectangle((100, 100), (200, 50)))
        environnement.ajouter_obstacle(Triangle((600, 300), (650, 350), (700, 300)))

        dessine(True)

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



    