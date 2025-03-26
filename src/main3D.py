from model.environnement import Environnement
from model.robot_3D import Robot
from model.obstacle import Rectangle, Triangle, Ligne, Sphere
from view.affichage_3D import SimulationView3D


def main():
    # Créer l'environnement
    env = Environnement((0, 100), (0, 100))

    # Ajouter des obstacles
    env.ajouter_obstacle(Rectangle((20, 20), (20, 10)))
    env.ajouter_obstacle(Sphere((60, 60), 5))
    env.ajouter_obstacle(Ligne((10, 80), (90, 80), largeur=1))
    env.ajouter_obstacle(Triangle((20, 70), (30, 90), (40, 70)))

    # Créer le robot
    robot = Robot(x=50, y=50, environnement=env, direction=0)

    # Lancer l'affichage
    vue = SimulationView3D(env, robot)
    vue.run()


if __name__ == "__main__":
    main()
