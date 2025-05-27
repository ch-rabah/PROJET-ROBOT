import time
from robot2IN013 import Robot2IN013
from FWSFR.adapter.adapter import RobotAdapterReel
from FWSFR.strategy import verif_sequence, initialiser_strategies
from FWSFR.view import mettre_a_jour_temps

def initialiser_simulation():
    robot_adapter = RobotAdapterReel(Robot2IN013())
    sequence = initialiser_strategies(robot_adapter,3,2,10)
    previous_time = time.time()
    elapsed_time = 0

    return  sequence, previous_time, elapsed_time

def main():

    sequence, previous_time, elapsed_time = initialiser_simulation()


    while True:
        previous_time, elapsed_time, dt = mettre_a_jour_temps(previous_time, elapsed_time)

        verif_sequence(sequence)

        time.sleep(1/60)


if __name__ == "__main__":
    main()
