import time
from FWSFR.adapter.adapter import RobotAdapterReel, RobotAdapterSimulation
from FWSFR.strategy import verif_sequence, initialiser_strategies
from FWSFR.view import mise_a_jour_simulation, mettre_a_jour_temps
from FWSFR.model import initialiser_environnement_robot

def initialiser_simulation():
    env, robot = initialiser_environnement_robot()
    robot_adapter = RobotAdapterReel()
    robot_adapter.start_record()
    sequence = initialiser_strategies(robot_adapter)
    previous_time = time.time()
    elapsed_time = 0

    return env, robot, robot_adapter, sequence, previous_time, elapsed_time

def main():

    env, robot, robot_adapter, sequence, previous_time, elapsed_time = initialiser_simulation()


    while True:
        previous_time, elapsed_time, dt = mettre_a_jour_temps(previous_time, elapsed_time)

        verif_sequence(sequence)

        time.sleep(1/60)


if __name__ == "__main__":
    main()
