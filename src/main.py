import time
from tkinter import Tk
from view.affichage_Tkinter import SimulationView
from model.robot import Robot
from model.environnement import Environnement
from model.obstacle import Rectangle, Cercle
from strategy.strategy import StrategyBoucleAllerRetour
from adapter.adapter import RobotAdapterSimulation
from RobotReel.Robot2I013 import Robot2I013




def main():
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
        simulation.mise_a_jour(tempsecouler)
        time.sleep(1 / 60)

    print("Stratégie terminée.")

if __name__ == "__main__":
    main()
