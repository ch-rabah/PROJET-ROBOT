import time
from FWSFR.adapter.adapter import RobotAdapterSimulation
from FWSFR.view.affichage_3D import SimulationView3D
from FWSFR.strategy import verif_sequence, initialiser_strategies
from FWSFR.view import mise_a_jour_simulation, mettre_a_jour_temps
from FWSFR.model import initialiser_environnement_robot



def initialiser_simulation():
    """Initialise la simulation 3D avec Ursina, l'environnement et le robot.
    :return: Tuple contenant l'environnement, le robot, l'adaptateur de robot, la vue de simulation, la séquence de stratégies, le temps précédent et le temps écoulé
    """
    env, robot = initialiser_environnement_robot()
    simulation = SimulationView3D(env, robot)
    robot_adapter = RobotAdapterSimulation(robot, simulation)
    sequence = initialiser_strategies(robot_adapter)
    previous_time = time.time()
    elapsed_time = 0

    return env, robot, robot_adapter, simulation, sequence, previous_time, elapsed_time


def main():
    env, robot, robot_adapter, simulation, sequence, previous_time, elapsed_time = initialiser_simulation()


    while True:
        previous_time, elapsed_time, dt = mettre_a_jour_temps(previous_time, elapsed_time)

        verif_sequence(sequence)

        mise_a_jour_simulation(env, robot, simulation, dt, elapsed_time)
        time.sleep(1/60)

if __name__ == "__main__":
    main()
