import time
from model.environnement import Environnement
from model.robot import Robot
from model.obstacle import Rectangle, Triangle, Ligne, Cercle
from model.balise import Balise
from strategy.strategy import StrategyAvancer, StrategyTourner, StrategySequentielle, StrategyConditionnelle
from adapter.adapter import RobotAdapterSimulation
from view.affichage_3D import SimulationView3D
from strategy import verif_sequence
from view import mise_a_jour_simulation, mettre_a_jour_temps
from __init__ import initialiser_simulation


def main():
    env, robot, simulation, sequence, previous_time, elapsed_time = initialiser_simulation()
    robot_adapter = RobotAdapterSimulation(robot)

    # Fonction de condition pour la stratégie conditionnelle
    def condition_func_distance_proche():
        distance = robot_adapter.get_distance()
        print(f"[Condition] Distance détectée : {distance}")
        return distance < 20  # Seuil arbitraire : obstacle à moins de 20 unités

    # Définir la stratégie conditionnelle
    strategy_conditionnelle = StrategyConditionnelle(
        robot_adapter,
        (StrategyTourner, 90),      # Si condition vraie : tourne
        (StrategyAvancer, 40),      # Sinon : avance
        condition_func_distance_proche
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
