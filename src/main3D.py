import time
from model.environnement import Environnement
from model.robot import Robot
from model.obstacle import Rectangle, Triangle, Ligne, Cercle
from model.balise import Balise
from strategy.strategy import StrategyAvancer, StrategyTourner, StrategySequentielle
from adapter.adapter import RobotAdapterSimulation
from view.affichage_3D import SimulationView3D


def main():
    env = Environnement((0, 200), (0, 200))
    env.ajouter_obstacle(Rectangle((20, 20), (20, 10)))
    env.ajouter_obstacle(Cercle((60, 120), 5))
    env.ajouter_obstacle(Ligne((20, 160), (180, 160), largeur=1))
    env.ajouter_obstacle(Triangle((20, 70), (30, 90), (40, 70)))
    env.ajouter_balise(Balise(position=(110, 130), taille=10, hauteur=5, rotation=45))

    robot = Robot(x=100, y=100, environnement=env, direction=0)
    robot_adapter = RobotAdapterSimulation(robot)
    simulation = SimulationView3D(env, robot)

    sequence = StrategySequentielle(robot_adapter, [
        (StrategyAvancer, 30),
        (StrategyTourner, 90),
        (StrategyAvancer, 30),
    ])

    previous_time = time.time()
    elapsed_time = 0

    while True:
        now = time.time()
        dt = now - previous_time
        previous_time = now
        elapsed_time += dt

        sequence.execute()

        env.update(robot, dt)
        simulation.mise_a_jour(elapsed_time)
        simulation.app.step()
        time.sleep(1/60)


if __name__ == "__main__":
    main()
