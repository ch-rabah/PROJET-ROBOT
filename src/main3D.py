import time
from model.environnement import Environnement
from model.robot_3D import Robot
from model.obstacle_3D import Rectangle3D, Sphere3D, Ligne3D, Triangle3D
from strategy.strategy import StrategyAvancer, StrategyTourner, StrategyConditionnelle, StrategySequentielle
from adapter.adapter import RobotAdapterSimulation
from view.affichage_3D import SimulationView3D


def main():
    # Initialisation de l'environnement
    env = Environnement((0, 100), (0, 100))
    env.ajouter_obstacle(Rectangle3D((20, 0, 20), (20, 1, 10)))
    env.ajouter_obstacle(Sphere3D((60, 0, 60), 5))
    env.ajouter_obstacle(Ligne3D((10, 0, 80), (90, 0, 80), largeur=1))
    env.ajouter_obstacle(Triangle3D((20, 0, 70), (30, 0, 90), (40, 0, 70)))

    # Création du robot simulé
    robot = Robot(x=50, y=50, environnement=env, direction=0)
    robot_adapter = RobotAdapterSimulation(robot)

    # Affichage 3D
    simulation = SimulationView3D(env, robot)

    # Séquence de stratégies (ex : faire un carré)
    strategy_sequence = StrategySequentielle(
        robot_adapter,
        [
            (StrategyAvancer, 40),
            (StrategyTourner, 90),
            (StrategyAvancer, 40),
            (StrategyTourner, 90),
            (StrategyAvancer, 40),
            (StrategyTourner, 90),
            (StrategyAvancer, 40),
            (StrategyTourner, 90),
        ]
    )

    # Optionnel : stratégie conditionnelle ensuite
    strategy_conditionnelle = StrategyConditionnelle(
        robot_adapter,
        (StrategyAvancer, 20),
        (StrategyTourner, 90),
        False
    )

    # Temps pour animation
    previous_time = time.time()
    elapsed_time = 0

    def update(t):
        nonlocal previous_time, elapsed_time

        now = time.time()
        dt = now - previous_time
        previous_time = now
        elapsed_time += dt

        if not strategy_sequence.est_terminee():
            strategy_sequence.execute(dt)
        elif not strategy_conditionnelle.est_terminee():
            strategy_conditionnelle.execute(dt)

        env.update(robot, dt)
        simulation.mise_a_jour(elapsed_time)

    simulation.run(update)


if __name__ == "__main__":
    main()
