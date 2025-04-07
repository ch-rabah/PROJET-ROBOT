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

        # Positionnement du robot dans le coin inférieur gauche
        robot = Robot(50, 550, environnement=environnement, direction=0, vitesse_gauche=0, vitesse_droite=0)

        # Ajout des obstacles alignés
        environnement.ajouter_obstacle(Rectangle((350, 300), (100, 50)))  # Rectangle au centre
        environnement.ajouter_obstacle(Cercle((400, 100), 50))            # Cercle en haut au milieu
        environnement.ajouter_obstacle(Triangle((350, 500), (400, 550), (450, 500)))  # Triangle en bas au milieu

        # Variables pour le traçage
        dessine = True
        couleur = "red"

        def changer_couleur(x):
            dessine
            dessine = x

        def rouge():
            nonlocal couleur
            couleur = "red"

        def bleu():
            nonlocal couleur
            couleur = "blue"


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


        strategy_conditionnelle = StrategyConditionnelle(
            robot_adapter,
            (StrategyTourner,90)
            (StrategyAvancer,20), 
            robot_adapter.get_distance()
        )


        # Création d'une séquence de stratégies pour dessiner le carré
        strategy_sequence = StrategySequentielle(
            robot_adapter, 
            [   
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
            

            if not strategy_sequence.est_terminee():
                strategy_sequence.execute()
            
            changer_couleur(True)
            bleu()


            # Mettre à jour l'environnement et l'affichage
            environnement.update(robot, dt)
            simulation.mise_a_jour(tempsecouler,dessine,couleur)
            time.sleep(1 / 60)


    if __name__ == "__main__":
        main()
