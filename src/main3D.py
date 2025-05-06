import time
from FWSFR.model.environnement import Environnement
from FWSFR.model.robot import Robot
from FWSFR.model.balise import Balise
from FWSFR.strategy.strategy import StrategyAvancer, StrategyTourner, StrategySequentielle, StrategyConditionnelle
from FWSFR.adapter.adapter import RobotAdapterSimulation
from FWSFR.view.affichage_3D import SimulationView3D
from FWSFR.strategy import verif_sequence, condition_func_distance_proche
from FWSFR.view import mise_a_jour_simulation, mettre_a_jour_temps
from __init__ import initialiser_simulation


def main():
    env, robot, simulation, sequence, previous_time, elapsed_time = initialiser_simulation()
    robot_adapter = RobotAdapterSimulation(robot)

    # Définir la stratégie conditionnelle
    strategy_conditionnelle = StrategyConditionnelle(
    robot_adapter,
    (StrategyTourner, 90),      # Si condition vraie : tourne
    (StrategyAvancer, 40),      # Sinon : avance
    lambda: condition_func_distance_proche(robot_adapter)  #  appel indirect
)


    while True:
        previous_time, elapsed_time, dt = mettre_a_jour_temps(previous_time, elapsed_time)

        if not strategy_conditionnelle.est_terminee():
            print("Exécution de la stratégie conditionnelle (distance)")
            strategy_conditionnelle.execute()
        else:
            verif_sequence(sequence)

        mise_a_jour_simulation(env, robot, simulation, dt, elapsed_time)
        time.sleep(1/60)

if __name__ == "__main__":
    main()
