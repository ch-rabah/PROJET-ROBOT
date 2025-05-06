import time
from FWSFR.model import initialiser_environnement_robot
from FWSFR.strategy import initialiser_strategies
from FWSFR.view.affichage_3D import SimulationView3D
from FWSFR.adapter import RobotAdapterSimulation

def initialiser_simulation():
    env, robot = initialiser_environnement_robot()
    robot_adapter = RobotAdapterSimulation(robot)
    simulation = SimulationView3D(env, robot)
    sequence = initialiser_strategies(robot_adapter)
    previous_time = time.time()
    elapsed_time = 0

    return env, robot, simulation, sequence, previous_time, elapsed_time