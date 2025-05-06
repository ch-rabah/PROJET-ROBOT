import time
from model.environnement import Environnement
from model.robot import Robot
from model.obstacle import Rectangle, Triangle, Ligne, Cercle
from model.balise import Balise
from strategy.strategy import StrategyAvancer, StrategyTourner, StrategySequentielle, StrategyConditionnelle
from adapter.adapter import RobotAdapterSimulation
from view.affichage_3D import SimulationView3D
from strategy import  verif_sequence
from view import mise_a_jour_simulation, mettre_a_jour_temps
from __init__ import initialiser_simulation


def main():
    env, robot, simulation, sequence, previous_time, elapsed_time = initialiser_simulation()
    while True:
        previous_time, elapsed_time, dt = mettre_a_jour_temps(previous_time, elapsed_time)
        verif_sequence(sequence)
        mise_a_jour_simulation(env, robot, simulation, dt, elapsed_time)
        time.sleep(1/60)

if __name__ == "__main__":
    main()
