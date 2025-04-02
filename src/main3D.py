import time
from model.environnement import Environnement
from model.robot import Robot
from model.obstacle import Rectangle, Triangle, Ligne, Cercle
from strategy.strategy import StrategyAvancer, StrategyTourner, StrategySequentielle
from adapter.adapter import RobotAdapterSimulation
from view.affichage_3D import SimulationView3D


def main():
    # Créer l'environnement
    env = Environnement((0, 200), (0, 200))

    # Ajouter des obstacles
    env.ajouter_obstacle(Rectangle((40, 40), (40, 20)))
    env.ajouter_obstacle(Cercle((60, 120), 5))
    env.ajouter_obstacle(Ligne((20, 160), (180, 160), largeur=1))
    env.ajouter_obstacle(Triangle((20, 70), (30, 90), (40, 70)))

    # Créer le robot simulé
    robot = Robot(x=100, y=100, environnement=env, direction=0)
    robot_adapter = RobotAdapterSimulation(robot)

    # Créer la vue 3D
    simulation = SimulationView3D(env, robot)

    # Définir une séquence de stratégies (ex: faire un carré)
    sequence = StrategySequentielle(robot_adapter, [
        (StrategyAvancer, 30),
        (StrategyTourner, 90),
        (StrategyAvancer, 30),
        (StrategyTourner, 90),
        (StrategyAvancer, 30),
        (StrategyTourner, 90),
        (StrategyAvancer, 30),
        (StrategyTourner, 90),
    ])

    previous_time = time.time()
    elapsed_time = 0

    def update(t):
        nonlocal previous_time, elapsed_time
        now = time.time()
        dt = now - previous_time
        previous_time = now
        elapsed_time += dt

        if not sequence.est_terminee():
            sequence.execute(dt)

        env.update(robot, dt)
        simulation.mise_a_jour(elapsed_time)

    simulation.run(update)

if __name__ == "__main__":
    main()